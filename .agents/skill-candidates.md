# Skill Candidates From `.cursor/rules`

This note maps the existing Cursor rules to agent-skill candidates for this repo.

## Create These Skills

### 1. `lecture-image-generator`

Create a skill for building and updating lecture visualization scripts and generated assets.

Use source material from:
- `.cursor/rules/lecture-image-generation.mdc`
- `.cursor/templates/image_generation_template.py`

Why this is worth a skill:
- It describes a repeatable workflow used across many lecture folders.
- It includes concrete implementation patterns, not just style advice.
- It has an obvious reusable asset: the image-generation template.
- It benefits from progressive disclosure: the skill can keep the workflow in `SKILL.md` and store the template under `assets/` or `references/`.

What the skill should do:
- Scaffold `generate_*.py` files for a lecture.
- Enforce `images/` output, reproducible seeds, save helpers, and figure cleanup.
- Adapt examples to NetworkX and matplotlib-heavy lecture content.
- Remind the agent to keep scripts runnable from the lecture directory.

Recommended bundled resources:
- `assets/image_generation_template.py`
- `references/repo-patterns.md` with a few real examples from `lectures/*/generate_*.py`

### 2. `marp-lecture-author`

Create a skill for writing and editing course lecture decks in Marp.

Use source material from:
- `.cursor/rules/marp-slide-structure.mdc`
- `.cursor/rules/marp-directives-styling.mdc`
- `.cursor/rules/marp-content-best-practices.mdc`
- `.cursor/rules/marp-advanced-features.mdc`
- `.cursor/rules/lecture-image-linking.mdc`
- `.cursor/rules/marp-export-presentation.mdc`

Why this is worth a skill:
- The repo uses Marp heavily for lectures.
- The rules form one coherent authoring workflow: structure, styling, image placement, and export.
- The material is procedural enough to help another agent produce consistent lecture decks.
- It is repo-specific because lectures mix network-science content, generated images, and Marp layout conventions.

What the skill should do:
- Draft or revise `lectures/XX/lecture.md`.
- Apply frontmatter, slide-break, title, and pagination conventions.
- Choose between inline images, background images, split layouts, and code-image pairings.
- Keep slides concise and presentation-friendly.
- Include export and presentation checks only as a final step.

Recommended structure:
- Keep the core workflow in `SKILL.md`.
- Move Marp syntax patterns into `references/layout-patterns.md`.
- Move example snippets for image layouts and split slides into `references/image-layouts.md`.

## Maybe Later, But Not From Current Rules Alone

### 3. `notebook-polish`

Possible future skill, but the current notebook rules are too generic on their own.

Source rules:
- `.cursor/rules/ipynb-code-organization.mdc`
- `.cursor/rules/ipynb-dependency-management.mdc`
- `.cursor/rules/ipynb-documentation.mdc`
- `.cursor/rules/ipynb-output-management.mdc`
- `.cursor/rules/ipynb-performance.mdc`
- `.cursor/rules/ipynb-reproducibility.mdc`

Why not yet:
- These read like general best practices, not a concrete repo workflow.
- They do not include templates, scripts, or local conventions strong enough to justify a dedicated skill.
- A skill here would be too broad unless you define specific operations such as "clean notebook for release", "make notebook reproducible", or "convert notebook into tutorial-ready state".

When it becomes worth a skill:
- Add scripts for stripping outputs, checking execution order, exporting dependency snapshots, or validating restart-and-run-all.
- Add repo-specific notebook conventions from `tutorials/` and `exercises/`.

## Do Not Turn These Into Skills

### `auto_conventional_commits.mdc`

Do not create a local skill from this rule.

Why:
- The workflow already maps to the existing `git-conventional-commit` skill in your global skill set.
- The "commit after every operation" part is agent-policy territory, not a reusable repo skill.

### `store_rules_in_directory.mdc`

Do not create a skill from this rule.

Why:
- This is a repository housekeeping rule for Cursor config organization.
- It is not a user-triggered workflow.

## Recommended Bundling

Create two repo-local skills instead of many one-rule skills:

1. `lecture-image-generator`
2. `marp-lecture-author`

Keep notebook guidance as rules for now.

This split matches how work happens in the repo:
- one workflow generates lecture visuals
- one workflow writes and lays out lecture slides

It also avoids creating weak skills from generic advice.
