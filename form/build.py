"""Build the single-file Sports Money DNA form with the BWB logos inlined.

Usage: python3 form/build.py   ->   writes form/sports-money-dna.html
"""
import base64
import pathlib

root = pathlib.Path(__file__).resolve().parent
brand = root.parent / "brand"


def data_uri(name: str) -> str:
    return "data:image/png;base64," + base64.b64encode((brand / name).read_bytes()).decode()


html = (root / "src" / "money-dna.html").read_text()
html = html.replace("{{LOGO_FULL}}", data_uri("bwb-logo-full-web.png"))
html = html.replace("{{LOGO_WORDMARK}}", data_uri("bwb-wordmark-web.png"))
(root / "sports-money-dna.html").write_text(html)
print("built", root / "sports-money-dna.html", f"{len(html)//1024} KB")
