import re
import aiofiles
from typing import List, Tuple
from log.logger_config import get_logger
logger = get_logger(__name__)

class FileContentManager:
    @staticmethod
    async def read_file(file_path: str) -> str:
        """Read the content of the file asynchronously."""
        try:
            async with aiofiles.open(file_path, 'r') as file:
                content = await file.read()
            logger.info(f"Successfully read file {file_path}")
            return content
        except Exception as e:
            logger.error(f"Error reading file {file_path}. Error: {e}")
            return ""

    @staticmethod
    async def write_file(file_path: str, content: str):
        """Write content to the file asynchronously."""
        try:
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(content)
            logger.info(f"File {file_path} has been successfully updated.")
        except Exception as e:
            logger.error(f"Error writing to file {file_path}. Error: {e}")

    @staticmethod
    def parse_search_replace_blocks(response: str) -> List[Tuple[str, str]]:
        """
        Parses a response string for single or multiple SEARCH/REPLACE blocks,
        returning search and replace content as tuples. Handles both cases correctly.
        """
        # Regular expression pattern to capture multiple SEARCH/REPLACE blocks
        pattern = r'<<<<< SEARCH\n(.*?)=======\n(.*?)>>>>>>> REPLACE'

        # Find all matches in the response
        matches = re.findall(pattern, response, re.DOTALL)

        # Raise an error if no blocks are found
        if not matches:
            raise ValueError("No valid SEARCH/REPLACE blocks found in the input.")

        blocks = []
        for search, replace in matches:
            # Strip any extra spaces or newlines for cleanliness
            search = search.strip()
            replace = replace.strip()

            # Append the search and replace blocks as a tuple
            blocks.append((search, replace))

        return blocks


    @classmethod
    async def apply_changes(cls, file_path: str, blocks: List[Tuple[str, str]]) -> str:
        """Apply the changes from SEARCH/REPLACE blocks to the file content."""
        content = await cls.read_file(file_path)
        for search, replace in blocks:
            if search:
                content = content.replace(search, replace)
            else:
                content += f"\n\n{replace}"
        logger.info(f"Successfully applied changes to content of {file_path}")
        return content

    @classmethod
    async def process_ai_response(cls, file_path: str, ai_response: str):
        """Process the AI response and automatically apply changes to the file."""
        blocks = cls.parse_search_replace_blocks(ai_response)
        if not blocks:
            logger.warning(f"No valid SEARCH/REPLACE blocks found in the AI response for {file_path} {blocks}")
            return

        new_content = await cls.apply_changes(file_path, blocks)
        await cls.write_file(file_path, new_content)
        logger.info(f"Changes have been automatically applied to {file_path}")

    @classmethod
    async def handle_ai_response(cls, file_path: str, ai_response: str):
        """Main method to handle AI responses and automatically manage code changes for a single file."""
        try:
            await cls.process_ai_response(file_path, ai_response)
            logger.info(f"Successfully handled AI response for {file_path}")
        except Exception as e:
            logger.error(f"Error processing AI response for {file_path}: {e}")
