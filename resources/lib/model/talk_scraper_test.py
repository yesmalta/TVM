import unittest
import talk_scraper
import test_util
import timeit


class TestTalkScraper(unittest.TestCase):

    def test_get_ted_video(self):
        self.assert_talk_details("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html", "http://download.ted.com/talks/ArielGarten_2011X-320k.mp4?apikey=489b859150fc58263f17110eeb44ed5fba4a3b22", "Know thyself, with a brain scanner", "Ariel Garten", True, True)
        self.assert_talk_details("http://www.ted.com/talks/tom_shannon_s_magnetic_sculpture.html", "http://download.ted.com/talks/TomShannon_2003-320k.mp4?apikey=489b859150fc58263f17110eeb44ed5fba4a3b22", "Anti-gravity sculpture", "Tom Shannon", True, True);

    def test_get_youtube_video(self):
        self.assert_talk_details("http://www.ted.com/talks/bjarke_ingels_hedonistic_sustainability.html", "plugin://plugin.video.youtube/?action=play_video&videoid=ogXT_CI7KRU", "Hedonistic sustainability", "Bjarke Ingels", False, True)

    def test_get_vimeo_video(self):
        self.assert_talk_details("http://www.ted.com/talks/seth_godin_this_is_broken_1.html", "plugin://plugin.video.vimeo?action=play_video&videoid=4246943", "This is broken", "Seth Godin", True, False)

    def assert_talk_details(self, talk_url, expected_video_url, expected_title, expected_speaker, expect_plot, expect_json):
        video_url, title, speaker, plot, talk_json = talk_scraper.get(test_util.get_HTML(talk_url))
        self.assertEqual(expected_video_url, video_url)
        self.assertEqual(expected_title, title)
        self.assertEqual(expected_speaker, speaker)

        if (expect_plot):
            self.assertTrue(plot)  # Not None or empty
        else:
            self.assertIsNone(plot)

        if expect_json:
            self.assertTrue(talk_json)  # Not None or empty
        else:
            self.assertIsNone(talk_json)

    def test_get_custom_quality_video(self):
        html = test_util.get_HTML("http://www.ted.com/talks/edith_widder_how_we_found_the_giant_squid.html")
        # Note not customized. Should be a useful fallback if this code goes haywire.
        self.assert_custom_quality_url(html, "320kbps", "http://download.ted.com/talks/EdithWidder_2013-320k.mp4?apikey=489b859150fc58263f17110eeb44ed5fba4a3b22")

        self.assert_custom_quality_url(html, "64kbps", "http://download.ted.com/talks/EdithWidder_2013-64k.mp4?apikey=489b859150fc58263f17110eeb44ed5fba4a3b22")
        self.assert_custom_quality_url(html, "180kbps", "http://download.ted.com/talks/EdithWidder_2013-180k.mp4?apikey=489b859150fc58263f17110eeb44ed5fba4a3b22")
        self.assert_custom_quality_url(html, "450kbps", "http://download.ted.com/talks/EdithWidder_2013-450k.mp4?apikey=489b859150fc58263f17110eeb44ed5fba4a3b22")
        self.assert_custom_quality_url(html, "600kbps", "http://download.ted.com/talks/EdithWidder_2013-600k.mp4?apikey=489b859150fc58263f17110eeb44ed5fba4a3b22")
        self.assert_custom_quality_url(html, "950kbps", "http://download.ted.com/talks/EdithWidder_2013-950k.mp4?apikey=489b859150fc58263f17110eeb44ed5fba4a3b22")
        self.assert_custom_quality_url(html, "1500kbps", "http://download.ted.com/talks/EdithWidder_2013-1500k.mp4?apikey=489b859150fc58263f17110eeb44ed5fba4a3b22")

        # Fall back to standard URL when custom URL 404s
        self.assert_custom_quality_url(html, "42kbps", "http://download.ted.com/talks/EdithWidder_2013-320k.mp4?apikey=489b859150fc58263f17110eeb44ed5fba4a3b22")

    def assert_custom_quality_url(self, talk_html, video_quality, expected_video_url):
        video_url, title, speaker, plot, talk_json = talk_scraper.get(talk_html, video_quality)
        self.assertEqual(expected_video_url, video_url)

    def test_performance(self):
        html = test_util.get_HTML("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html")

        def test():
            talk_scraper.get(html);

        t = timeit.Timer(test)
        repeats = 10
        time = t.timeit(repeats)
        print "Extracting talk details took %s seconds per run" % (time / repeats)
        self.assertGreater(4, time)

