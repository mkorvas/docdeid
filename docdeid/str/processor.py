import re
from abc import ABC, abstractmethod
from typing import Iterable

from docdeid.str.utils import (drop_accents,
                               lowercase_tail,
                               remove_nonascii,
                               replace_nonascii)


class StringProcessor(ABC):
    """Abstract class for string processing."""

    @abstractmethod
    def process_items(self, items: Iterable[str]) -> list[str]:
        """
        Process an iterable of strings.

        Args:
            items: The input items.

        Returns:
            The processed items.
        """

    def __repr__(self) -> str:
        return (
            self.__class__.__name__
            + "("
            + ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
            + ")"
        )


class StringModifier(StringProcessor, ABC):
    """Modifies strings."""

    @abstractmethod
    def process(self, item: str) -> str:
        """
        Processes a string by modifying it.

        Args:
            item: The input string.

        Returns:
            The output string.
        """

    def process_items(self, items: Iterable[str]) -> list[str]:
        return [self.process(item) for item in items]


class StringFilter(StringProcessor, ABC):
    """Filters strings."""

    @abstractmethod
    def filter(self, item: str) -> bool:
        """
        Filters strings.

        Args:
            item: The input string.

        Returns:
            ``True`` to keep the item, ``False`` to remove it (same as
            ``filter`` builtin).
        """

    def process_items(self, items: Iterable[str]) -> list[str]:
        return [item for item in items if self.filter(item)]


class LowercaseString(StringModifier):
    """Lowercase a string."""

    def process(self, item: str) -> str:
        return item.casefold()


_WORD_RX = re.compile("\\w+", re.U)


class LowercaseTail(StringModifier):
    """Lowercases the tail of all-caps words."""

    def __init__(self, lang: str = "nl") -> None:
        self._lang = lang

    def _process_word_match(self, match: re.Match) -> str:
        return lowercase_tail(match.group(0), self._lang)

    def process(self, item: str) -> str:
        return _WORD_RX.sub(self._process_word_match, item)


class StripString(StringModifier):
    """
    Strip string (whitespaces, tabs, newlines, etc.

    at start/end).
    """

    def process(self, item: str) -> str:
        return item.strip()


class RemoveNonAsciiCharacters(StringModifier):
    """
    Removes non-ascii characters from a string.

    E.g.: Renée -> Rene.
    """

    def process(self, item: str) -> str:
        return remove_nonascii(item)


class ReplaceNonAsciiCharacters(StringModifier):
    """
    Maps non-ascii characters to ascii characters.

    E.g.: Renée -> Renee. It's advised to test this before using as mapping can be
    tricky in practice for some characters.
    """

    def process(self, item: str) -> str:
        return replace_nonascii(item)


class DropAccents(StringModifier):
    """\
    Drops any accents from characters of the input text.

    E.g.: "Renée" -> "Renee" but "μL" -> "μL".
    """

    def process(self, item: str) -> str:
        return drop_accents(item)


class ReplaceValue(StringModifier):
    """
    Replaces a value in a string, literally.

    Args:
        find_value: The value to be replaced.
        replace_value: The value to replace with.
    """

    def __init__(self, find_value: str, replace_value: str) -> None:
        self.find_value = find_value
        self.replace_value = replace_value

    def process(self, item: str) -> str:
        return item.replace(self.find_value, self.replace_value)


class ReplaceValueRegexp(StringModifier):
    """
    Replace a value in a string with regexp.

    Args:
        find_value: The input regexp.
        replace_value: The value to replace it with.
    """

    def __init__(self, find_value: str, replace_value: str) -> None:
        self.find_value = find_value
        self.replace_value = replace_value

    def process(self, item: str) -> str:
        return re.sub(self.find_value, self.replace_value, item)


class FilterByLength(StringFilter):
    """
    Filter by length.

    Args:
        min_len: The minimum length. Strings shorter than this will be filtered out.
    """

    def __init__(self, min_len: int) -> None:
        self.min_len = min_len

    def filter(self, item: str) -> bool:
        return len(item) >= self.min_len
