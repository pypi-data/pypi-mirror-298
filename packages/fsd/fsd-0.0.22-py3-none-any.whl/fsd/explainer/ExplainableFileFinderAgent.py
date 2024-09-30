import os
import aiohttp
import asyncio
import json
import sys
from json_repair import repair_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)
class ExplainableFileFinderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

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

    async def get_file_planning(self, idea):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            idea (str): The general plan idea.
            all_file_contents (str): The project structure.

        Returns:
            dict: JSON response with the plan.
        """
        all_file_contents = self.repo.print_tree()
        prompt = (
            f"From the provided user prompt, build a JSON to list all working_files to be used. Provide only a JSON response without any additional text or Markdown formatting. "
            f"Working_files must include the full path of files that may be helpful to provide enough context to answer user request. "
            f"Current working project is {self.repo.get_repo_path()}. "
            f"Use this JSON format:"
            "{\n"
            "    \"working_files\": [\"/full/path/to/file1.swift\", \"/full/path/to/file2.m\", \"/full/path/to/file3.h\"]\n"
            "}\n\n"
            "Return only valid JSON without Markdown symbols or invalid escapes."
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is user request to do:\n{idea}\nThis is the current project context:\n{all_file_contents}\n"
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            return {
                "reason": str(e)
            }

    async def get_file_plannings(self, idea):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            files (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the plan.
        """
        plan = await self.get_file_planning(idea)
        return plan
