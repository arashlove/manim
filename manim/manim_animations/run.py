"""
Run any scene by name. Usage:
  poetry run manim-animate <SceneName>              # preview
  poetry run manim-animate <SceneName> --gif        # export GIF
  poetry run manim-animate <SceneName> --gif -qh    # high-quality GIF
  poetry run manim-animate                          # list scenes

When adding a new scene: add it to SCENE_MODULES and to scenes/__init__.py.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

# Scene class name -> module path (module must define that class)
SCENE_MODULES = {
    "VectorAsPointInSpace": "manim_animations.scenes.vector_intuition",
    "DotProductAndNorm": "manim_animations.scenes.dot_norm",
    "MatrixTransformsGIF": "manim_animations.scenes.matrix_transforms",
}


def main():
    argv = sys.argv[1:]
    if not argv or argv[0].startswith("-"):
        print("Usage: manim-animate <SceneName> [--gif] [manim options...]")
        print("Examples:")
        print("  manim-animate VectorAsPointInSpace")
        print("  manim-animate VectorAsPointInSpace --gif -qh")
        print("\nScenes:", ", ".join(sorted(SCENE_MODULES)))
        sys.exit(0 if not argv else 1)

    scene_name = argv[0]
    argv = argv[1:]

    if scene_name not in SCENE_MODULES:
        print(f"Unknown scene: {scene_name}")
        print("Available:", ", ".join(sorted(SCENE_MODULES)))
        sys.exit(1)

    if "--gif" in argv:
        argv = [a for a in argv if a != "--gif"]
        if not any(a.startswith("-q") for a in argv):
            argv = ["-ql", *argv]
        argv = ["--format=gif", *argv]
    else:
        if not any(a.startswith("-q") for a in argv):
            argv = ["-pql", *argv]
        if "-p" not in argv and "--preview" not in argv:
            argv = ["-p", *argv]

    module_name = SCENE_MODULES[scene_name]
    spec = importlib.util.find_spec(module_name)
    if spec is None or spec.origin is None:
        print(f"Could not find module: {module_name}")
        sys.exit(1)
    scene_file = Path(spec.origin).resolve()

    cmd = ["manim", *argv, str(scene_file), scene_name]
    sys.exit(subprocess.run(cmd).returncode)


if __name__ == "__main__":
    main()
