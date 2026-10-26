from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_LINKS = {
    "官網": "https://lupinvisual.com/",
    "Facebook": "https://www.facebook.com/profile.php?id=61582371620174",
    "Threads": "https://www.threads.com/@lupin_visual",
    "Email": "mailto:lupinart1008@gmail.com",
}


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_link = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a":
            self.current_link = {"attrs": attributes, "svg_count": 0, "text": ""}
            self.links.append(self.current_link)
        elif tag == "svg" and self.current_link is not None:
            self.current_link["svg_count"] += 1
            self.current_link["svg_attrs"] = attributes

    def handle_endtag(self, tag):
        if tag == "a":
            self.current_link = None

    def handle_data(self, data):
        if self.current_link is not None:
            self.current_link["text"] += data


def parse_widget():
    parser = LinkParser()
    widget = ROOT / "index.html"
    if not widget.exists():
        return []
    parser.feed(widget.read_text(encoding="utf-8"))
    return parser.links


class WidgetContractTests(unittest.TestCase):
    def test_exposes_the_four_requested_destinations(self):
        links = parse_widget()
        actual = {
            link["attrs"].get("aria-label"): link["attrs"].get("href")
            for link in links
        }
        self.assertEqual(EXPECTED_LINKS, actual)

    def test_each_link_has_an_accessible_inline_icon(self):
        links = parse_widget()
        self.assertEqual(4, len(links))
        for link in links:
            with self.subTest(link=link["attrs"].get("aria-label")):
                self.assertEqual(1, link["svg_count"])
                self.assertEqual("true", link["svg_attrs"].get("aria-hidden"))

    def test_buttons_are_icon_only(self):
        links = parse_widget()
        self.assertEqual(4, len(links))
        for link in links:
            with self.subTest(link=link["attrs"].get("aria-label")):
                self.assertEqual("", link["text"].strip())

    def test_links_escape_the_notion_embed_safely(self):
        links = parse_widget()
        self.assertEqual(4, len(links))
        for link in links:
            with self.subTest(link=link["attrs"].get("aria-label")):
                self.assertEqual("_blank", link["attrs"].get("target"))
                rel = set(link["attrs"].get("rel", "").split())
                self.assertTrue({"noopener", "noreferrer"}.issubset(rel))


if __name__ == "__main__":
    unittest.main()
