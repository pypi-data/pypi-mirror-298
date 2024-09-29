import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class TaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner with necessary configurations.

        Args:
            directory_path (str): Path to the project directory.
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            deployment_id (str): Deployment ID for the AI model.
            max_tokens (int): Maximum number of tokens for AI responses.
        """
        self.max_tokens = 4096
        self.repo = repo
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, file_list):
        """
        Get a development plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for task planning.
            crawl_logs: Logs from web crawling, if any.

        Returns:
            dict: Development plan or error reason.
        """
            # Start of Selection
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a highly experienced principal engineer specializing in Pyramid architecture and efficient system integration. Your mission is to generate an ordered list of files necessary for implementing a system following Pyramid architecture best practices, based on the original instruction and the provided list of files. The list should begin with foundational components and progress to more complex files that require greater context and integration.\n\n"
                    "**Guidelines:**\n"
                    "1. **File Mapping:** Ensure that each `file_name` corresponds exactly to the full path provided in the `file_list`. These are the files we are going to work on.\n"
                    "2. **Ordering:** Start with the most foundational and context-rich files at the base, then move towards higher-level, more complex files.\n"
                    "3. **Content Scope:** Focus exclusively on listing the essential files required for implementation. Do not include additional tasks, instructions, or unnecessary files.\n"
                    "4. **File Structure:** For each file, provide only the `file_name` (full path) and `techStack` attributes.\n"
                    "5. **Integration:** Ensure that each listed file is designed to integrate seamlessly with the others, promoting maintainability and scalability.\n"
                    "6. **Exclusions:** Omit any files related to configuration, dependencies, or other non-essential aspects. **Additionally, exclude all image files except those with the `.svg` extension and exclude all audio asset files.**\n"
                    "7. **Assets:** For asset-related files, include **only** those with the `.svg` extension.\n\n"
                    "**Response Format:**\n"
                    "Provide a valid JSON object following this structure:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "/full/path/to/file",\n'
                    '            "techStack": ""\n'
                    '        },\n'
                    '        {\n'
                    '            "file_name": "/full/path/to/another/file",\n'
                    '            "techStack": ""\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    "**Important:** Respond with **only** the JSON content as specified above. Do not include any additional text, explanations, or Markdown formatting. Ensure that the files are ordered correctly according to Pyramid architecture best practices to facilitate optimal integration and maintainability.\n\n"
                    f"Current working project is {self.repo.get_repo_path()}"
                )
            },
            {
                "role": "user",
                "content": f"Create an ordered list of files to implement following Pyramid architecture best practices. Ensure foundational files are listed first, progressing to more complex files that require greater context. These are the files we are going to work on:\n{file_list}\n\nInclude only the `file_name` (full path) and `techStack` for each file in the specified JSON format. Ensure that the `file_name` respects the root path and the full correct relative path from the original instruction. Here is original instruction: {instruction}"
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
            logger.error(f"Failed to get task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction, file_lists):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        plan = await self.get_task_plan(instruction, file_lists)
        return plan
