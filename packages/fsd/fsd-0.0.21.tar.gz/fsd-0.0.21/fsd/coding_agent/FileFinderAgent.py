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

class FileFinderAgent:
    def __init__(self, repo):
        """
        Initialize the FileFinderAgent with directory path, API key, endpoint, deployment ID, and max tokens for API requests.

        Args:
            directory_path (str): Path to the directory containing .txt files.
            api_key (str): API key for Azure OpenAI API.
            endpoint (str): Endpoint URL for Azure OpenAI.
            deployment_id (str): Deployment ID for the model.
            max_tokens (int): Maximum tokens for the Azure OpenAI API response.
        """
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_file_planning(self, idea):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            idea (str): The general plan idea.
            tree (str): The project structure.

        Returns:
            dict: JSON response with the plan.
        """
        prompt = (
            "From the provided development plan, build a JSON to list all working_files to be used. Provide only a JSON response without any additional text or Markdown formatting. "
            "Working_files must include the full path for each file that the user mentions to work on. "
            "Use this JSON format:"
            "{\n"
            "    \"working_files\": [\"/full/path/to/file1.extension\", \"/full/path/to/file2.extension\", \"/full/path/to/file3.extension\"]\n"
            "}\n\n"
            f"current project path is \"{self.repo.get_repo_path()}\"\n"
            "Return only valid JSON without Markdown symbols or invalid escapes."
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is the user's request to do:\n{idea}\nThis is the current project structure:\n{self.repo.print_tree()}\n"
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
            logger.info(f"Failed: {e}")
            return {
                "reason": str(e)
            }


    async def get_file_plannings(self, idea):
        return await self.get_file_planning(idea)
        
