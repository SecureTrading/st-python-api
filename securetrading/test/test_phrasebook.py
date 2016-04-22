#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
from securetrading.test import abstract_test
import securetrading


class Test_PhraseBook(abstract_test.TestCase):

    def test_lookup(self):
        tmp_phrase_book = securetrading.phrase_book
        try:
            securetrading.phrase_book = {"testing": {"de_de": "testen",
                                                     "fr_fr": "essai",
                                                     },
                                         }

            tests = [({"locale": "en_gb"},
                      {"testing": "testing", "HERE": "HERE"}),
                     ({"locale": "fr_fr"},
                      {"testing": "essai", "HERE": "HERE"}),
                     ({"locale": "de_de"},
                      {"testing": "testen", "HERE": "HERE"}),
                     ]

            for configData, expected in tests:
                config = securetrading.Config()
                for key in configData:
                    setattr(config, key, configData[key])
                phrasebook = securetrading.PhraseBook(config)
                for message in expected:
                    self.assertEquals(expected[message],
                                      phrasebook.lookup(message),
                                      )
        finally:
            securetrading.phrase_book = tmp_phrase_book

if __name__ == "__main__":
    unittest.main()
