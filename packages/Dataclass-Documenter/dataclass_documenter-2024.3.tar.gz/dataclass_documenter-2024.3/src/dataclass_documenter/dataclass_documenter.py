#!/usr/bin/env python3
"""Generate documented YAML files from documented dataclasses."""

import dataclasses
import functools
import logging
import textwrap

import yaml
from docstring_parser import parse as parse_docstring

from .typing import type_to_string


LOGGER = logging.getLogger(__name__)


class DataclassDocumenter:
    """Generate markdown and YAML documentation from documented dataclasses."""

    def __init__(self, datacls, name=None, width=120):
        """
        Args:
            datacls:
                The dataclass to document.

            name:
                The name to use for this class in the documentation. If None,
                the name of the dataclass will be used.

            width:
                The target output width for wrapped comments.
        """
        if not dataclasses.is_dataclass(datacls):
            raise ValueError("First argument is not a dataclass.")
        self.datacls = datacls
        self.name = datacls.__name__ if name is None else name
        self.width = int(width)

    @functools.cached_property
    def docstring(self):
        """The parsed docstring."""
        return parse_docstring(self.datacls.__doc__)

    @functools.cached_property
    def fields(self):
        """The fields of the dataclass."""
        return dataclasses.fields(self.datacls)

    def _wrap_yaml_comment(self, comment, indent):
        """
        Wrap a YAML comment.

        Args:
            comment:
                The comment to wrap.

            indent:
                The indentation for each line.

        Returns:
            The wrapped lines.
        """
        indent = f"{indent}# "
        return textwrap.wrap(
            comment, width=self.width, initial_indent=indent, subsequent_indent=indent
        )

    def _wrap_yaml_default(self, name, value, indent):
        """
        Wrap YAML output for embedding in another YAML document.

        Args:
            name:
                The field name.

            value:
                The value.

            indent:
                The indentation for each line.

        Returns:
            The wrapped YAML lines.
        """
        obj = {name: value}
        text = yaml.dump(obj)
        return textwrap.wrap(
            text, width=self.width, initial_indent=indent, subsequent_indent=indent
        )

    def get_yaml_blocks(self, level=0, header=None):
        """
        Get commented YAML input for the dataclass.

        Args:
            level:
                The indentation level.

        Returns:
            A generator over blocks of YAML.
        """
        docstring = self.docstring
        params = {param.arg_name: param for param in docstring.params}
        indent = "  " * level
        if header is not None:
            yield from self._wrap_yaml_comment(header, indent)
            yield ""
        for field in self.fields:
            try:
                doc = params[field.name].description
            except KeyError:
                LOGGER.warning("%s is not documented in the docstring.", field.name)
                doc = "Undocumented."
            yield from self._wrap_yaml_comment(doc, indent)

            # Recursively document dataclasses.
            if dataclasses.is_dataclass(field.type):
                yield f"{indent}{field.name}:"
                dado = self.__class__(field.type)
                yield from dado.get_yaml_blocks(level=level + 1)
                continue

            meta = f"{indent}# Type: {type_to_string(field.type)}"
            if field.default is dataclasses.MISSING:
                if field.default_factory is dataclasses.MISSING:
                    yield f"{meta} [REQUIRED]"
                    yield f"{indent}{field.name}: ..."
                else:
                    yield f"{meta} [OPTIONAL]"
                    default = field.default_factory()
                    yield from self._wrap_yaml_default(field.name, default, indent)
            else:
                yield f"{meta} [OPTIONAL]"
                yield from self._wrap_yaml_default(field.name, field.default, indent)
            yield ""

    def get_yaml(self, level=0):
        """
        Get commented YAML input for the dataclass.
        """
        header = f"Input for {self.name}"
        return "\n".join(self.get_yaml_blocks(level=level, header=header))

    def get_markdown(self, level=0):
        """
        Get a markdown description of the datacalss that contains commented example YAML input file.

        Args:
            level:
                Markdown header level for the returned markdown.

        Returns:
            The markdown string.
        """
        level = max(level + 1, 1)
        header_prefix = "#" * level

        docstring = parse_docstring(self.datacls.__doc__)
        cls_desc = (docstring.short_description, docstring.long_description)
        cls_desc = [desc for desc in cls_desc if desc]
        if cls_desc:
            cls_desc = "\n\n".join(cls_desc)
        if not cls_desc:
            LOGGER.warning("No class description for %s", self.datacls.__name__)
            cls_desc = "No description available."

        return f"""{header_prefix} {self.name}

{cls_desc}

{header_prefix}# Input

~~~yaml
{self.get_yaml()}
~~~

"""
