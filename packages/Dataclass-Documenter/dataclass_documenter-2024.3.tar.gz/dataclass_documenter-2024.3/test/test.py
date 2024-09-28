#!/usr/bin/env python3
"""
Test dataclass documentation.
"""

import contextlib
import dataclasses
import logging
import re
import unittest
from typing import Optional


from dataclass_documenter import DataclassDocumenter


@dataclasses.dataclass
class NestedExampleDataclass:
    """
    Nested dataclass to test recursive documentation.

    Parameters:
        nested_string:
            A string parameter of the nested dataclass.

        nested_number:
            An numerical parameter of the nested dataclass
    """

    nested_string: str = "Another string value."
    nested_number: int | float = 5


@dataclasses.dataclass
class ExampleDataclass:
    """
    Brief description for example dataclass.

    This is a longer description. This dataclass is used for testing and
    generating an example in the README.

    Parameters:
        string:
            A string parameter.

        nested_dataclass:
            A nested dataclass that encapsulates its own parameters.

        integer:
            An integer parameter.

        floats:
            A list of floats.

        opt_string:
            An optional string that may be None.
    """

    string: str
    nested_dataclass: NestedExampleDataclass
    integer: int = 7
    floats: list[float] = dataclasses.field(default_factory=list)
    opt_string: Optional[str] = None
    undocumented_string: str = "Intentionally undocumented string."


EXPECTED_MARKDOWN = """\
# ExampleDataclass

Brief description for example dataclass.

This is a longer description. This dataclass is used for testing and
generating an example in the README.

## Input

~~~yaml
# Input for ExampleDataclass

# A string parameter.
# Type: str [REQUIRED]
string: ...

# A nested dataclass that encapsulates its own parameters.
nested_dataclass:
  # A string parameter of the nested dataclass.
  # Type: str [OPTIONAL]
  nested_string: Another string value.

  # An numerical parameter of the nested dataclass
  # Type: UnionType[int, float] [OPTIONAL]
  nested_number: 5

# An integer parameter.
# Type: int [OPTIONAL]
integer: 7

# A list of floats.
# Type: list[float] [OPTIONAL]
floats: []

# An optional string that may be None.
# Type: str [OPTIONAL]
opt_string: null

# Undocumented.
# Type: str [OPTIONAL]
undocumented_string: Intentionally undocumented string.

~~~

"""


@contextlib.contextmanager
def disable_logger():
    """
    Context manager for disabling a specific logger.

    Args:
        name:
            The logger name to disable.
    """
    logger = logging.getLogger("dataclass_documenter.dataclass_documenter")
    prev = logger.disabled
    logger.disabled = True
    try:
        yield None
    finally:
        logger.disabled = prev


class TestDataclassDocumenter(unittest.TestCase):
    """
    Test the DataclassDocumenter class.
    """

    def setUp(self):
        self.dado = DataclassDocumenter(ExampleDataclass)

    # This indireclty tests YAML generation.
    def test_markdown(self):
        """Markdown is correctly generated from dataclasses."""
        with disable_logger():
            self.assertEqual(self.dado.get_markdown(), EXPECTED_MARKDOWN)

    def test_markdown_level(self):
        """Markdown headers are correctly set."""
        for level in range(0, 5):
            repl = "#" * (level + 1)
            expected = re.sub(r"^#", repl, EXPECTED_MARKDOWN, count=2, flags=re.M)
            with self.subTest(level=level), disable_logger():
                self.assertEqual(self.dado.get_markdown(level=level), expected)

    def test_undocumented_warning(self):
        """Undocumented parameters create warnings."""
        expected = (
            "WARNING:dataclass_documenter.dataclass_documenter:"
            "undocumented_string is not documented in the docstring."
        )
        with self.assertLogs(level=logging.WARNING) as ctx:
            self.dado.get_markdown()
            self.assertIn(expected, ctx.output)


if __name__ == "__main__":
    unittest.main()
