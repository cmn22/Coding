# Direct Google Sheets tracker

Use `references/workspace.json` for the document ID and platform-tab mapping. For LeetCode the required columns are, in order:

`Number | Problem Name | LeetCode Link | Difficulty | Topics | GitHub Solution | YT Link`

Number is the platform's numeric problem identifier, not a row counter. Topics are the official platform tags; use `Array, Hash Table` for the verified Two Sum trial. Use actual plain URLs for link values unless the sheet has an established hyperlink formatting convention.

## Connection selection

1. Discover available direct Google Drive / Google Sheets editing tools. If Google Drive is installed, follow its Google Sheets instructions and inspect the supported read/write operations. Installation alone does not prove editing permission.
2. Alternatively, discover connected document sessions for `sheets`. Match the exact spreadsheet ID, inspect the selected session's supported tool schemas, then issue commands using that session and stable idempotency keys. Never guess tool names or schemas. A session for another workbook is not sufficient.
3. If neither direct route can read and edit this spreadsheet, keep the prepared row pending. Explain that the Google Drive plugin must be installed and connected to an account with editor access, or that this exact document needs an editing-capable connected session. Do not invent add-on setup buttons or promise persistent sessions. Do not change sharing settings, ask the user to publish the sheet, or fall back to browser editing unless explicitly authorized.

The trial found the in-sheet ChatGPT extension installed but no connected document sessions. Google Drive was available but not yet installed/connected when the integration was suggested. Recheck these observations each time; do not treat an old blocker as current evidence.

## Upsert and readback

- Read spreadsheet/tab metadata, headers, and existing rows before a write. Match the exact platform tab; use the configured gid only after confirming its name.
- If a tab is empty, initialize the seven requested headings. If populated, map headings first and preserve additional columns and formatting. Do not reorder or overwrite existing data to force a layout.
- Find the problem by its numeric Number within that platform tab. Exactly one match means update that row; no match means append after the last existing record. Multiple matches require resolving ambiguity before writing, not updating an arbitrary row.
- Preserve nonempty YT Link when the current request provides no YouTube URL. A supplied YouTube link replaces that field for the identified problem. For video-link-only requests, edit only YT Link.
- Write only the intended range/cells. Preserve unrelated formulas, formatting, extra columns, and other rows. A confirmed GitHub URL is required before filling GitHub Solution.
- Re-read the changed row. Compare all seven intended values and verify the problem appears once. If a write times out, read again before repeating the mutation.
- Verify a second planning/read pass recognizes the row as current and does not append a duplicate. Never add a throwaway row merely to test permissions.

## Trial values

- Number: `1`
- Problem Name: `Two Sum`
- LeetCode Link: `https://leetcode.com/problems/two-sum/`
- Difficulty: `Easy`
- Topics: `Array, Hash Table`
- GitHub Solution: `https://github.com/cmn22/Coding/blob/master/LeetCode/001_Two_Sum.ipynb`
- YT Link: `https://youtu.be/4iVPG4mUH3c`

## Deterministic planning helper

After a direct tool read, normalize its result to a snapshot with `headers` (list), `rows` (list of objects with actual `row_number` and a `values` mapping keyed by header), and `append_row_number` (the verified first row after the last existing record). Include the platform's `link_column` when it differs from `LeetCode Link`. For a genuinely empty tab set `empty_tab_verified: true`, `headers: []`, `rows: []`, and `append_row_number: 2`.

Save the desired seven-field mapping separately, then run `scripts/plan_tracker.py SNAPSHOT.json DESIRED.json --report PLAN.json`. It plans an append, an update of only changed fields, or no operation; it preserves an existing YT Link when omitted and rejects duplicate problem rows or ambiguous headers. It is a local planner, not a Google Sheets connection. Execute its planned cells through the selected direct tool, then read back and replan to verify a no-op. Keep any unrelated columns intact. A video-link-only request should update only YT Link directly after identifying the unique problem row.
