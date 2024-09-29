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

    async def get_prePrompt_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        all_file_contents = self.repo.print_tree()
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an ELITE software engineering specialist with UNPARALLELED expertise in project compilation, build processes, and local development environments. METICULOUSLY analyze the provided project files and user prompt, then deliver a COMPREHENSIVE response in JSON format. STRICTLY ADHERE to these CRITICAL guidelines:\n\n"
                    "processed_prompt: Transform the user's prompt into a CRYSTAL-CLEAR, HIGHLY DETAILED directive focused PRIMARILY on setting up and running the project in a local development environment, unless EXPLICITLY instructed otherwise. If not in English, provide an IMPECCABLE translation. ELEVATE the prompt by incorporating project-specific insights related to local development, testing, and running the application. Your refined prompt MUST serve as an AUTHORITATIVE roadmap for the development process.\n"
                    "pipeline: Determine the OPTIMAL course of action with SURGICAL PRECISION. Respond with a number (0, 1, or 2) based on these EXACTING criteria:\n"
                    "For project setup and execution:\n"
                    "0. No setup needed: SELECT THIS OPTION WHEN the project is empty, lacks executable code, or requires no setup process.\n"
                    "1. IDE required: Utilize when the project DEMANDS sophisticated IDE environments such as Xcode, Android Studio, or other integrated development environments that CANNOT BE HANDLED through CLI for local development and testing.\n"
                    "2. CLI setup and execution feasible: SELECT THIS OPTION WHEN the project can be set up and run through command-line interfaces (CLI) or scripted processes. This INCLUDES standard tools like npm start, python manage.py runserver, gradle run, and similar CLI-based methods for local development and testing.\n"
                    "The JSON response MUST STRICTLY adhere to this structure, with ABSOLUTELY NO DEVIATIONS:\n\n"
                    "{\n"
                    '    "processed_prompt": "EXHAUSTIVE, STRATEGICALLY ENHANCED user directive, PRIORITIZING local development setup and execution instructions, ONLY including build/deployment if EXPLICITLY requested",\n'
                    '    "pipeline": "0, 1, or 2"\n'
                    "}\n\n"
                    "Your response MUST be a FLAWLESSLY formatted JSON object, DEVOID of ANY extraneous text, comments, or markdown elements. FOCUS PRIMARILY ON LOCAL DEVELOPMENT SETUP AND EXECUTION, unless the user EXPLICITLY requests deployment preparation."
                )
            },
            {
                "role": "user",
                "content": (
                    f"CRITICAL project structure and files summary:\n{all_file_contents}\n\n"
                    f"User directive:\n{user_prompt}\n"
                )
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
            logger.info(f"Failed: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt):
        plan = await self.get_prePrompt_plan(user_prompt)
        return plan
