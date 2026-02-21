# Manim ML/Math explainer GIFs

One scene per concept (vectors, linear algebra, ML, etc.). Black background, white text, one accent. Built for short, loop-friendly GIFs.

## System requirements (Windows)

Manim needs these on your **PATH** (install them before running):

- **LaTeX** — for `MathTex` (formulas). Install [MiKTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/). Restart the terminal after installing so PATH is updated.
- **ffmpeg** — for video/GIF output. Install from [ffmpeg.org](https://ffmpeg.org/download.html) or via `winget install ffmpeg`, and ensure the `ffmpeg` binary is on PATH.

Without these you may see `FileNotFoundError` (LaTeX) or “Couldn't find ffmpeg” (video/GIF).

## Quick start

```bash
poetry install
poetry run manim-animate                                    # list scenes
poetry run manim-animate VectorAsPointInSpace               # preview
poetry run manim-animate VectorAsPointInSpace --gif         # export GIF
poetry run manim-animate VectorAsPointInSpace --gif -qh     # high-quality GIF
```

Output: `media/videos/<module>/<quality>/<SceneName>.mp4` or `.gif`.

## Adding a new scene

1. **Create the scene file**  
   Add e.g. `manim_animations/scenes/my_concept.py` with a class that subclasses `Scene` or `ThreeDScene`:

   ```python
   from manim import *

   class MyNewConcept(Scene):
       def construct(self):
           self.camera.background_color = BLACK
           # ...
   ```

2. **Register it**  
   In `manim_animations/run.py`, add to `SCENE_MODULES`:

   ```python
   SCENE_MODULES = {
       "VectorAsPointInSpace": "manim_animations.scenes.vector_intuition",
       "MyNewConcept": "manim_animations.scenes.my_concept",
   }
   ```

3. **Export from the package (optional)**  
   In `manim_animations/scenes/__init__.py`, import and add to `__all__`:

   ```python
   from manim_animations.scenes.vector_intuition import VectorAsPointInSpace
   from manim_animations.scenes.my_concept import MyNewConcept
   __all__ = ["VectorAsPointInSpace", "MyNewConcept"]
   ```

Then run:

```bash
poetry run manim-animate MyNewConcept --gif
```

## Structure

- `manim_animations/scenes/` — one module per concept, each with one or more scene classes.
- `manim_animations/run.py` — `manim-animate <SceneName> [--gif]`; scene list lives in `SCENE_MODULES`.

## Current scenes

| Scene                 | Concept                                                    |
|-----------------------|------------------------------------------------------------|
| `VectorAsPointInSpace` | Vector as a point (2D → 3D, loop)                          |
| `DotProductAndNorm`    | Dot product vs angle, norms, cosine-similarity hint       |
