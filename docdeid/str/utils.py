import unicodedata


def remove_nonascii(text: str) -> str:
    """\
    Removes all non-ascii characters from a string.

    :param text: a word or a phrase to process
    """
    text = str(bytes(text, encoding="ascii", errors="ignore"), encoding="ascii")
    return unicodedata.normalize("NFKD", text)


def replace_nonascii(text: str) -> str:
    """\
    Maps non-ascii characters to ascii characters.

    :param text: a word or a phrase to process
    """
    text = unicodedata.normalize("NFD", text)
    return text.encode("ascii", "ignore").decode("utf-8")


def lowercase_tail(word: str, lang: str = "nl") -> str:
    """\
    Lowercases tail of an all-caps word, keeping the first letter as is. In Dutch,
    the `IJ` digraph is considered one letter. If the word is not all-caps, returns
    it unchanged.

    :param word: the word to process
    :param lang: 2-letter language code of the current language, default: "nl"
    """
    if word.isupper():
        if lang == "nl" and word.startswith("IJ"):
            return word[0:2] + word[2:].lower()
        return word[0] + word[1:].lower()
    return word


