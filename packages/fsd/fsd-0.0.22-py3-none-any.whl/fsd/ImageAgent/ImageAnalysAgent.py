import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ImageAnalysAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway('bedrock')
        self.project_path = self.repo.get_repo_path()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, dependency_files):
        """
        Initialize the conversation with a system prompt and user context.
        """

        all_file_contents = ""
        tree_contents = self.repo.print_tree()

        dependency_files_path = dependency_files

        if dependency_files_path:
            for file_path in dependency_files_path:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No dependency files found."

        system_prompt = (
            f"You are a senior UI/UX designer specializing in image generation and style analysis. Your task is to analyze the provided project files, focusing on style-related elements, and develop a comprehensive plan for generating images that match the current theme. STRICTLY ADHERE to these guidelines:\n\n"

            f"1. ALWAYS start by navigating to the current working directory with: cd {self.project_path}\n"
            "2. METICULOUSLY analyze the project structure and identify ALL style-related files (e.g., CSS, SCSS, JSON theme files).\n"
            "3. Extract key information about the current theme, including:\n"
            "   a. Color scheme (primary, secondary, accent colors)\n"
            "   b. Typography (font families, sizes, weights)\n"
            "   c. Layout preferences (padding, margins, grid systems)\n"
            "   d. Recurring design elements (shapes, patterns, icons)\n"
            "4. Determine the preferred image sizes based on the layout and responsive design requirements.\n"
            "5. Identify the dominant background colors or patterns used in the project.\n"
            "6. Analyze any existing images or illustrations for style consistency.\n"
            "7. If NO style-related files exist, EXPLICITLY state this and provide recommendations for establishing a basic style guide.\n"
            "8. Based on the analysis, provide CLEAR guidelines for generating images that:\n"
            "   a. Match the color scheme of the project\n"
            "   b. Complement the typography choices\n"
            "   c. Fit the preferred sizing and aspect ratios (ONLY '1024x1024', '1792x1024', '1024x1792')\n"
            "   d. Align with the overall aesthetic and mood of the design\n"
            "9. Suggest image generation techniques or tools that would be suitable for creating images in line with the project's style.\n"
            "10. If the user requests specific image generation, provide detailed recommendations on how to adapt the request to fit the current theme and available sizes.\n"
            f"11. ALWAYS conclude by suggesting to save any generated images in an appropriate directory within {self.project_path}.\n\n"

            "Provide a CLEAR, CONCISE analysis and image generation plan. FOCUS SOLELY on style-related aspects and image creation guidelines. DO NOT include ANY steps for modifying code, implementing the images, or any actions beyond style analysis and image generation recommendations.\n\n"

            "ENSURE all suggestions are compatible with the provided style information and available image sizes ('1024x1024', '1792x1024', '1024x1792'). If no related style files are found, provide recommendations for establishing a basic style guide before proceeding with image generation.\n\n"

            "UNDER NO CIRCUMSTANCES should you include steps for writing code, modifying the project structure, or any tasks beyond style analysis and image generation guidelines.\n\n"

            f"CRITICAL: STRICTLY LIMIT your response to style analysis and image generation recommendations, always starting with 'cd {self.project_path}'. Any deviation from this will be considered a critical error.\n\n"

            "IMPORTANT: When the user mentions specific file names or paths, use EXACTLY those names and paths. DO NOT create or suggest new names. STRICTLY follow the user's directions if they mention any specific requirements or preferences."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current dependency files: {all_file_contents}\n\nProject structure: {tree_contents}\n"})
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
            response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0, 0)
            return response.choices[0].message.content
        except Exception as e:
            logger.info(f"Failed: {e}")
            return {
                "reason": str(e)
            }


    async def get_idea_plans(self, user_prompt):
        plan = await self.get_idea_plan(user_prompt)
        return plan
