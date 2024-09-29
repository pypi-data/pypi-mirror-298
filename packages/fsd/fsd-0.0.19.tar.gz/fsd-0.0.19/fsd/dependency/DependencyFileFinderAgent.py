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

class DependencyFileFinderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_dependency_file_planning(self, tree):
        """
        Request dependency file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            idea (str): The general plan idea.
            tree (str): The project structure.

        Returns:
            dict: JSON response with the dependency file plan.
        """
        prompt = (
            "Analyze the provided project structure and identify ALL main files related to dependency management, configuration, and installation. Your task:\n\n"
            "1. INCLUDE:\n"
            "   a. Main dependency files (e.g., 'requirements.txt', 'package.json', 'Pipfile', 'poetry.lock', 'Gemfile', 'build.gradle', 'pom.xml', 'setup.py', 'pyproject.toml', 'Cargo.toml', 'composer.json', 'yarn.lock', 'package-lock.json', 'Podfile', 'Cartfile', 'go.mod', 'mix.exs', 'sbt', 'project.clj', 'deps.edn').\n"
            "   b. Key configuration files (e.g., '.npmrc', 'pip.conf', 'gradle.properties', 'maven.config', '.yarnrc', '.bundleconfig', 'nuget.config', 'Gemfile.lock', 'Berksfile', 'Puppetfile', 'bower.json').\n"
            "   c. Critical environment files (e.g., '.env', '.dockerignore', 'docker-compose.yml', 'Dockerfile').\n"
            "   d. Essential build scripts (e.g., 'Makefile', 'build.sh', 'build.bat', 'gulpfile.js', 'webpack.config.js', 'rollup.config.js', 'tsconfig.json').\n"
            "   e. Project-specific dependency management files.\n"
            "2. EXCLUDE: All files from third-party libraries, external dependencies, or generated folders (e.g., 'node_modules', 'vendor', '.venv', 'dist', 'build', 'target', 'Pods').\n"
            "3. FOCUS: On root-level and key subdirectory files that directly impact the main project's dependency management.\n\n"
            "Provide your response as a JSON object with this exact structure:\n"
            "{\n"
            "    \"dependency_files\": [\"/full/path/to/file1.extension\", \"/full/path/to/file2.extension\", ...]\n"
            "}\n\n"
            f"CRITICAL: Return ONLY the valid JSON object. Do NOT include any explanatory text, markdown formatting, or extraneous characters. Ensure the JSON is parseable and contains the full paths of relevant files. The current working project is located at: {self.repo.get_repo_path()}"
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is the current project structure:\n{tree}\n"
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


    async def get_dependency_file_plannings(self):
        all_dependency_file_contents = self.repo.print_tree()

        plan = await self.get_dependency_file_planning(all_dependency_file_contents)
        return plan
