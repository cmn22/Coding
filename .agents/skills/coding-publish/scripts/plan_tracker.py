#!/usr/bin/env python3
"""Plan one tracker upsert from a tool-read snapshot; never writes to Google."""
import argparse
import json
from pathlib import Path


def problem_number(value):
    if type(value) is int and value >= 1:
        return value
    if isinstance(value, str) and value.strip().isdigit() and int(value.strip()) >= 1:
        return int(value.strip())
    raise ValueError(f'Invalid problem number: {value!r}')


def plan(snapshot, desired):
    headers = snapshot['headers']
    if len(headers) != len(set(headers)):
        raise ValueError('Duplicate headers must be resolved before writing.')
    expected = ['Number', 'Problem Name', snapshot.get('link_column', 'LeetCode Link'),
                'Difficulty', 'Topics', 'GitHub Solution', 'YT Link']
    if not headers:
        if snapshot.get('rows'):
            raise ValueError('A populated tab cannot have missing headers.')
        if snapshot.get('empty_tab_verified') is not True:
            raise ValueError('Confirm the tab is empty before planning header creation.')
        headers = expected
        initialize = True
    else:
        missing = [x for x in expected if x not in headers]
        if missing:
            raise ValueError(f'Missing required headers: {missing}')
        initialize = False
    number = problem_number(desired['Number'])
    fields = {key: desired[key] for key in expected if key in desired}
    if any(key not in fields or fields[key] in ('',None) for key in expected if key != 'YT Link'):
        raise ValueError('All problem fields except YT Link are required.')
    fields['Number'] = number
    matches = []
    for row in snapshot.get('rows', []):
        value = row['values'].get('Number')
        if value in (None,''):
            continue
        if problem_number(value) == number:
            matches.append(row)
    if len(matches) > 1:
        raise ValueError('Multiple matching rows; resolve duplicates before writing.')
    if matches:
        current = matches[0]
        # An omitted or empty new YouTube link does not erase one already present.
        if fields.get('YT Link') in ('',None):
            fields['YT Link'] = current['values'].get('YT Link', '')
        changes = {key:value for key,value in fields.items()
                   if (problem_number(current['values']['Number']) if key=='Number' else current['values'].get(key,'')) != value}
        return {'action':'update' if changes else 'noop', 'row_number':current['row_number'],
                'changes':changes, 'expected_values':fields, 'initialize_headers':False}
    next_row = snapshot.get('append_row_number')
    if type(next_row) is not int or next_row < 2:
        raise ValueError('A verified append_row_number after the last record is required.')
    if any(r['row_number'] >= next_row for r in snapshot.get('rows', [])):
        raise ValueError('append_row_number would overwrite an existing row.')
    fields.setdefault('YT Link','')
    return {'action':'append','row_number':next_row,'changes':fields,'expected_values':fields,
            'initialize_headers':headers if initialize else False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot',type=Path)
    parser.add_argument('desired',type=Path)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    result=plan(json.loads(args.snapshot.read_text()),json.loads(args.desired.read_text()))
    output=json.dumps(result,indent=2)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(output)
    print(output,end='')

if __name__=='__main__':
    main()
