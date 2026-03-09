---
name: marp-lecture-author
description: Draft, revise, and polish Marp-based lecture decks for this repository. Use when editing `lectures/*/lecture.md`, `lecture_annex.md`, or other Marp markdown files, structuring slides, applying Marp directives, pairing generated images with explanations, or preparing a deck for export and presentation.
---

# Marp Lecture Author

## Overview

Write lecture decks that match the repository's existing course style instead of producing generic slides. Keep slide flow concise, teaching-oriented, and aligned with generated images and network-science examples already present in the lecture folder.

Read [`references/layout-patterns.md`](references/layout-patterns.md) for concrete Marp structures and [`references/image-layouts.md`](references/image-layouts.md) when choosing between inline, background, or split-image slides.

## Workflow

### 1. Read the local lecture context first

- Read the target lecture file before rewriting structure or tone.
- Inspect nearby images and generator scripts so slide content matches real assets.
- Reuse the lecture's current frontmatter and footer conventions unless the task is to standardize them.

### 2. Keep slides lecture-first, not document-first

- Put one main teaching idea on each slide.
- Break dense explanations into multiple slides instead of building text walls.
- Keep headings short and clear.
- Prefer bullets or short code blocks over prose-heavy paragraphs.

### 3. Follow the repository's Marp structure

- Start files with Marp frontmatter.
- Preserve `marp: true`, `theme`, and pagination unless there is a concrete reason to change them.
- Use `---` with surrounding blank lines for slide breaks.
- Keep title slides and "what we'll learn" slides aligned with nearby lecture patterns when creating a new lecture.

### 4. Choose image layout intentionally

- Use full-width inline images for central diagrams or process sequences.
- Use right-background layouts when image and explanation should share a slide.
- Use side-by-side code and image layouts only when the code materially explains the image.
- Keep repeated image sequences stable in size and position across slides.
- If the task mainly requires generating or regenerating figures, use `lecture-image-generator`.

### 5. Write for teaching clarity

- State what matters before showing implementation details.
- Prefer examples that are small enough to discuss live.
- Keep bullet lists shallow.
- Use citations or source notes only when they add real value.

### 6. Use Marp features selectively

- Use local directives for exceptional slides, not every slide.
- Use background images and split layouts where they improve pacing.
- Use Mermaid or math blocks only when the concept benefits from them.
- Keep custom styling minimal and local to the deck.

### 7. Finish with presentability checks

- Check that image paths resolve relative to the lecture file.
- Check that slide separators and fenced blocks are balanced.
- If export is requested, use the repo's Marp CLI workflow and verify the target format.
- Keep speaker notes in HTML comments when needed.

## Default Conventions

- Use sentence-case slide titles.
- Prefer concise bullets and short explanation blocks.
- Preserve existing footer and course metadata style within a lecture.
- Use relative image paths such as `images/foo.png` in lecture files.

## Outputs

- `lectures/XX/lecture.md`
- `lectures/XX/lecture_annex.md`
- Optional coordinated image-link updates after figure regeneration

## Avoid

- Do not produce generic corporate-slide language.
- Do not overuse local directives or CSS when plain Marp structure is enough.
- Do not crowd a slide with both long prose and a complex figure.
- Do not rename or move images without updating every reference.
