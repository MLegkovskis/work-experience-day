from __future__ import annotations

from pathlib import Path
import importlib
import importlib.util

if importlib.util.find_spec("flask") is None:
    class Flask:  # type: ignore[override]
        def __init__(self, name: str):
            self.name = name

        def route(self, _path: str):
            def decorator(func):
                return func

            return decorator

        def test_request_context(self, _path: str):
            class _ContextManager:
                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc, tb):
                    return False

            return _ContextManager()

        def run(self, host: str, port: int):
            raise RuntimeError(
                "Flask is not installed. Install Flask to run the local development server."
            )

    def render_template_string(template: str) -> str:
        return template
else:
    flask_module = importlib.import_module("flask")
    Flask = flask_module.Flask
    render_template_string = flask_module.render_template_string

app = Flask(__name__)

HTML = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Alexa Marketing Playground</title>
    <style>
      :root {
        color-scheme: light dark;
        font-family: Arial, Helvetica, sans-serif;
      }
      body {
        margin: 0;
        min-height: 100vh;
        display: grid;
        place-items: center;
        background: linear-gradient(120deg, #232f3e, #00a8e1);
        color: #fff;
      }
      .card {
        text-align: center;
        background: rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 2rem;
        width: min(90vw, 700px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
      }
      h1 {
        margin-top: 0;
        font-size: clamp(1.8rem, 4vw, 3rem);
      }
      p {
        margin-bottom: 0;
        opacity: 0.9;
      }
      code {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        padding: 0.2rem 0.4rem;
      }
    </style>
  </head>
  <body>
    <main class=\"card\">
      <h1>Alexa Marketing Playground</h1>
      <p>This starter page is generated from <code>app.py</code> and deployed via GitHub Pages.</p>
      <p id=\"build-time\"></p>
    </main>
    <script>
      const now = new Date();
      document.getElementById("build-time").textContent =
        `Loaded at ${now.toLocaleString()}`;
    </script>
  </body>
</html>
"""


@app.route("/")
def home() -> str:
    return render_template_string(HTML)


def build_static(output_dir: str = "dist") -> tuple[Path, Path]:
    """Render the Flask route to static index.html files for GitHub Pages."""
    with app.test_request_context("/"):
        rendered = home()

    dist_dir = Path(output_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)

    dist_index = dist_dir / "index.html"
    dist_index.write_text(rendered, encoding="utf-8")

    root_index = Path("index.html")
    root_index.write_text(rendered, encoding="utf-8")

    nojekyll = Path(".nojekyll")
    nojekyll.write_text("", encoding="utf-8")

    return dist_index, root_index


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Alexa Marketing Playground")
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build static index.html files for GitHub Pages deployment",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    if args.build:
        dist_file, root_file = build_static()
        print(f"Built static pages: {dist_file} and {root_file}")
    else:
        app.run(host=args.host, port=args.port)
