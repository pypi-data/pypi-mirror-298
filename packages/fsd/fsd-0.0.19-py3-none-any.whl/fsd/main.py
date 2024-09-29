import git
import json
import os
import asyncio
import re
import time
import shutil  # Import shutil for copying directories
import subprocess
from concurrent.futures import ProcessPoolExecutor
from fsd.explainer.ExplainerController import ExplainerController  # Ensure this module is correctly imported and available
from fsd.coding_agent.ControllerAgent import ControllerAgent  # Ensure this module is correctly imported and available
from fsd.FirstPromptAgent import FirstPromptAgent
from fsd.io import InputOutput
from fsd.repo import GitRepo
from fsd.util import utils
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)
max_tokens = 4096
async def start(project_path):
    try:
        # check project_path exist
        if not os.path.exists(project_path):
            raise FileNotFoundError("Project path does not exist.")

        repo = GitRepo(project_path)
        
        explainer_controller = ExplainerController(repo)
        coding_controller = ControllerAgent(repo)

        while True:
            user_prompt_json = input("Enter your prompt (type 'exit' to quit): ")
            if user_prompt_json.startswith('/rollback'):
                repo.reset_previous_commit()
                continue
            user_prompt, file_attachment = parse_payload(user_prompt_json, project_path)
            result = await get_prePrompt(user_prompt)
            pipeline = result['pipeline']
            if pipeline == "1":
                logger.debug(f"Zinley: Sent explaining request for: {user_prompt}")
                await explainer_controller.get_started(user_prompt)
            elif pipeline == "2":
                logger.debug(f"Zinley: Sent coding request for: {user_prompt}")
                await coding_controller.get_started(user_prompt)
                repo.add_all_files(user_prompt)
                logger.debug(f"Zinley: Done coding request for: {user_prompt}")
            elif pipeline == "3":
                logger.debug(f"Zinley: Exit now")
                break
    except FileNotFoundError as e:
        logger.error(f"{e}")
        exit()
    except Exception as e:
        logger.info(f"An error occurred while copying the project: {e}")
        exit()
        
async def get_prePrompt(user_prompt):
    """Generate idea plans based on user prompt and available files."""
    first_prompt_controller = FirstPromptAgent(max_tokens)
    return await first_prompt_controller.get_prePrompt_plans(user_prompt)

def parse_payload(user_prompt_json, project_path):
    try:
        file_path = None
        data = json.loads(user_prompt_json)
        user_prompt = data.get("prompt", "")
        file_path = data.get("file_path", None)
        if file_path and os.path.exists(file_path):
            logger.info(f"{file_path} exists. Moving the file to {project_path}")
            # Check if the destination file already exists and remove it if necessary
            destination_file = os.path.join(project_path, os.path.basename(file_path))
            if os.path.exists(destination_file):
                os.remove(destination_file)
            shutil.move(file_path, project_path)
        else:
            logger.debug(f"{file_path} does not exists")
            file_path = None
    except json.JSONDecodeError:
        # If input is not valid JSON, treat it as plain text
        user_prompt = user_prompt_json
        logger.info(f"Received Plain Text Prompt: {user_prompt}")
    return user_prompt, file_path