class WordList:
    """Searchable list of words from a file.

    This isn't Boggle-specific (you could use it for Scrabble or other word
    games), so there's no Boggle-specific logic in it.
    """

    def __init__(self, dict_path="dictionary.txt"):
        """Create a word list from a dictionary file on disk.

            >>> wl = WordList("test_dictionary.txt")
            >>> wl.words == {'CAT', 'DOG'}
            True
        """

        self.words = self._read_dict(dict_path)

    def __repr__(self):
        return f"<WordList len={len(self.words)}>"

    def _read_dict(self, dict_path):
        """Read dictionary file at dict_path and return set of words."""

        dict_file = open(dict_path)
        words = {w.strip().upper() for w in dict_file}
        dict_file.close()

        return words

    def check_word(self, word):
        """Is word in word list?

        Checks if a word is in the word list
        >>> wl = WordList("dictionary.txt")
        >>> wl.check_word("ALBUMS")
        True

        Lookups must be in ALL CAPS!
        >>> wl.check_word("albums")
        False

        Apparently this isn't in the dictionary
        >>> wl.check_word("AARDVARK")
        False
        """

        return word in self.words


english_words = WordList("dictionary.txt")
