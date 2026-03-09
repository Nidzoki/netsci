# Marp Layout Patterns In This Repo

## Frontmatter Baseline

Most lectures start with a frontmatter block like:

```yaml
---
marp: true
theme: default
paginate: true
footer: "Network Analysis - PMF-UNIST 2024/2025"
---
```

Treat this as the baseline unless the target lecture already uses a different convention.

## Common Slide Flow

Many lecture decks follow this pattern:

1. Title slide with lecture topic, course, instructor, and date
2. "What we'll learn today" slide
3. One concept per slide or short slide pair
4. Code examples only where they teach the concept
5. Summary, references, or annex content when useful

## Good Local Examples

- `lectures/05/lecture.md` for overall pacing and concept sequencing
- `lectures/07/lecture.md` for image-led explanation
- `lectures/10/lecture.md` for repeated explanatory pattern with one figure per model
- `lectures/11/lecture.md` for concise topical slides plus an annex file

## Structural Rules

- Use `---` on its own line for slide breaks.
- Leave a blank line around each slide break.
- Keep headings short.
- Split dense material into multiple slides instead of reducing font size by hand.
