import os
import sys
import json
import subprocess
import asyncio
import re

from .DependencyPrePromptAgent import DependencyPrePromptAgent
from .DependencyProjectAnalysAgent import DependencyProjectAnalysAgent
from .DependencyProjectAnalysForCodingAgent import DependencyProjectAnalysForCodingAgent
from .DependencyFileFinderAgent import DependencyFileFinderAgent
from .DependencyGuiderAgent import DependencyGuiderAgent
from .DependencyTaskPlanner import DependencyTaskPlanner


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.MainOperation.ProjectManager import ProjectManager
from fsd.coding_agent.LanguageAgent import LanguageAgent
from fsd.system.CommandRunner import CommandRunner
from fsd.system.OSEnvironmentDetector import OSEnvironmentDetector
from fsd.util import utils
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

HOME_DIRECTORY = os.path.expanduser('~')
HIDDEN_ZINLEY_FOLDER = '.zinley'

class DependencyControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.analysAgent = DependencyProjectAnalysAgent(repo)
        self.analysAgentCoding = DependencyProjectAnalysForCodingAgent(repo)
        self.preprompt = DependencyPrePromptAgent(repo)
        self.project = ProjectManager(repo)
        self.fileFinder = DependencyFileFinderAgent(repo)
        self.guider = DependencyGuiderAgent(repo)
        self.lang = LanguageAgent(repo)
        self.taskPlanner = DependencyTaskPlanner(repo)
        self.command = CommandRunner(repo)
        self.detector = OSEnvironmentDetector()
        self.directory_path = self.repo.get_repo_path()


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


    async def start_dependency_installation_process(self, instruction):
        os_architecture = self.detector
        file_result = await self.fileFinder.get_dependency_file_plannings()

        dependency_files = file_result.get('dependency_files', [])

        self.analysAgent.initial_setup(dependency_files, os_architecture)

        logger.info("Now I will create an initial dependency plan for clarification.")

        idea_plan = await self.analysAgentCoding.get_idea_plans(instruction)

        logger.info(f"This is my initial dependency plan: {idea_plan}")

        while True:
            logger.info(
                "Are you satisfied with this dependency plan? Enter \"yes\" if satisfied, or provide feedback for modifications: ")

            user_prompt_json = input()
            user_prompt, _ = self.parse_payload(user_prompt_json)
            user_prompt = user_prompt.lower()

            if user_prompt == "" or user_prompt == "yes" or user_prompt == "y":
                break
            else:
                logger.info(f"Let's me update my dependency plan!")
                eng_prompt = await self.lang.get_language_plans(user_prompt, "DevOps engineer")
                instruction = instruction + " " + eng_prompt
                self.analysAgent.remove_latest_conversation()
                idea_plan = await self.analysAgent.get_idea_plans(instruction)
                logger.info(f"This is my updated dependency plan: {idea_plan}")

        self.analysAgent.clear_conversation_history()
        logger.info("Alright, let's get organized! Preparing the task and getting my digital gears turning.")
        task = await self.taskPlanner.get_task_plan(idea_plan, os_architecture)
        await self.command.execute_steps(task)
        logger.info(f"{instruction}: Done")


    async def start_dependency_installation_process_coding_pipeline(self, instruction):

        logger.info(instruction)
        user_permission = input("Press Tab to proceed with dependency installation, or Enter to skip: ")
        if user_permission != '\t':
            logger.info("Dependency installation skipped.")
            return
        

        os_architecture = self.detector
        file_result = await self.fileFinder.get_dependency_file_plannings()
        dependency_files = file_result.get('dependency_files', [])
        self.analysAgentCoding.initial_setup(dependency_files, os_architecture)
        idea_plan = await self.analysAgentCoding.get_idea_plans(instruction)
        should_process_install_dependency = idea_plan.get('should_process_install_dependency')
        if should_process_install_dependency:
            logger.info(f"This is my initial dependency plan: {idea_plan.get('plan')}")

            while True:
                logger.info(
                    "Are you satisfied with this dependency plan? Enter \"yes\" if satisfied, or provide feedback for modifications: ")

                user_prompt_json = input()
                user_prompt, _ = self.parse_payload(user_prompt_json)
                user_prompt = user_prompt.lower()

                if user_prompt == "" or user_prompt == "yes" or user_prompt == "y":
                    break
                else:
                    logger.info(f"Let's me update my dependency plan!")
                    eng_prompt = await self.lang.get_language_plans(user_prompt, "DevOps engineer")
                    instruction = instruction + " " + eng_prompt
                    self.analysAgentCoding.remove_latest_conversation()
                    idea_plan = await self.analysAgentCoding.get_idea_plans(instruction)
                    should_process_install_dependency = idea_plan.get('should_process_install_dependency')

                    if should_process_install_dependency:
                        logger.info(f"This is my updated dependency plan: {idea_plan.get('plan')}")
                    else:
                        logger.info(f"{idea_plan.get('reason')}")
                        return

            self.analysAgentCoding.clear_conversation_history()
            logger.info("Alright, let's get organized! Preparing the task and getting my digital gears turning.")
            task = await self.taskPlanner.get_task_plan(idea_plan, os_architecture)
            await self.command.execute_steps(task, dependency_files)
            logger.info(f"{instruction}: Done")
        else:
            logger.info(f"{idea_plan.get('reason')}")



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
        explainer = prePrompt['explainer']

        if pipeline == "0":
            print(explainer)
        elif pipeline == "1":
            print(explainer)
            self.guider.initial_setup(user_prompt)
            self.guider.conversation_history.append({"role": "assistant", "content": f"{prePrompt}"})
            await self.guider_pipeline(user_prompt)
        elif pipeline == "2":
            await self.start_dependency_installation_process(finalPrompt)

        logger.info(f"Done work for: {user_prompt}")


    async def get_started_coding_pipeline(self, user_prompt):
            logger.info(f"get_started_coding_pipeline")
            """Start the processing of the user prompt."""
            logger.info("Hi I am Zinley, I will process your prompt now")

            prePrompt = await self.get_prePrompt(user_prompt)
            finalPrompt = prePrompt['processed_prompt']
            pipeline = prePrompt['pipeline']
            explainer = prePrompt['explainer']
           
            if pipeline == "0":
                print(explainer)
            elif pipeline == "2":
                await self.start_dependency_installation_process_coding_pipeline(finalPrompt)

            logger.info(f"Done work for: {user_prompt}")

