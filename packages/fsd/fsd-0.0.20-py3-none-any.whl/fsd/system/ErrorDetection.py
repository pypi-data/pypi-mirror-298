import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class ErrorDetection:
    """
    A class to plan and manage tasks using AI-powered assistance, including error handling and suggestions.
    """

    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway('bedrock')

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self):
        """
        Initialize the conversation with a system prompt and user context.
        """

        system_prompt = (
            "You are an expert DevOps engineer tasked with analyzing errors that occur during project run, build, or compile processes. Your job is to determine whether the error is a code-related issue or a configuration/dependency-related issue. Provide a clear and comprehensive analysis.\n\n"
            "Instructions:\n"
            "1. Carefully examine the provided error message.\n"
            "2. Categorize the error as either a code error (type 1) or a configuration/dependency-related error (type 2).\n"
            "3. Extract and combine only the error-related information from the provided log, excluding any non-error content.\n"
            "4. Return your analysis in a JSON format with the following structure:\n"
            "   {\n"
            "     'error_type': <1 or 2 as an integer>,\n"
            "     'error_message': <combined error information as a string>\n"
            "   }\n\n"
            "Error Types:\n"
            "1. Code Error (return 'error_type': 1):\n"
            "   - Syntax errors, logic errors, missing imports, incorrect usage, type mismatches, undefined variables, incorrect function calls\n\n"
            "2. Configuration/Dependency-Related Error (return 'error_type': 2):\n"
            "   - Missing repositories, failed installations, runtime errors due to missing dependencies, incorrect configurations, version conflicts, port blocks, failed environment setups, missing environment variables\n\n"
            "Examples:\n"
            "1. Code Error:\n"
            "   {\n"
            "     'error_type': 1,\n"
            "     'error_message': 'SyntaxError: invalid syntax (file.py, line 10)'\n"
            "   }\n\n"
            "2. Configuration/Dependency-Related Error:\n"
            "   {\n"
            "     'error_type': 2,\n"
            "     'error_message': 'ImportError: No module named \"requests\". ModuleNotFoundError: No module named \"yaml\". ConnectionError: Port 8080 blocked by firewall.'\n"
            "   }\n\n"
            "3. Port Block Error:\n"
            "   {\n"
            "     'error_type': 2,\n"
            "     'error_message': 'ConnectionError: Port 3306 is blocked by the firewall, preventing database connectivity.'\n"
            "   }\n\n"
            "4. Missing Environment Variable:\n"
            "   {\n"
            "     'error_type': 2,\n"
            "     'error_message': 'EnvironmentError: Required environment variable \"DATABASE_URL\" is not set.'\n"
            "   }\n"
            "Provide only the JSON response without additional text or Markdown symbols."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
    

    async def get_task_plan(self, error):
        """
        Get a dependency installation plan based on the error, config context, and OS architecture using AI.

        Args:
            error (str): The error message encountered during dependency installation.

        Returns:
            dict: Dependency installation plan or error reason.
        """

        prompt = (
             f"Analyze the following error and determine if it's a code error or a dependency error. Provide a comprehensive explanation and suggested action.\n\n"
             f"Error: {error}\n"
             "Return your analysis in a JSON format with the following structure:\n"
             "{\n"
             "  'error_type': <1 or 2 as an integer>,\n"
             "  'error_message': <combined error information as a string>\n"
             "}\n"
             "Provide only the JSON response without additional text or Markdown symbols."
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            self.remove_latest_conversation()
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"Failed to get task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, error):
        """
        Get development plans based on the error, config context, and OS architecture.

        Args:
            error (str): The error message encountered during dependency installation.
            config_context (str): The configuration context of the project.
            os_architecture (str): The operating system and architecture of the target environment.

        Returns:
            dict: Development plan or error reason.
        """
        plan = await self.get_task_plan(error)
        return plan
