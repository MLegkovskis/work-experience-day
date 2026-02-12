from __future__ import annotations

from pathlib import Path

try:
    from flask import Flask, render_template_string
except ModuleNotFoundError:  # fallback for restricted offline environments
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


def build_static(output_dir: str = "dist") -> Path:
    """Render the Flask route to a static index.html for GitHub Pages."""
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    with app.test_request_context("/"):
        rendered = home()

    output_file = target_dir / "index.html"
    output_file.write_text(rendered, encoding="utf-8")
    return output_file


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Alexa Marketing Playground")
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build a static dist/index.html for GitHub Pages deployment",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    if args.build:
        output = build_static()
        print(f"Built static page: {output}")
    else:
        app.run(host=args.host, port=args.port)
