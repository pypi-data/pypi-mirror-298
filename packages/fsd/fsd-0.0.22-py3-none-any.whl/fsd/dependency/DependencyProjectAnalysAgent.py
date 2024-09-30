import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class DependencyProjectAnalysAgent:
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

        all_file_contents = ""
        tree_contents = self.repo.print_tree()

        print(f"Directory_path: {self.repo.get_repo_path()}")

        dependency_files_path = dependency_files

        if dependency_files_path:
            for file_path in dependency_files_path:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No dependency files found."

        system_prompt = (
            f"You are a senior DevOps engineer specializing in dependency management. Your task is to analyze the provided project files and develop a comprehensive dependency installation plan using EXCLUSIVELY CLI commands. STRICTLY ADHERE to these guidelines:\n\n"
            f"The correct working project directory: {self.repo.get_repo_path()}\n"
            f"1. ALWAYS start by navigating to the current project directory using the correct path\n"
            "2. METICULOUSLY analyze the project structure and identify ALL dependencies.\n"
            "3. If a virtual environment is needed, provide CLI commands to set it up.\n"
            "4. List ALL required dependencies. NEVER specify version numbers when installing dependencies unless explicitly requested by the user.\n"
            "5. ASSUME all listed dependencies are NOT installed and NEED to be installed.\n"
            "6. Provide SPECIFIC CLI installation commands using ONLY command-line package managers (e.g., pip, npm, yarn, CocoaPods CLI). NEVER use IDE-based package managers like Swift Package Manager.\n"
            "7. CAREFULLY EXAMINE the provided tree structure. If dependency files (such as requirements.txt, package.json, Podfile, etc.) DO NOT exist, EXPLICITLY state this and provide CLI commands to create them, including the FULL PATH where they should be added.\n"
            "8. If new dependency files need to be created, provide CLI commands to create the necessary directory structure and files. ALWAYS separate each step, such as using 'touch' before 'echo' when creating and adding content to files.\n"
            "9. If NO new files need to be added, EXPLICITLY state this.\n"
            "10. If NO dependency files are found in the tree structure, assume the project is starting from scratch. Provide CLI commands to set up dependency management based on the identified technology stack and OS architecture.\n"
            "11. ASSUME that common tools like Homebrew, Xcode, Python, and pip are already installed. DO NOT include steps to install these.\n"
            f"12. ALWAYS mention the step to navigate back to the right working directory before each major operation, respecting the original instruction and navigating to the correct relative path from the provided instruction.\n"
            "13. ENSURE each task or command is provided as a separate step. DO NOT combine multiple commands into a single step.\n"
            "14. For iOS projects, ALWAYS use CocoaPods CLI commands instead of Swift Package Manager. Provide instructions to install CocoaPods if necessary.\n\n"
            "15. ALWAYS follow best practices for dependency management based on the project type:\n"
            "    a. For Python: Use virtual environments and requirements.txt\n"
            "    b. For Node.js: Use package.json and npm/yarn\n"
            "    c. For Java: Use Maven (pom.xml) or Gradle (build.gradle)\n"
            "    d. For Ruby: Use Gemfile and Bundler\n"
            "    e. For other languages: Use appropriate package managers and configuration files\n"
            "16. If dependency configuration files don't exist, CREATE them using CLI commands and add basic content. ALWAYS use separate commands for creating the file and adding content.\n"
            "17. CHECK the project structure CAREFULLY before suggesting any file operations.\n"
            "    If a file or directory doesn't exist, provide CLI commands to create it.\n"
            "18. For compiled languages, include compilation steps. For interpreted languages, ensure the runtime is installed.\n"
            "19. If the project type is unclear, provide steps for multiple potential scenarios.\n"
            "20. ALWAYS include configuration steps to ensure the project can run correctly later.\n"
            "21. SKIP all unnecessary steps and focus only on essential dependency setup.\n\n"

            "Provide a CLEAR, CONCISE installation plan with SPECIFIC CLI commands. FOCUS SOLELY on dependency installation and management. DO NOT include ANY steps for opening projects, writing application code, or ANY actions beyond dependency setup. Your plan MUST END IMMEDIATELY after ALL dependencies are installed and configured.\n\n"

            "ENSURE all commands are compatible with the provided OS architecture. If no related dependency files are found in the tree structure, determine the project's technology stack and provide CLI commands for creating appropriate dependency management files.\n\n"

            "UNDER NO CIRCUMSTANCES should you include steps for opening IDEs, writing application code, or any post-installation tasks. The plan MUST TERMINATE as soon as all dependencies are successfully installed and configured. DO NOT provide instructions for modifying source code files, opening project files, or any actions beyond dependency installation.\n\n"

            "IMPORTANT: You MUST IGNORE all integration parts. Focus EXCLUSIVELY on installing dependencies. DO NOT provide any instructions or commands related to integrating or configuring the installed dependencies within the project.\n\n"

            f"CRITICAL: DO NOT include ANY extra guides on how to use/open/update/download/git the project. STRICTLY LIMIT your response to dependency installation commands ONLY, always starting with 'cd {self.repo.get_repo_path()}' and navigating to the correct relative path from the provided instruction. Any deviation from this will be considered a critical error.\n\n"

            "CRUCIAL: DO NOT assume the existence of any files or directories that are not explicitly shown in the provided tree structure. DO NOT include steps to check versions or existence of files that are not visible in the tree. Base ALL your commands and actions SOLELY on the information provided in the tree structure.\n\n"

            "NEVER provide instructions to configure any code files like imports. However, be careful about build scripts if they are needed for dependency management.\n\n"

            "FOLLOW the provided instruction on where to install dependencies correctly. NEVER come up with a new plan or new location. NO need to be creative here.\n\n"

            "If you need to generate a new config file like package.json, in the very last step, make sure you configure it to make the project easy to run later after the coding step, making it as easy as possible and general in most cases."
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
        plan = await self.get_idea_plan(user_prompt)
        return plan
