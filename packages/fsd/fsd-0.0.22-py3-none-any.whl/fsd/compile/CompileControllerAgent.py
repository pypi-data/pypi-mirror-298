import os
import sys
import json
import subprocess
import asyncio
import re

from .CompilePrePromptAgent import CompilePrePromptAgent
from .CompileProjectAnalysAgent import CompileProjectAnalysAgent
from .CompileFileFinderAgent import CompileFileFinderAgent
from .CompileGuiderAgent import CompileGuiderAgent
from .CompileTaskPlanner import CompileTaskPlanner


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.coding_agent.LanguageAgent import LanguageAgent
from fsd.system.CompileCommandRunner import CompileCommandRunner
from fsd.system.OSEnvironmentDetector import OSEnvironmentDetector
from fsd.util import utils
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class CompileControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.analysAgent = CompileProjectAnalysAgent(repo)
        self.preprompt = CompilePrePromptAgent(repo)
        self.fileFinder = CompileFileFinderAgent(repo)
        self.guider = CompileGuiderAgent(repo)
        self.lang = LanguageAgent(repo)
        self.taskPlanner = CompileTaskPlanner(repo)
        self.command = CompileCommandRunner(repo)
        self.detector = OSEnvironmentDetector()

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)


    async def guider_pipeline(self, user_prompt):
        """Pipeline for regular coding tasks."""
        print('guider_pipeline')

        while True:
            user_prompt_json = input("Do you need more help with dependency?: ")
            guide = await self.guider.get_guider_plans(user_prompt_json)
            finalPrompt = guide['processed_prompt']
            pipeline = guide['pipeline']
            explainer = guide['explainer']

            if pipeline == "0":
                break
            elif pipeline == "1":
                print(explainer)
            elif pipeline == "2":
                print(guide)
                await self.start_dependency_installation_process(user_prompt)
                break


    async def start_CLI_compile_process(self, instruction, code_files):
        os_architecture = self.detector

        file_result = await self.fileFinder.get_compile_file_plannings(instruction)

        compile_files = file_result.get('crucial_files', [])

        logger.info(f"This is compile related files: {compile_files}")

        self.analysAgent.initial_setup(compile_files, os_architecture)

        logger.info("Now I will create an initial compile plan for clarification.")

        idea_plan = await self.analysAgent.get_idea_plans(instruction)

        logger.info(f"This is my initial compile plan: {idea_plan}")

        while True:
            logger.info(
                "Are you satisfied with this compile plan? Enter \"yes\" if satisfied, or provide feedback for modifications: ")

            user_prompt_json = input()
            user_prompt, _ = self.parse_payload(user_prompt_json)
            user_prompt = user_prompt.lower()

            if user_prompt == "" or user_prompt == "yes" or user_prompt == "y":
                break
            else:
                logger.info(f"Let's me update my compile plan!")
                eng_prompt = await self.lang.get_language_plans(user_prompt, "DevOps engineer")
                instruction = instruction + " " + eng_prompt
                self.analysAgent.remove_latest_conversation()
                idea_plan = await self.analysAgent.get_idea_plans(instruction)
                logger.info(f"This is my updated compile plan: {idea_plan}")

        self.analysAgent.clear_conversation_history()
        logger.info("Alright, let's get organized! Preparing the task and getting my digital gears turning.")
        task = await self.taskPlanner.get_task_plan(idea_plan, os_architecture)
        await self.command.execute_steps(task, compile_files, code_files)
        logger.info(f"{instruction}: Done")


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
            logger.info("No compilation needed.")
        elif pipeline == "1":
            print(prePrompt)
        elif pipeline == "2":
            await self.start_CLI_compile_process(finalPrompt)

        logger.info(f"Done work for: `{user_prompt}`")
         
