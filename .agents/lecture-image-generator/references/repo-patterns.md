# Lecture Image Patterns In This Repo

Use these files as concrete examples before inventing a new structure.

## Script Patterns

- `lectures/02/generate_graph_examples.py`
  Good example of one script producing many teaching figures into `images/`.

- `lectures/05/generate_images.py`
  Good example of a shared `save_figure(...)` helper plus several concept-specific generators.

- `lectures/07/generate_ws_images.py`
  Good example of higher-DPI output and consistent save logic for multiple related visuals.

- `lectures/08/generate_images.py`
  Good example of a larger lecture generator with many outputs and stable naming.

- `lectures/11/generate_multilayer_visuals.py`
  Good example of a compact helper-based script for a focused topic.

## Slide Integration Patterns

- `lectures/02/lecture.md`
  Frequent use of right-background images paired with short explanatory bullets.

- `lectures/05/lecture.md`
  Mix of background images, full-width figures, and code examples for algorithm explanation.

- `lectures/07/lecture.md`
  Reuses related images with consistent placement across multiple slides.

- `lectures/09/lecture.md`
  Shows more advanced image usage, including wide backgrounds and image tables.

## Repeated Conventions

- Create `images/` from code if needed.
- Save figures with descriptive names that map directly to slide topics.
- Use reproducible seeds for spring layouts and stochastic sampling.
- Close figures after saving.
- Keep scripts readable enough that an instructor can edit them directly.
