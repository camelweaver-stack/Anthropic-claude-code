#!/usr/bin/env python3
"""Tests for the northfwliving production validators.

Run with:  python3 -m unittest discover northfwliving-scripts/tests
(or `python3 northfwliving-scripts/tests/test_validators.py`)

Fixtures are generated in a temp directory at runtime — nothing here is ever
part of the deployable site, so no fixture content can leak into production.
"""
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import validate_credibility as vc
import validate_technical as vt

HEAD = (
    '<meta name="description" content="A page.">'
    '<link rel="canonical" href="https://northfwliving.com/{path}">'
    '<link rel="alternate" hreflang="en" href="https://northfwliving.com/{path}">'
    '<link rel="alternate" hreflang="es" href="https://northfwliving.com/es/{path}">'
    '<link rel="alternate" hreflang="x-default" href="https://northfwliving.com/{path}">'
)


def page(title="A page", body="Hello corridor.", lang="en", path=""):
    return (
        f'<!DOCTYPE html><html lang="{lang}"><head><title>{title}</title>'
        + HEAD.format(path=path)
        + f"</head><body>{body}</body></html>"
    )


class SiteFixture(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.root)

    def write(self, rel, content):
        p = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)

    def sitemap_for(self, rels):
        locs = "".join(
            f"<loc>https://northfwliving.com/{r[:-len('index.html')] if r.endswith('index.html') else r}</loc>"
            for r in rels
        )
        self.write("sitemap.xml", f"<urlset>{locs}</urlset>")


class TestCredibilityValidator(SiteFixture):
    def test_clean_page_passes(self):
        self.write("index.html", page())
        self.assertEqual(vc.main(self.root), 0)

    def test_todo_copy_fails(self):
        self.write("index.html", page(body="<p>TODO: verify this rate</p>"))
        self.assertEqual(vc.main(self.root), 1)

    def test_spanish_todo_is_not_a_violation(self):
        self.write("es/index.html", page(lang="es", body="<p>sobre todo: el techo. Lo organizan todo: bien.</p>"))
        self.assertEqual(vc.main(self.root), 0)

    def test_fake_field_note_fails(self):
        self.write("index.html", page(body="<p>FIELD NOTE: we drove the loop at 7am</p>"))
        self.assertEqual(vc.main(self.root), 1)

    def test_branded_field_notes_heading_passes(self):
        self.write("index.html", page(body="<h2>Latest field notes</h2>"))
        self.assertEqual(vc.main(self.root), 0)

    def test_future_visit_placeholder_fails(self):
        self.write("index.html", page(body="<p>Photos added after an in-person visit.</p>"))
        self.assertEqual(vc.main(self.root), 1)

    def test_placeholder_copy_fails(self):
        self.write("index.html", page(body="<p>PLACEHOLDER — write intro</p>"))
        self.assertEqual(vc.main(self.root), 1)

    def test_placeholder_attribute_is_fine(self):
        self.write("index.html", page(body='<input placeholder="e.g., spring 2027">'))
        self.assertEqual(vc.main(self.root), 0)

    def test_insert_marker_fails(self):
        self.write("index.html", page(body="<p>[INSERT rate table]</p>"))
        self.assertEqual(vc.main(self.root), 1)

    def test_add_photo_marker_fails(self):
        self.write("index.html", page(body="<p>[ADD PHOTO of the model home]</p>"))
        self.assertEqual(vc.main(self.root), 1)

    def test_firsthand_claim_marker_fails(self):
        self.write("index.html", page(body="<p>FIRST-HAND observation from our team</p>"))
        self.assertEqual(vc.main(self.root), 1)

    def test_lorem_ipsum_fails(self):
        self.write("index.html", page(body="<p>Lorem ipsum dolor sit amet</p>"))
        self.assertEqual(vc.main(self.root), 1)

    def test_violation_in_meta_description_fails(self):
        bad = page().replace('content="A page."', 'content="TODO: write description"')
        self.write("index.html", bad)
        self.assertEqual(vc.main(self.root), 1)

    def test_violation_in_alt_text_fails(self):
        self.write("index.html", page(body='<img src="/x.jpg" alt="PLACEHOLDER photo">'))
        self.assertEqual(vc.main(self.root), 1)

    def test_script_content_is_ignored(self):
        self.write("index.html", page(body="<script>// TODO: refactor later</script><p>fine</p>"))
        self.assertEqual(vc.main(self.root), 0)


class TestTechnicalValidator(SiteFixture):
    def clean_site(self):
        self.write("index.html", page(path=""))
        self.write("es/index.html", page(title="Página", lang="es", path="es/"))
        self.sitemap_for(["index.html", "es/index.html"])

    def test_clean_site_passes(self):
        self.clean_site()
        self.assertEqual(vt.main(self.root), 0)

    def test_missing_canonical_fails(self):
        self.clean_site()
        self.write("index.html", page(path="").replace('rel="canonical"', 'rel="canonicalX"'))
        self.assertEqual(vt.main(self.root), 1)

    def test_wrong_canonical_fails(self):
        self.clean_site()
        self.write(
            "index.html",
            page(path="").replace(
                'canonical" href="https://northfwliving.com/"',
                'canonical" href="https://northfwliving.com/other/"',
            ),
        )
        self.assertEqual(vt.main(self.root), 1)

    def test_incomplete_hreflang_fails(self):
        self.clean_site()
        self.write("index.html", page(path="").replace('hreflang="x-default"', 'hreflang="fr"'))
        self.assertEqual(vt.main(self.root), 1)

    def test_wrong_lang_attr_on_es_page_fails(self):
        self.clean_site()
        self.write("es/index.html", page(title="Página", lang="en", path="es/"))
        self.assertEqual(vt.main(self.root), 1)

    def test_noindex_fails(self):
        self.clean_site()
        bad = page(path="").replace("</title>", '</title><meta name="robots" content="noindex">')
        self.write("index.html", bad)
        self.assertEqual(vt.main(self.root), 1)

    def test_duplicate_titles_fail(self):
        self.clean_site()
        self.write("es/index.html", page(title="A page", lang="es", path="es/"))
        self.assertEqual(vt.main(self.root), 1)

    def test_broken_internal_link_fails(self):
        self.clean_site()
        self.write("index.html", page(path="", body='<a href="/nowhere/">x</a>'))
        self.assertEqual(vt.main(self.root), 1)

    def test_page_missing_from_sitemap_fails(self):
        self.clean_site()
        self.write("extra/index.html", page(title="Extra", path="extra/"))
        self.assertEqual(vt.main(self.root), 1)

    def test_sitemap_entry_without_file_fails(self):
        self.clean_site()
        self.sitemap_for(["index.html", "es/index.html", "ghost/index.html"])
        self.assertEqual(vt.main(self.root), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
