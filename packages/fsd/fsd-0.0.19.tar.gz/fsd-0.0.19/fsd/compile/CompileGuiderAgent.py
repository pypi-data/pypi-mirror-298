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

class CompileGuiderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def initial_setup(self, user_prompt):
        """Initialize the setup with the provided instructions and context."""
        # Step to remove all empty files from the list
        
        all_file_contents = self.repo.print_tree()

        prompt = (
            "You are an elite DevOps engineering specialist with unparalleled expertise in dependency management and project architecture. Your task is to meticulously analyze the provided project files and user prompt, then deliver a comprehensive response in JSON format. Adhere to these stringent guidelines:\n\n"
            "processed_prompt: Transform the user's prompt into a crystal-clear, highly detailed directive. If not in English, provide an impeccable translation. Elevate the prompt by incorporating project-specific insights, anticipating potential challenges, and outlining a strategic approach. Your refined prompt should serve as an authoritative roadmap for the coding agent.\n"
            "pipeline: Determine the optimal course of action with surgical precision. Respond with a number (0, 1, or 2) based on these exacting criteria:\n"
            "For advanced dependency management:\n"
            "0. Null operation: Employ when the user explicitly confirms no further dependency-related actions are required.\n"
            "1. Expert intervention imperative: Utilize when installation demands sophisticated IDE manipulations, intricate package manager operations, or system-level configurations that exceed automated capabilities.\n"
            "2. Automated resolution feasible: Select when dependencies can be efficiently managed through command-line interfaces, configuration file modifications, or scripted processes.\n"
            "explainer: For pipeline 1 scenarios, craft an exhaustive, technically rigorous explanation detailing why automated installation is suboptimal or impossible. Provide a meticulously structured, step-by-step guide for manual intervention. Include critical warnings, best practices, and potential pitfalls. This explanation must be delivered in the user's original language, ensuring clarity and precision in communication.\n"
            "The JSON response must strictly adhere to this structure, with no deviations:\n\n"
            "{\n"
            '    "processed_prompt": "Exhaustive, strategically enhanced user directive",\n'
            '    "pipeline": "0, 1, or 2",\n'
            '    "explainer": "Comprehensive technical rationale and expert guidance"\n'
            "}\n\n"
            "Your response must be a flawlessly formatted JSON object, devoid of any extraneous text, comments, or markdown elements."
            f"Critical project context:\n{all_file_contents}\n"
        )

        self.conversation_history.append({"role": "system", "content": prompt})
        self.conversation_history.append({"role": "user", "content": f"{user_prompt}"})


    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

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

    async def get_guider_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        self.conversation_history.append({"role": "user", "content": f"{user_prompt}"})

        try:
            response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            self.conversation_history.append({"role": "assistant", "content": f"{response.choices[0].message.content}"})
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

    async def get_guider_plans(self, user_prompt):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """

        plan = await self.get_guider_plan(user_prompt)
        return plan
