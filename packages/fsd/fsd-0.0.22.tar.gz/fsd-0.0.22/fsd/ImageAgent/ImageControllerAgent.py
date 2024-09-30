import os
import sys
import json
import subprocess
import asyncio
import re

from .ImagePrePromptAgent import CompilePrePromptAgent
from .ImageTaskPlanner import ImageTaskPlanner
from .ImageFileFinderAgent import ImageFileFinderAgent
from .ImageAnalysAgent import ImageAnalysAgent
from .ImageGenAgent import ImageGenAgent

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.coding_agent.LanguageAgent import LanguageAgent
from fsd.util import utils
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

HOME_DIRECTORY = os.path.expanduser('~')
HIDDEN_ZINLEY_FOLDER = '.zinley'

class ImageControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.preprompt = CompilePrePromptAgent(repo)
        self.lang = LanguageAgent(repo)
        self.fileFinder = ImageFileFinderAgent(repo)
        self.analysAgent = ImageAnalysAgent(repo)
        self.taskPlanner = ImageTaskPlanner(repo)
        self.imageGenAgent = ImageGenAgent(repo)

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
            logger.error(f"Failed to read file {file_path} in binary mode: {e}")

        return None

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)


    async def start_image_process(self, instruction):
        file_result = await self.fileFinder.get_style_file_plannings()

        style_files = file_result.get('style_files', [])

        self.analysAgent.initial_setup(style_files)

        logger.info("Now I will create an initial image plan for clarification.")

        idea_plan = await self.analysAgent.get_idea_plans(instruction)

        logger.info(f"This is my initial image plan: {idea_plan}")

        while True:
            logger.info(
                "Are you satisfied with this image plan? Enter \"yes\" if satisfied, or provide feedback for modifications: ")

            user_prompt_json = input()
            user_prompt, _ = self.parse_payload(user_prompt_json)
            user_prompt = user_prompt.lower()

            if user_prompt == "" or user_prompt == "yes" or user_prompt == "y":
                break
            else:
                logger.info(f"Let's me update my image plan!")
                eng_prompt = await self.lang.get_language_plans(user_prompt, "DevOps engineer")
                instruction = instruction + " " + eng_prompt
                self.analysAgent.remove_latest_conversation()
                idea_plan = await self.analysAgent.get_idea_plans(instruction)
                logger.info(f"This is my updated image plan: {idea_plan}")

        self.analysAgent.clear_conversation_history()

        logger.info("Alright, let's get organized! Preparing the task and getting my digital gears turning.")
        task = await self.taskPlanner.get_task_plan(idea_plan)
        await self.imageGenAgent.generate_images(task)
        logger.info(f"{instruction}: Done")


    async def process_creation(self, data):
        """Process the creation of new files based on provided data."""
        if data.get('Is_creating'):
            processes = data.get('Adding_new_files', [])
            await self.project.execute_files_creation(processes)


    def parse_payload(self, user_prompt_json):
        try:
            file_path = None
            data = json.loads(user_prompt_json)
            user_prompt = data.get("prompt", "")
            file_path = data.get("file_path", None)
        except json.JSONDecodeError:
            # If input is not valid JSON, treat it as plain text
            user_prompt = user_prompt_json
            logger.info(f"Received Plain Text Prompt: {user_prompt}")
        return user_prompt, file_path


    async def get_started(self, user_prompt):
        """Start the processing of the user prompt."""
        
        logger.info("Hi I am Zinley, I will process your prompt now")

        prePrompt = await self.get_prePrompt(user_prompt)
        finalPrompt = prePrompt['processed_prompt']
        pipeline = prePrompt['pipeline']

        if pipeline == "0":
            print(user_prompt)
        elif pipeline == "1":
            await self.start_image_process(finalPrompt)

        logger.info(f"Done work for: `{user_prompt}`")
       
         
