# Publishing and resuming

## Repository checks

Read the working tree, current branch, remote, and `AGENTS.md` before changing files. The configured branch is a hint; inspect it rather than resetting or switching away from user work. Read the current `.gitignore`: Keynote files and `AGENTS.md` are intentionally ignored in the tested repository. Do not force-add them.

## Publication

For a new or changed notebook, verify it first, stage only that notebook, and commit with `<platform>_<notebook stem>`. For example, `LeetCode/002_Add_Two_Numbers.ipynb` uses `LeetCode_002_Add_Two_Numbers`. Commit its PNG separately with a descriptive cover subject. Workflow-source files belong in their own descriptive commit. Do not create empty commits for an unchanged existing notebook.

Push the intended branch normally. If authentication fails, request the normal GitHub sign-in flow, not a pasted access token. If the remote has advanced, inspect before integrating; do not force-push. Do not publish unrelated local commits without reviewing whether they are part of the authorized work.

After pushing, verify the branch's remote commit and file. `gh api` can read a GitHub content record including `sha` and `html_url`; quote a command argument containing `?ref=` so zsh does not interpret it as a glob. Compare the content record's `sha` with `git hash-object` for the local file. Construct the final notebook URL using the verified branch and repository-relative path, URL-encoding components when necessary.

## Checkpoint

Record per-problem platform, number, title, repository-relative notebook path, verified notebook blob SHA and GitHub URL, cover path and dimensions, metadata source, YouTube link if supplied, and tracker state. A local checkpoint under `.git/workflow-state/` stays outside tracked source without adding a new ignore rule. It must contain no credentials. The checkpoint is a convenience; the remote and sheet readback are the authoritative evidence.

On retry, inspect reality before repeating mutations. Reuse an unchanged published notebook and cover. Recheck whether a timed-out sheet write succeeded before retrying. Preserve a supplied or existing YouTube link. Report stages as completed, pending, or failed individually.
