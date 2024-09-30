import os
import aiohttp
import json
import sys
from typing import List, Dict, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.openai import OpenAIClient
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class MainBuilderAgent:
    def __init__(self, repo):
        self.repo = repo

    def read_file_content(self, file_path: str) -> Optional[str]:
        """Read the content of a specified file."""
        try:
            with open(file_path, "r") as file:
                return file.read()
        except Exception as e:
            logger.info(f"Failed to read file {file_path}: {e}")
            return None

    async def get_pipeline_plan(self, files: str, tree: str) -> Dict:
        """Get a development plan for all txt files from Azure OpenAI based on the user prompt."""
        openai_client = OpenAIClient()
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a builder agent tasked with checking for any compile errors. "
                    "Analyze the provided context to determine the appropriate pipeline to use and respond in JSON format. "
                    "Follow these guidelines:\n\n"
                    "1. Use pipeline 1 if the project needs to be built with Apple Xcode.\n"
                    "2. Use pipeline 2 if the project can be built without Apple Xcode.\n"
                    "The JSON response must follow this format:\n\n"
                    '{\n    "pipeline": "1 or 2"\n}\n\n'
                    "Return only a valid JSON response without additional text or Markdown symbols."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Here are the file changes that need to be built to verify:\n{files}\n"
                    f"Here is the tree structure of the build project:\n{tree}\n"
                )
            }
        ]


        try:
            plan = await openai_client.complete(messages, 0.2)
            if "choices" in plan and len(plan["choices"]) > 0:
                message_content = plan["choices"][0]["message"]["content"]
                plan_json = json.loads(message_content)
                return plan_json
        except json.JSONDecodeError:
            good_json_string = repair_json(message_content)
            plan_json = json.loads(good_json_string)
            return plan_json 
        except Exception as e:
            error_message = plan.get("error", {}).get(
                "message", "Unknown error"
            )
            logger.error(f"Error: {error_message}")
            return {"reason": error_message}

    async def get_pipeline_plans(self, files: List[str]) -> Dict:
        """Get development plans for a list of txt files from Azure OpenAI based on the user prompt."""
        all_file_contents = self.repo.print_tree()
        return await self.get_pipeline_plan(files, all_file_contents)