import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)
class ExplainablePrePromptAgent:
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

    async def get_prePrompt_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a prompt engineering specialist. Analyze the provided project files and the user's prompt and respond in JSON format. Follow these guidelines:\n\n"
                    "original_prompt_language: Determine the user's main prompt language, such as English, Vietnamese, Indian, etc.\n"
                    "processed_prompt: If the user's original prompt is not in English, translate it to 100% English. Correct grammar, ensure it is clear, concise, and based on current project insights. Keep it crisp and short, avoiding confusion.\n"
                    "pipeline: You need to pick one best pipeline that fits the user's prompt. Only respond with a number for the specific pipeline you pick, such as 1, 2, following the guideline below:\n"
                    "1. Need context: Use if the user asks about the project, context insights to answer.\n"
                    "2. Don't need context: Use if the user asks about general things and can answer without context insights.\n"
                    "The JSON response must follow this format:\n\n"
                    "{\n"
                    '    "processed_prompt": "",\n'
                    '    "original_prompt_language": "Vietnamese, English, Chinese, etc.",\n'
                    '    "pipeline": "1 or 2"\n'
                    "}\n\n"
                    "Return only a valid JSON response without additional text or Markdown symbols or invalid escapes."
                )
            },
            {
                "role": "user",
                "content": f"User original prompt:\n{user_prompt}\n\n"
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

    async def get_prePrompt_plans(self, user_prompt):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        plan = await self.get_prePrompt_plan(user_prompt)
        return plan
