---
name: lecture-image-generator
description: Create, extend, or refactor Python scripts that generate lecture figures for this repository's network science course materials. Use when working on `lectures/*/generate_*.py`, adding or regenerating files in `lectures/*/images/`, adapting the lecture image template, or keeping NetworkX and matplotlib visualizations reproducible, consistent, and easy to link from Marp slides.
---

# Lecture Image Generator

## Overview

Create lecture visuals as code, not as one-off notebook output. Keep generation scripts reproducible, lecture-local, and aligned with the existing `lectures/*/generate_*.py` patterns in this repository.

Read [`references/repo-patterns.md`](references/repo-patterns.md) when you need concrete examples from existing lecture scripts. Copy or adapt [`assets/image_generation_template.py`](assets/image_generation_template.py) when starting a new generator from scratch.

## Workflow

### 1. Inspect the lecture context

- Read the target `lectures/XX/lecture.md` before naming images or choosing layouts.
- Inspect existing `generate_*.py` files in the same lecture before introducing a new script.
- Reuse existing filenames when updating visuals so slide links stay stable.
- Use a new script only when the lecture has no suitable generator or when a topic is clearly separate.

### 2. Start from the lecture template or an existing script

- For a new generator, copy `assets/image_generation_template.py` into the lecture directory and rename it to a descriptive `generate_*.py` filename.
- For an existing generator, preserve the current structure unless it is actively blocking the task.
- Keep scripts runnable from the lecture directory with relative paths such as `images/...`.

### 3. Keep generation deterministic and lecture-local

- Create the `images/` directory in code if needed.
- Set a fixed random seed before any stochastic layout or sampling step.
- Prefer a shared helper for repeated save-and-style logic.
- Close figures after saving to avoid memory leaks in multi-image scripts.
- Print progress messages when generation is non-trivial.

### 4. Organize code around output images

- Use one function per distinct figure or figure family.
- Give each function a clear docstring that explains the teaching purpose of the image.
- Return reusable objects only when that materially simplifies related figures.
- Keep `main()` as the place that orchestrates all outputs for the script.

### 5. Match repository conventions

- Save into `images/<descriptive-name>.png` unless the lecture already uses another extension.
- Prefer descriptive filenames that map cleanly to slide content.
- Use NetworkX, matplotlib, and NumPy directly unless the lecture already depends on another library.
- Keep figure sizes and DPI appropriate for slide use, not paper publication.

### 6. Verify outputs before finishing

- Run the generator after editing it.
- Confirm that expected files were written under `images/`.
- If the task includes slide updates, verify that every referenced filename exists.
- If the task is primarily about slide layout or Marp authoring, switch to or combine with `marp-lecture-author`.

## Patterns To Preserve

- Prefer simple, readable code over abstract helper layers.
- Keep each script understandable by an instructor editing it later.
- Use inline comments sparingly and only where the visualization logic is not obvious.
- Avoid notebook-only idioms or hidden state.

## Outputs

- `lectures/XX/generate_*.py`
- `lectures/XX/images/*.png`
- Optional small adjustments to `lectures/XX/lecture.md` when image names or ordering change

## Avoid

- Do not hardcode absolute paths.
- Do not save figures outside the lecture directory.
- Do not introduce a new generator file when a small edit to an existing one is enough.
- Do not change image filenames casually when slides already reference them.
