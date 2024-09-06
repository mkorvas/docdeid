import unicodedata
from itertools import filterfalse


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


def drop_accents(text: str) -> str:
    """\
    Drops any accents from characters of the input text.

    :param text: a word or a phrase to process
    """
    decomposed = unicodedata.normalize("NFD", text)
    wo_accents = filterfalse(unicodedata.combining, decomposed)
    return ''.join(wo_accents)


def lowercase_tail(word: str,
                   lang: str = "nl",
                   keep_mixed: bool = True) -> str:
    """\
    Lowercases tail of an all-caps word, keeping the first letter as is. In Dutch,
    the `IJ` digraph is considered one letter. If the word is not all-caps, returns
    it unchanged by default.

    :param word: the word to process
    :param lang: 2-letter language code of the current language, default: "nl"
    :param keep_mixed: should mixed-case tokens be kept untouched?
    """
    if not keep_mixed or word.isupper():
        if lang == "nl" and word.startswith("IJ"):
            return word[0:2] + word[2:].lower()
        return word[0] + word[1:].lower()
    return word


