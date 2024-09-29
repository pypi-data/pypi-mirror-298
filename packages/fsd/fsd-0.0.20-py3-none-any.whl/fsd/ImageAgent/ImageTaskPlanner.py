import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class ImageTaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_task_plan(self, instruction):
        """
        Get a dependency installation plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for image planning.

        Returns:
            dict: Dependency installation plan or error reason.
        """

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior UI/UX designer specializing in image generation and style analysis. Your task is to create a focused, step-by-step image generation plan based on the project's current style and the user's instructions. Follow these guidelines:\n\n"
                    "1. Always start with a task to specify the main project directory where images should be saved.\n"
                    "2. Organize image generation steps logically, considering the project's overall style and theme.\n"
                    "3. Provide detailed prompts for each image to be generated, ensuring they align with the project's style.\n"
                    "4. Specify the file path and name for each image, relative to the main project directory.\n"
                    "5. Include image dimensions and format (e.g., png, jpg) for each task. Use only the following size options for DALL-E 3: '1024x1024', '1792x1024', '1024x1792'.\n\n"
                    "For each task, provide:\n"
                    "- file_path: The full path and filename where the image should be saved, relative to the main project directory.\n"
                    "- prompt: A detailed description of the image to be generated, including style, colors, content, and any other relevant details.\n"
                    "- dalle_dimension: The width and height of the image in pixels for DALL-E 3 (must be one of '1024x1024', '1792x1024', '1024x1792').\n"
                    "- actual_dimension: The actual width and height of the image in pixels, adaptive to the use case.\n"
                    "- format: The file format of the image (e.g., 'png', 'jpg'). Always use lowercase for the format.\n\n"
                    "Respond with a valid JSON in this format:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    f'           "file_path": "{self.repo.get_repo_path()}/images/example.png",\n'
                    '            "prompt": "Generate an image that...",\n'
                    '            "dalle_dimension": "1024x1024",\n'
                    '            "actual_dimension": "800x600",\n'
                    '            "format": "png"\n'
                    '        },\n'
                    '        {\n'
                    '            "file_path": "",\n'
                    '            "prompt": "",\n'
                    '            "dalle_dimension": "",\n'
                    '            "actual_dimension": "",\n'
                    '            "format": ""\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    "Provide only the JSON response without additional text or Markdown symbols. Ensure all image formats are in lowercase."
                )
            },
            {
                "role": "user",
                "content": f"Create a focused, step-by-step image generation plan based on these instructions. Provide detailed prompts for each image, ensuring they align with the project's current style. Specify the file path for each image relative to '{self.repo.get_repo_path()}'. Include DALL-E 3 dimensions (using only '1024x1024', '1792x1024', or '1024x1792') and actual dimensions adaptive to the use case. Also include the format for each task. Always use lowercase for the image format. Respect every requirement and guideline for file_path, dimensions, and format from the original instruction:\n{instruction}\n"
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"Failed to get task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        plan = await self.get_task_plan(instruction)
        return plan
