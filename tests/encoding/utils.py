from unittest import TestCase

from shobdokutir.encoding.utils import bijoy2unicode, unicode2bijoy

class TestUtils(TestCase):

    def test_bijoy2unicode_and_unicode2bijoy(self):
        bijoy_texts = ""
        unicode_texts = ""
        with open("resources/sample_docs/bijoy_sample.txt") as f_bijoy:
            for a_line in f_bijoy:
                bijoy_texts += a_line
        with open("resources/sample_docs/unicode_sample.txt", encoding="utf-8") as f_unicode:
            for a_line in f_unicode:
                unicode_texts += a_line
    
        self.assertTrue(bijoy2unicode(bijoy_texts) == unicode_texts)
        # self.assertTrue(unicode2bijoy(unicode_texts) == bijoy_texts)
