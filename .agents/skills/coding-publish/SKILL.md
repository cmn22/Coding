---
name: coding-publish
description: Prepare and publish CMN coding-problem notebooks, export PNG video covers from the repository's Keynote template, and update the platform tab in the Google Sheets tracker. Use for a problem link, an end-to-end publishing request, a retry, or adding a YouTube link to an existing problem.
---

# Coding Publisher

Turn a problem link into a verified notebook, a published GitHub solution, a PNG cover, and one tracker row. Existing solutions and video-link-only requests should update only what is needed.

Read [the workspace settings](references/workspace.json) first. Read the repository's current `AGENTS.md` and reference notebook for authoring rules; do not duplicate those rules here. The user's current request overrides saved defaults. Preserve unrelated working-tree changes.

## Workflow

1. Inspect the repository, active branch, remote, existing notebook, and existing generated assets. Resolve the official platform, problem number, title, difficulty, topic tags, constraints, examples, and Python editor interface. Use official sources; do not infer official topic tags from the algorithm. If required metadata cannot be read, mark that field pending rather than inventing it.
2. Create or revise `<platform>/<number padded to at least 3 digits>_<Title_With_Underscores>.ipynb` following `AGENTS.md`. For an already-published unchanged notebook, verify and reuse it without a duplicate commit. Keep the notebook suitable for public readers and a recording script, with no workflow or video-companion notes.
3. Run `scripts/check_notebook.py NOTEBOOK --report REPORT.json`. This executes every code cell in order, using a Jupyter kernel when available and an explicitly reported Python fallback otherwise. It never modifies the notebook. Also test the final submission cell independently against representative valid inputs, supplying only data types normally supplied by the platform. Correct failures and stale saved outputs before publishing. For newly authored notebooks, save real execution outputs with the actual execution method recorded.
4. Prepare the cover using [the Keynote procedure](references/keynote.md). The required deliverable is an exported PNG of the slide, not an editor screenshot. Preserve the master. Store `<platform>/covers/<notebook stem>.png`; retain an editable `.key` copy locally if useful (the repository ignores `.key`). Inspect the exported image before publishing.
5. Publish only verified intended files. Read [publishing and retry rules](references/publishing.md). Notebook commit subjects are `<platform>_<notebook stem>` without the extension, for example `LeetCode_002_Add_Two_Numbers`. Keep cover/workflow changes in separate descriptive commits. Push the current intended branch to the configured remote, then read back the remote file and verify its Git blob SHA matches the local file. Never assume `main`; this repository currently uses `master`. Use the remote's actual branch when constructing the GitHub blob URL. Do not force-push or create a second remote. Respect requests for a draft, local-only output, or no publishing.
6. Update the Google Sheet through a direct editing tool, following [tracker rules](references/tracker.md). Read before writing, match the platform tab and problem number, preserve an existing YouTube link if none was supplied, and verify by reading the changed row back. A missing connector must not be silently replaced with browser editing: prepare a pending row and continue other work. Never report a sheet write as complete until the readback succeeds.
7. Give a short result with the GitHub link, the actual cover PNG, and tracker status. Report each incomplete step and the one action needed to unblock it. Keep a local checkpoint of completed steps and pending tracker values so the next invocation can resume without duplicate commits or rows. Do not describe a partially tested workflow as flawless or fully complete.

## Scope and invocation

A request to publish a problem authorizes that problem's notebook, cover, commit/push, and tracker update; a bare link in this established workflow can identify the next problem, while a link supplied merely as background does not authorize publishing. Ask only when ambiguity changes the outcome. Do not schedule runs, publish videos to YouTube, or change Google sharing/access settings. A video-link-only request updates the matching tracker row without regenerating the notebook or cover.

Normal invocation: `$coding-publish https://leetcode.com/problems/add-two-numbers/`. A supplied YouTube link may accompany the problem link or arrive later. For another platform, use its own folder and tracker tab; use the equivalent platform link heading rather than a LeetCode URL.
