#!/usr/bin/env python3
"""Read-only execution check for a trusted coding-solution notebook."""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import traceback


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('notebook', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--timeout', type=int, default=60)
    args = parser.parse_args()
    original = args.notebook.read_bytes()
    report = {'notebook': str(args.notebook.resolve()), 'sha256': hashlib.sha256(original).hexdigest(),
              'passed': False, 'code_cells': 0, 'execution_method': None,
              'standalone_submission_check': 'Run a separate platform-specific fixture; not performed by this helper'}
    try:
        document = json.loads(original)
        if document.get('nbformat') != 4:
            raise ValueError('Expected notebook format 4.')
        cells = document['cells']
        if not cells or cells[-1].get('cell_type') != 'code':
            raise ValueError('The final cell must contain submission code.')
        if document.get('metadata', {}).get('kernelspec', {}).get('language') != 'python':
            raise ValueError('Expected Python kernel metadata.')
        ids = [c['id'] for c in cells if 'id' in c]
        if len(ids) != len(set(ids)):
            raise ValueError('Notebook contains duplicate cell IDs.')
        for index, cell in enumerate(cells):
            if cell.get('cell_type') not in ('markdown', 'code', 'raw'):
                raise ValueError(f'Invalid cell type at position {index}.')
            if not isinstance(cell.get('source'), (list, str)):
                raise ValueError(f'Invalid source at position {index}.')
        sources = [(i, ''.join(c['source'])) for i, c in enumerate(cells) if c['cell_type'] == 'code']
        report['code_cells'] = len(sources)
        report['saved_output_errors'] = [i for i,c in enumerate(cells) if c['cell_type']=='code'
                                         and any(o.get('output_type')=='error' for o in c.get('outputs',[]))]
        if report['saved_output_errors']:
            raise ValueError('Saved outputs contain error tracebacks.')
        available = all(importlib.util.find_spec(x) is not None for x in ('nbformat','nbclient','ipykernel'))
        with tempfile.TemporaryDirectory(prefix='coding-notebook-') as directory:
            if available:
                import nbformat
                from nbclient import NotebookClient
                node = nbformat.reads(original.decode('utf-8'), as_version=4)
                nbformat.validate(node)
                report['execution_method'] = 'fresh Jupyter kernel'
                client = NotebookClient(node, timeout=args.timeout, kernel_name='python3',
                                        resources={'metadata':{'path':directory}})
                client.execute()
            else:
                report['execution_method'] = 'sequential Python exec in a fresh shared namespace; no Jupyter kernel'
                report['limitation'] = 'Python fallback does not emulate IPython magics or rich display semantics.'
                namespace = {'__name__':'__main__'}
                # The coding notebook contract uses standard Python and no file dependencies.
                # Launch this helper from scratch; its cwd is deliberately not the repository.
                import os
                previous = Path.cwd()
                try:
                    os.chdir(directory)
                    for index, source in sources:
                        with contextlib.redirect_stdout(io.StringIO()):
                            exec(compile(source, f'notebook_cell_{index+1}', 'exec'), namespace)
                finally:
                    os.chdir(previous)
        report['passed'] = True
    except Exception as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
        report['traceback'] = traceback.format_exc()
    if args.notebook.read_bytes() != original:
        report['passed'] = False
        report['error'] = 'Notebook changed during read-only verification.'
    encoded = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(encoded)
    print(encoded, end='')
    return 0 if report['passed'] else 1

if __name__ == '__main__':
    sys.exit(main())
