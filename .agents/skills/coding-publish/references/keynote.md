# Keynote cover procedure

Use the configured repository `.key` file as the master. The tested master is a single widescreen slide with a black background, a large white platform title, a smaller `1. Two Sum` problem label, and the author's name. Reinspect the actual file if it changes.

1. Copy the master to a working `.key` file; never overwrite the master for an individual problem. Open the copy with the available computer-use tools. Native app interactions must use those tools, not shell-driven UI automation.
2. Read the current slide and its editable text boxes. Update the existing platform title and the `<number>. <problem name>` label. Preserve the author credit, typography, alignment, background, and slide size. For longer names, verify fitting rather than silently shortening the official title. The master already matches Two Sum, so that trial required no text changes; editing a different problem's text is still to be tested.
3. In Keynote choose File > Export To > Images. Select PNG, one cover slide, no per-build images, and leave transparent background disabled. Use the slide's native dimensions. The tested export is 1920 x 1080 pixels.
4. Export to a scratch directory. Keynote creates a directory containing a slide-numbered file such as `LeetCode_001_Two_Sum_Cover.001.png`. Inspect the actual output, then copy/rename that single file to the configured cover destination.
5. Open the PNG to confirm the platform and complete problem name, no clipped text, preserved author credit, and no editor chrome. Check PNG signature, dimensions, 16:9 aspect ratio, and nonempty file size. Prefer at least 1280 x 720 pixels for the existing cover design.
6. Verify the source master is unchanged. Keep the required PNG with the repository assets; do not change the repository's `.key` ignore rule just to publish the editable copy. Return the PNG inline in the completion response.

A low-resolution embedded `preview.jpg` can help inspect the source but is not an exported cover. A screenshot of the Keynote editor is not equivalent to the clean slide image. If native export fails, report the limitation; do not silently redesign the cover or substitute an unrelated rendering.
