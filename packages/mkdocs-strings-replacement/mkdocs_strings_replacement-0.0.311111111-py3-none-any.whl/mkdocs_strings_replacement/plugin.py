from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs_strings_replacement.config import StringsMarkdownReplacementPluginConfig
from mkdocs_strings_replacement.logger import logger

class StringsMarkdownReplacementPlugin(BasePlugin[StringsMarkdownReplacementPluginConfig]):
    
    def on_page_markdown(
        self,
        markdown: str,
        config: MkDocsConfig,
    ) -> str:
        try:
            updated_markdown = markdown 

            for replacement_pair in self.config.strings_replacements:
                old_value = replacement_pair.old_value
                new_value = replacement_pair.new_value
                
                logger.info(f"Replacing: '{old_value}', with: '{new_value}'")
                
                updated_markdown = updated_markdown.replace(old_value, new_value)

            return updated_markdown
        except Exception as exception:
            raise PluginError(f"An error occurred during markdown processing: '{exception}'")