from __future__ import annotations

from mkdocs.config import base, config_options
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig

class _OldToNewStrings(Config):
    old_value = config_options.Type(str)
    new_value = config_options.Type(str)

class StringsMarkdownReplacementPluginConfig(Config):
    strings_replacements = config_options.ListOfItems(config_options.SubConfig(_OldToNewStrings))