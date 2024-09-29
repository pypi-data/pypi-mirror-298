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

class CompilePrePromptAgent:
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
            logger.error(f"Failed to read file {file_path} in binary mode: {e}")

        return None

    async def get_prePrompt_plan(self, all_file_contents, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
            # Start of Selection
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an image generation specialist. Your task is to detect and process image generation requests STRICTLY for the following formats ONLY: PNG, JPG, JPEG, png, jpg, or jpeg. Analyze the user prompt and project context, and respond in JSON format following these guidelines:\n\n"
                    "processed_prompt: If the user requests image generation in ANY of the supported formats ONLY, provide the details extracted from the user prompt for all images to be created, including:\n"
                    "- Save path: Specify where each image should be saved within the project structure.\n"
                    "- Name: Suggest an appropriate filename for each image.\n"
                    "- Dimension: Specify the image dimensions (width x height in pixels) for each image.\n"
                    "- Description: Provide a detailed description of each image to be generated.\n"
                    "Combine the details of all images into a single string, separating each image's details with a newline character.\n"
                    "If the user prompt is not in English, translate it accurately. If NO supported image formats are requested, or if ANY unsupported format (e.g., SVG, GIF, etc.) is mentioned, set processed_prompt to an empty string.\n"
                    "pipeline: Determine the appropriate action based on the presence of ONLY supported image formats. Respond with a string:\n"
                    "\"0\": No supported image generation requested or ANY unsupported format mentioned.\n"
                    "\"1\": Supported image generation requested (ONLY PNG, JPG, JPEG, png, jpg, or jpeg).\n"
                    "The JSON response must follow this structure:\n\n"
                    "{\n"
                    '    "processed_prompt": "Save path: [path1], Name: [filename1], Dimension: [width1]x[height1], Description: [detailed image description1]\n'
                    'Save path: [path2], Name: [filename2], Dimension: [width2]x[height2], Description: [detailed image description2]\n'
                    '...\n'
                    '",\n'
                    '    "pipeline": "0" or "1"\n'
                    "}\n\n"
                    "Ensure the response is a valid JSON object without any additional text, comments, or markdown. ONLY process image generation requests for the EXPLICITLY specified formats (PNG, JPG, JPEG, png, jpg, or jpeg). ANY mention of unsupported formats like SVG, GIF, etc., should result in setting pipeline to \"0\" and processed_prompt to an empty string."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Project context:\n{all_file_contents}\n\n"
                    f"User directive:\n{user_prompt}\n"
                )
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0, 0)
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.info(f"Failed: {e}")
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
        all_file_contents = self.repo.print_summarize_with_tree()
        plan = await self.get_prePrompt_plan(all_file_contents, user_prompt)
        print(f"CompilePrePromptAgent: {plan}")
        return plan
