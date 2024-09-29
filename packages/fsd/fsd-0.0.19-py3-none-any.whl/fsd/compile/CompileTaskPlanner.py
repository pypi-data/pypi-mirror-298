import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class CompileTaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner with necessary configurations.

        Args:
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            deployment_id (str): Deployment ID for the AI model.
            max_tokens (int): Maximum number of tokens for AI responses.
        """
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, os_architecture):
        """
        Get a dependency installation plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for dependency installation planning.
            os_architecture (str): The operating system and architecture of the target environment.

        Returns:
            dict: Dependency installation plan or error reason.
        """

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a principal-level DevOps engineer tasked with creating a focused, step-by-step compilation plan. Your goal is to structure tasks logically, following a pyramid architecture approach:\n\n"
                    f"The correct working project directory: {self.repo.get_repo_path()}\n"
                    "1. Always start with a task to navigate to the main project directory where compilation can be executed.\n"
                    "2. CAREFULLY ANALYZE the provided project tree structure before suggesting any file operations.\n"
                    "3. If a configuration file doesn't exist, include a step to create it using CLI commands.\n"
                    "4. Organize compilation steps based on the pyramid architecture principle, starting with foundational components.\n"
                    "5. Consider the provided OS architecture when specifying commands.\n"
                    "6. Provide detailed, environment-specific commands that can be executed directly in a terminal.\n"
                    "7. Strictly focus on compilation and build processes. Do not include steps for writing application code, opening projects, or tasks unrelated to the compilation process.\n"
                    "8. Ensure each CLI command is a separate task. Never combine multiple commands into a single step.\n"
                    "9. Don't make up extra steps or information. Provide only what's necessary to serve the user's request in the fastest way possible.\n"
                    "10. Do not include steps to check versions or file existence, as these cannot be determined from the provided tree structure.\n"
                    "11. If any errors occur during the process, another agent will handle them.\n"
                    "12. When installing dependencies, do not specify versions unless explicitly requested by the user.\n"
                    "13. For all cd commands, ensure they go alone and are not combined with any other command.\n"
                    "14. If you need to generate a new configuration file like package.json, in the very last step, make sure you configure it to make running the project easy after the coding step, as easy as possible, and make it general in most cases.\n\n"
                    "For each task, provide:\n"
                    "- file_name: The full path of the build configuration file to be updated (if applicable), or 'N/A' for CLI commands.\n"
                    "- prompt: A specific, comprehensive instruction for the given compilation-related task. For 'update' method, include detailed configuration changes, such as specific build settings to modify.\n"
                    "- method: Either only 'update' for build file modifications or 'bash' for terminal commands.\n"
                    "- command: The exact command to be executed (for 'bash' method only). Each CLI command should be a single operation.\n\n"
                    "Respond with a valid JSON in this format:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "N/A",\n'
                    '            "prompt": "Navigate to the main project directory",\n'
                    '            "method": "bash",\n'
                    f'            "command": "cd {self.repo.get_repo_path()}"\n'
                    '        },\n'
                    '        {\n'
                    '            "file_name": "/full/path/to/file",\n'
                    '            "prompt": "",\n'
                    '            "method": "",\n'
                    '            "command": ""\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    "Provide only the JSON response without additional text or Markdown symbols. Follow the provided instruction on where to install dependencies correctly. Never come up with a new plan or new location. No need to be creative here."
                )
            },
            {
                "role": "user",
                "content": f"Create a focused, step-by-step compilation plan following the pyramid architecture for these instructions. Consider the OS architecture: {os_architecture}. Provide detailed, environment-specific commands. Only include steps related to the compilation process. Always start by navigating to the main project directory. If the instruction specifies a relative path, navigate to the correct path in {self.repo.get_repo_path()} and then to the specified relative path. Do not include any steps for opening files, projects, or downloading. Ensure each CLI command is a separate task. Never combine multiple commands into a single step. Don't make up extra steps or information, and provide only what's necessary to serve the request in the fastest way possible. When installing dependencies, do not specify versions unless explicitly requested. Here's the current project tree structure:\n\n{self.repo.print_tree()}\n\nBased on this structure, create the compilation plan for:\n{instruction}\n"
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
