from html.parser import HTMLParser
from pathlib import Path
import re
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


def parse_styles():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    style_match = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
    if not style_match:
        return {}

    rules = {}
    for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", style_match.group(1)):
        declarations = {}
        for declaration in body.split(";"):
            if ":" not in declaration:
                continue
            name, value = declaration.split(":", 1)
            declarations[name.strip()] = value.strip()
        for selector in selectors.split(","):
            rules.setdefault(selector.strip(), {}).update(declarations)
    return rules


def px(value):
    return float(value.removesuffix("px"))


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

    def test_four_buttons_stay_on_one_row_in_a_narrow_notion_embed(self):
        styles = parse_styles()
        list_style = styles[".social-links"]
        button_style = styles[".social-link"]
        body_style = styles["body"]

        button_width = px(button_style["width"])
        gap = px(list_style["gap"])
        horizontal_padding = px(body_style["padding"])
        required_width = (4 * button_width) + (3 * gap) + (2 * horizontal_padding)

        self.assertEqual("nowrap", list_style.get("flex-wrap"))
        self.assertLessEqual(required_width, 220)

    def test_embed_canvas_is_transparent_and_centers_content_in_both_directions(self):
        styles = parse_styles()

        self.assertEqual("transparent", styles["html"].get("background"))
        self.assertEqual("transparent", styles["body"].get("background"))
        self.assertEqual("100%", styles["html"].get("height"))
        self.assertEqual("100%", styles["body"].get("min-height"))
        self.assertEqual("center", styles["body"].get("justify-content"))
        self.assertEqual("center", styles["body"].get("align-items"))

    def test_icons_and_buttons_use_the_compact_size(self):
        styles = parse_styles()

        self.assertLessEqual(px(styles[".social-link"]["width"]), 40)
        self.assertLessEqual(px(styles[".social-link"]["height"]), 40)
        self.assertLessEqual(px(styles[".social-link svg"]["width"]), 18)
        self.assertLessEqual(px(styles[".social-link svg"]["height"]), 18)


if __name__ == "__main__":
    unittest.main()
