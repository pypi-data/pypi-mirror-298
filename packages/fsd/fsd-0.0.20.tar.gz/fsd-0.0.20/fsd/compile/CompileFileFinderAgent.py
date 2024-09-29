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

class CompileFileFinderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    def read_dependency_file_content(self, file_path):
        """
        Read the content of a dependency file.

        Args:
            file_path (str): Path to the dependency file to read.

        Returns:
            str: Content of the dependency file, or None if an error occurs.
        """
        try:
            with open(file_path, "r") as file:
                return file.read()
        except Exception as e:
            logger.info(f"Failed to read dependency file {file_path}: {e}")
            return None


    async def get_compile_file_planning(self, userRequest, tree):
        """
        Request compile file planning from Azure OpenAI API for a given project structure.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            userRequest (str): The user's request or context.
            tree (str): The project structure.

        Returns:
            dict: JSON response with the compile file plan.
        """
        prompt = (
            "Analyze the provided project structure and identify MAIN files that are crucial for the compilation, running, and build processes. Your task:\n\n"
            "1. INCLUDE:\n"
            "   a. MAIN dependency files (e.g., requirements.txt, package.json, Gemfile, build.gradle, pom.xml, Cargo.toml)\n"
            "   b. MAIN entry point files (e.g., main.py, index.js, App.java, Program.cs, main.go, app.rb)\n"
            "   c. MAIN configuration files (e.g., .csproj, CMakeLists.txt, Makefile, webpack.config.js, tsconfig.json)\n"
            "   d. MAIN build scripts (e.g., setup.py, build.gradle, gulpfile.js, Rakefile)\n"
            "   e. MAIN environment files (e.g., .env, .dockerignore, Dockerfile, docker-compose.yml)\n"
            "2. EXCLUDE ENTIRELY:\n"
            "   a. Files from third-party libraries (e.g., node_modules/, vendor/, lib/)\n"
            "   b. Generated folders (e.g., build/, dist/, target/)\n"
            "   c. IDE-specific folders (e.g., .vscode/, .idea/)\n"
            "   d. Dependency caches (e.g., .gradle/, .nuget/, .m2/)\n"
            "3. FOCUS ON: Main entry points, primary build scripts, and core configuration files\n"
            "4. CONSIDER: Project-specific main files that significantly impact compilation or runtime\n\n"
            "Provide your response as a JSON object with this exact structure:\n"
            "{\n"
            "    \"crucial_files\": [\"full/path/to/file1.extension\", \"full/path/to/file2.extension\", ...]\n"
            "}\n\n"
            f"CRITICAL: Return ONLY the valid JSON object. Do NOT include any explanatory text, markdown formatting, or extraneous characters. Ensure the JSON is parseable and contains the full paths of main relevant files for compilation, running, and building the project. The current working project is located at: {self.repo.get_repo_path()}"
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"User Request: {userRequest}\nThis is the current project structure:\n{tree}\n"
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
            logger.info(f"Failed to get dependency file planning: {e}")
            return {
                "reason": str(e)
            }


    async def get_compile_file_plannings(self, userRequest):
        """
        Request dependency file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            tree (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the dependency file plan.
        """
        all_dependency_file_contents = self.repo.print_tree()

        plan = await self.get_compile_file_planning(userRequest, all_dependency_file_contents)
        return plan
