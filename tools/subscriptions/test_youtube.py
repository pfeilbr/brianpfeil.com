import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import youtube  # noqa: E402

SAMPLE = '''# header
total: 2
combined_subscribers: "5M"

categories:
  - key: code
    count: 1
  - key: food
    count: 1

channels:
  - name: "Say \\"hi\\""
    handle: "@hi"
    cat: code
    subs: "4.2M"
    uploads: "UUaaaaaaaaaaaaaaaaaaaaaa"
    avatar: "/subscriptions/avatars/hi.jpg"
  - name: "Cook"
    handle: "@cook"
    cat: food
    subs: "800K"
    uploads: "UUbbbbbbbbbbbbbbbbbbbbbb"
    avatar: "/subscriptions/avatars/cook.jpg"
'''


class YoutubeTest(unittest.TestCase):
    def test_roundtrip_is_byte_identical(self):
        head, cats, channels = youtube.parse(SAMPLE)
        self.assertEqual(channels[0]["name"], 'Say "hi"')
        self.assertEqual(youtube.render(head, cats, channels), SAMPLE)

    def test_live_file_roundtrips(self):
        text = youtube.DATA.read_text()
        self.assertEqual(youtube.render(*youtube.parse(text)), text)

    def test_render_recounts(self):
        head, cats, channels = youtube.parse(SAMPLE)
        channels[1]["cat"] = "code"
        out = youtube.render(head, cats, channels)
        self.assertIn("  - key: code\n    count: 2\n", out)
        self.assertIn("  - key: food\n    count: 0\n", out)
        self.assertIn('combined_subscribers: "5M"', out)

    def test_parse_channel_page_reads_header_not_featured(self):
        page = (
            '<meta property="og:title" content="Fire &amp; Ship ">'
            '<meta property="og:image" content="https://yt3.example/abc=s900-c-k-c0x00ffffff-no-rj">'
            '"subscriberCountText":{"simpleText":"464K subscribers"}'
            '"canonicalBaseUrl":"/@Fireship"'
            '{"metadataParts":[{"text":{"content":"4.29M subscribers"}}]}'
        )
        info = youtube.parse_channel_page(page, "UCx")
        self.assertEqual(info["name"], "Fire & Ship")
        self.assertEqual(info["handle"], "@Fireship")
        self.assertEqual(info["subs"], "4.29M")
        self.assertTrue(info["avatar_url"].endswith("=s96-c-k-c0x00ffffff-no-rj"))

    def test_slug(self):
        self.assertEqual(youtube.slug("Adam Marczak - Azure for Everyone"), "adam-marczak-azure-for-everyone")
        self.assertEqual(youtube.slug("李子柒 Liziqi"), "liziqi")


if __name__ == "__main__":
    unittest.main()
