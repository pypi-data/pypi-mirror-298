import os
import sys
import asyncio
from datetime import datetime
import aiohttp
import json
import re
from json_repair import repair_json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class CodingAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway('bedrock')

    def get_current_time_formatted(self):
        """Return the current time formatted as mm/dd/yy."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%m/%d/%y")
        return formatted_time

    def initial_setup(self, context_files, instructions, context, role, crawl_logs):
        """Initialize the setup with the provided instructions and context."""

        prompt = f"""You are a senior software engineer working as a coding agent. You will receive detailed instructions to work on. Follow these guidelines strictly:
                **Response Guidelines:**
                1. For ALL code changes, additions, or deletions, you MUST ALWAYS use the following *SEARCH/REPLACE block* format:

                   <<<<<<< SEARCH
                   [Existing code to be replaced, if any]
                   =======
                   [New or modified code]
                   >>>>>>> REPLACE

                2. For new code additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New code to be added]
                   >>>>>>> REPLACE

                3. Ensure that the SEARCH section exactly matches the existing code, including whitespace and comments.

                4. For large files, focus on the relevant sections. Use comments to indicate skipped portions:
                   // ... existing code ...

                5. For complex changes or large files, break them into multiple SEARCH/REPLACE blocks.

                6. CRITICAL: NEVER provide code snippets, suggestions, or examples outside of the SEARCH/REPLACE block format. ALL code must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a user's request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                Remember, your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.
        """

        self.conversation_history = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"These are your instructions: {instructions}"},
            {"role": "assistant", "content": "Got it! I'll proceed with the given instructions."},
            {"role": "user", "content": f"Current context: {context}"},
            {"role": "assistant", "content": "Understood. I'm ready to receive instructions."},
        ]


        if context_files:
            all_file_contents = ""

            for file_path in context_files:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

            self.conversation_history.append({"role": "user", "content": f"These are all the supported files to provide enough context for this task: {all_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Got it!"})

        if crawl_logs:
            self.conversation_history.append({"role": "user", "content": f"This task requires you to scrape data. Here is the provided data: {crawl_logs}"})
            self.conversation_history.append({"role": "assistant", "content": "Got it!"})


    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file.
        """
        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.info(f"Failed to read file {file_path} with {encoding} encoding: {e}")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.context(f"Failed to read file {file_path} in binary mode: {e}")

        return None

        # Start of Selection

    async def get_coding_request(self, is_first, file, techStack):
            """
            Get coding response for the given instruction and context from Azure OpenAI.

            Args:
                session (aiohttp.ClientSession): The aiohttp session to use for the request.
                is_first (bool): Flag to indicate if it's the first request.
                prompt (str): The coding task prompt.
                file (str): Name of the file to work on.
                techStack (str): The technology stack for which the code should be written.

            Returns:
                dict: The code response or error reason.
            """

            user_prompt = (
                f"{'Begin' if is_first else 'Continue'} implementing the following task on {file}:\n"
                f"Strictly follow {techStack} syntax, best practices, and design patterns. Ensure code is idiomatic and leverages language-specific features effectively.\n"
                f"Your response must exclusively contain SEARCH/REPLACE blocks for code changes. Provide complete implementations, not placeholders. Do not include any other content outside these blocks."
            )

            if self.conversation_history and self.conversation_history[-1]["role"] == "user":
                self.conversation_history.append({"role": "assistant", "content": ""})

            self.conversation_history.append({"role": "user", "content": user_prompt})

            try:
                response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
                self.conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
                return response.choices[0].message.content
            except Exception as e:
                logger.info(f"Failed: {e}")
                return {
                    "reason": str(e)
                }


    async def get_coding_requests(self, is_first, file, techStack):
        """
        Get coding responses for a list of files from Azure OpenAI based on user instruction.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            prompt (str): The coding task prompt.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.

        Returns:
            dict: The code response or error reason.
        """
        return await self.get_coding_request(is_first, file, techStack)

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
