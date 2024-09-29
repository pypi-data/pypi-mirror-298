import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class CompileProjectAnalysAgent:
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

    def initial_setup(self, dependency_files, OS_architecture):
        """
        Initialize the conversation with a system prompt and user context.
        """

        tree_contents = self.repo.print_tree()

        dependency_files_path = dependency_files

        all_file_contents = ""
        if dependency_files_path:
            for file_path in dependency_files_path:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No dependency files found."

        system_prompt = (
            f"You are a senior DevOps engineer. Analyze the project structure and develop a concise plan for setting up and compiling the project for local development using CLI commands. Follow these guidelines:\n\n"
            f"Working directory: {self.repo.get_repo_path()}\n"
            "1. Provide a SHORT TITLE for the setup process.\n"
            "2. ANALYZE the project structure.\n"
            "3. For empty/incomplete projects:\n"
               "   a. Create necessary directories/files.\n"
               "   b. Provide CLI commands for file creation.\n"
            "4. For existing projects:\n"
               "   a. Analyze the structure for config files, build scripts, etc.\n"
               "   b. Don't assume existence of files not shown.\n"
            "5. Focus on local development setup only.\n"
            f"6. Always navigate to the right path in {self.repo.get_repo_path()} and the right relative path from the provided instruction.\n"
            "7. Explain steps concisely, referencing specific file names/paths.\n"
            "8. Provide CLI commands for setup, file creation, dependency installation, and compilation.\n"
            "9. For new files, provide exact CLI commands to create and populate.\n"
            "10. Navigate back to working directory before major operations.\n"
            "11. Provide each task as a separate, logical step.\n"
            "12. Follow best practices for dependency management (e.g., venv for Python, npm for Node.js).\n"
            "13. Create dependency config files if missing.\n"
            "14. Check project structure before suggesting file operations.\n"
            "15. Include compilation steps for compiled languages.\n"
            "16. Provide steps for multiple scenarios if project type is unclear.\n"
            "17. Don't specify dependency versions unless requested.\n\n"

            "Response structure:\n"
            "- Title: [Short setup process title]\n"
            "- Explanation: [Brief process overview]\n"
            "- Steps: [Numbered list of concise steps with CLI commands]\n\n"

            f"CRITICAL: Limit to local development setup. Start with 'cd {self.repo.get_repo_path()}' and end with final compilation/run command. Use exact file names/paths. Provide each CLI command as a separate step."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current dependency files: {all_file_contents}\n\nProject structure: {tree_contents}\n\nOS Architecture: {OS_architecture}"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

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

    async def get_idea_plan(self, user_prompt):
        """
        Get development plan for all txt files from Azure OpenAI based on user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        prompt = (
             f"Follow the user prompt strictly and provide a no code response:\n{user_prompt}\n\n"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            return response.choices[0].message.content
        except Exception as e:
            logger.info(f"Failed: {e}")
            return {
                "reason": str(e)
            }


    async def get_idea_plans(self, user_prompt):
        """
        Get development plans for a list of txt files from Azure OpenAI based on user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """

        plan = await self.get_idea_plan(user_prompt)
        return plan
