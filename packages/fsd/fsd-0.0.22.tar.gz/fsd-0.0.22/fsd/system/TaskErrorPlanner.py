import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class TaskErrorPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance, including error handling and suggestions.
    """

    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway('bedrock')

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

    async def get_task_plan(self, error, config_context, os_architecture, compile_files):
        """
        Get a dependency installation plan based on the error, config context, and OS architecture using AI.

        Args:
            error (str): The error message encountered during dependency installation.
            config_context (str): The configuration context of the project, including what is being built.
            os_architecture (str): The operating system and architecture of the target environment.
            compile_files (list): List of files to be checked for configuration issues.

        Returns:
            dict: Dependency installation plan or error reason.
        """

        all_file_contents = ""

        files_paths = compile_files

        if files_paths:
            for file_path in files_paths:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No related files found."


        messages = [
            {
                "role": "system",
                "content": (
                    "You are a principal-level DevOps engineer tasked with creating a focused, step-by-step dependency installation/ build configuration plan and providing error resolution suggestions. Your goal is to structure tasks logically, following a pyramid architecture approach:\n\n"
                    "1. Analyze the provided error message and suggest fixes.\n"
                    "2. Organize installation steps based on the pyramid architecture principle, starting with foundational components.\n"
                    "3. Consider the provided OS architecture when specifying commands.\n"
                    "4. Provide detailed, environment-specific commands that can be executed directly in a terminal.\n"
                    "5. Carefully check all configuration files provided for any issues with names, paths, or other potential misconfigurations.\n\n"
                    "For each task, provide:\n"
                    f"- file_name: The full path of the dependency configuration file to be updated (if applicable), or 'N/A' for bash commands. The full path should include the current project directory path, which is {self.repo.get_repo_path()}.\n"
                    "- error_resolution: A specific, comprehensive instruction for the given dependency-related task. For 'update' method, include detailed configuration changes.\n"
                    "- method: Either 'update' for dependency file modifications or 'bash' for terminal commands.\n"
                    "- command: The exact command to be executed (for 'bash' method only). Ensure that 'cd' commands are provided alone and not combined with any other commands.\n"
                    "Respond with a valid JSON in this format:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "",\n'
                    '            "method": "",\n'
                    '            "command": "",\n'
                    '            "error_resolution": ""\n'
                    '        },\n'
                    '        {\n'
                    '            "file_name": "",\n'
                    '            "method": "",\n'
                    '            "command": "",\n'
                    '            "error_resolution": ""\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    "Provide only the JSON response without additional text or Markdown symbols."
                )
            },
            {
                "role": "user",
                "content": f"Analyze this error and create a focused, step-by-step dependency installation plan to resolve it. Consider the following information:\n\n"
                           f"1. Config Context (what is being built): {config_context}\n"
                           f"2. Error encountered: {error}\n"
                           f"3. Current OS Architecture: {os_architecture}\n"
                           f"4. Configuration Files Context:\n{all_file_contents}\n\n"
                           f"Provide detailed, environment-specific commands. Only include steps related to dependency configuration and installation. "
                           f"Do not include any steps for opening files, projects, or downloading. "
                           f"Check all configuration files for any issues with names, paths, or other misconfigurations. "
                           f"Ensure the plan addresses the specific error and takes into account the current architecture and build context."
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

    async def get_task_plans(self, error, config_context, os_architecture, compile_files):
        """
        Get development plans based on the error, config context, and OS architecture.

        Args:
            error (str): The error message encountered during dependency installation.
            config_context (str): The configuration context of the project.
            os_architecture (str): The operating system and architecture of the target environment.

        Returns:
            dict: Development plan or error reason.
        """
        plan = await self.get_task_plan(error, config_context, os_architecture, compile_files)
        return plan
