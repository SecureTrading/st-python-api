from __future__ import unicode_literals
import securetrading


class PhraseBook(object):

    """Secure Trading language phrasebook module.

    This class will translate phrases to various languages.
"""

    def __init__(self, config):
        """Initialises the PhraseBook.

        This method will initialise the Secure Trading phrasebook
module, which can translate phrases using the locale specified in the
config that was passed in.

        Args:
           config:  A securetrading.config object containing
the locale information.

        Usage:
           >>> import securetrading
           >>> phrase_book = securetrading.PhraseBook(st_config)
        """
        self.config = config
        super(PhraseBook, self).__init__()

    def lookup(self, english, locale=None):
        """Retrieves the locale translation for an English message.

        This method will translate an English phrase, to either a passed
in locale or to the specified locale in the config passed
in on initialisation.

        Args:
           english: [string] The messsage to retrieve the translation for.
           locale: (optional[string]) The locale to translate the messsage
into. See the config.py documentation for more details.

        Returns:
           A string representing the translated message.

        Usage:
           >>> translated = phrase_book.lookup("message")
           or
           >>> translated = phrase_book.lookup("message", locale=new_locale)
        """
        if locale is None:
            locale = self.config.locale
        mapping = securetrading.phrase_book.get(english, {"en_gb": english})
        return mapping.get(locale, english)
