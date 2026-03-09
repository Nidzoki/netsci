# Image Layout Patterns In This Repo

## Inline Figure

Use for the main image on a slide:

```markdown
![width:900px](images/example.png)
```

Prefer this for central diagrams, process snapshots, and large comparison visuals.

## Right Background With Text

Use when the explanation and figure should share the slide:

```markdown
![bg right:50% width:700px](images/example.png)
```

This pattern appears throughout `lectures/02/lecture.md`, `lectures/05/lecture.md`, and `lectures/07/lecture.md`.

## Full Background

Use when the image should dominate the slide:

```markdown
![width:1200px bg](images/example.png)
```

Reserve this for high-value visuals that remain readable behind minimal text.

## Side-By-Side Code And Image

Use when the code directly explains the figure:

````markdown
<div class="columns">
<div>

```python
# short, focused example
```

</div>
<div>

![width:380px](images/example.png)

</div>
</div>
````

Keep code short enough to present live.

## Progression Slides

Use several slides with stable image placement when teaching a step-by-step process. Keep widths and positions consistent so only the concept changes from slide to slide.
