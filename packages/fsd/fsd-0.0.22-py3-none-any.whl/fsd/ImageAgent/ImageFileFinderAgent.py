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

class ImageFileFinderAgent:
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


    async def get_style_file_planning(self, tree):
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
            f"Analyze the provided project structure and identify ALL main files related to color and style of the current project. Your task:\n\n"
            "1. INCLUDE:\n"
            "   a. Main style files (e.g., 'styles.css', 'main.scss', 'theme.less', 'colors.json', 'variables.css', 'palette.js').\n"
            "   b. Key configuration files for styling (e.g., 'tailwind.config.js', 'styled-components.js', 'theme.js').\n"
            "   c. UI component libraries or style guide files (e.g., 'ui-kit.css', 'design-system.js').\n"
            "   d. Any files that define color schemes or theming (e.g., 'colors.ts', 'theme.json').\n"
            "2. EXCLUDE: All files from third-party libraries, external dependencies, or generated folders.\n"
            "3. FOCUS: On root-level and key subdirectory files that directly impact the main project's styling.\n"
            "4. If no clear style file exists, identify potential relevant files that could represent the current style of the project.\n\n"
            "Provide your response as a JSON object with this exact structure:\n"
            "{\n"
            f"    \"style_files\": [\"{self.repo.get_repo_path()}/full_correct_relative_path/file1.extension\", \"{self.repo.get_repo_path()}/full_correct_relative_path/file2.extension\", ...]\n"
            "}\n\n"
            "CRITICAL: Return ONLY the valid JSON object. Do NOT include any explanatory text, markdown formatting, or extraneous characters. Ensure the JSON is parseable and contains the full paths of relevant files."
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


    async def get_style_file_plannings(self):
        """
        Request dependency file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            tree (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the dependency file plan.
        """
        all_tree_file_contents = self.repo.print_tree()
        plan = await self.get_style_file_planning(all_tree_file_contents)
        return plan
