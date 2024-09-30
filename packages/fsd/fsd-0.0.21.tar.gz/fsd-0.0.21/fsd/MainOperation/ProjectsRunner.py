import os
import aiohttp
import asyncio
import json
import sys
import subprocess
import time
import requests
import re

from fsd.util import utils

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.coding_agent.SelfHealingAgent import SelfHealingAgent
from fsd.coding_agent.FileManagerAgent import FileManagerAgent
from fsd.coding_agent.BugExplainer import BugExplainer
from fsd.util.utils import get_preferred_simulator_uuid
from .ProjectManager import ProjectManager
from .MainBuilderAgent import MainBuilderAgent
from fsd.log.logger_config import get_logger
from fsd.compile.CompileControllerAgent import CompileControllerAgent
logger = get_logger(__name__)

class ProjectsRunner:
    def __init__(self, repo):
        self.repo = repo
        self.directory_path = self.repo.get_repo_path()
        self.self_healing = SelfHealingAgent(repo)
        self.bugExplainer = BugExplainer(repo)
        self.project = ProjectManager(repo)
        self.fileManager = FileManagerAgent(repo)
        self.builderAgent = MainBuilderAgent(repo)
        self.compile = CompileControllerAgent(repo)

    def read_txt_files(self, files):
        """
        Get development plans for a list of txt files from OpenAI based on user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        all_file_contents = ""

        for file_path in files:
            file_content = self.read_file_content(file_path)
            if file_content:
                all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

        return all_file_contents

    def read_file_content(self, file_path):
        try:
            with open(file_path, "r") as file:
                return file.read()
        except Exception as e:
            print(f"Failed to read file {file_path}: {e}")
            return None

    async def run_project(self, basename, role, max_retries=20):
        tree = await self.get_tree_txt_files()
        result = await self.builderAgent.get_pipeline_plans(basename)
        logger.info("Printing the result of executing preparation")
        logger.info(result)
        pipeline = result["pipeline"]

        if pipeline == "1":
            return await self.run_xcode_project(basename, role)
        elif pipeline == "2":
            return await self.compile.start_CLI_compile_process("Run and open this project in the fastest way. Read the configuration file and tree structure to ensure the project runs properly. Modify anything necessary to achieve this goal, assuming all dependencies are installed.", basename)
        else:
            logger.info("This type of project can be built to test compile errors. Please run it and let me know what needs to be updated.")

        return []
       

    async def run_xcode_project(self, basename, role, max_retries=50):
        """
        Builds and runs an Xcode project using xcodebuild.

        Parameters:
        - basename (list): The base name list to update.
        - scheme (str): The scheme to build and run.
        - max_retries (int): Maximum number of retries for building the project.

        Returns:
        - output (str): The output of the xcodebuild command or an error message if the build fails.
        """

        scheme = self.repo.get_project_name()
        project_directory = self.repo.get_repo_path()
        logger.info(f"Building project at: {project_directory}, {scheme}")
        os.chdir(project_directory)

        # Get the preferred simulator UUID
        preferred_simulator_uuid = get_preferred_simulator_uuid()
        preferred_simulator_uuid = 'AB332A1B-27FA-4C37-A3F1-5F3A9D09B403'

        totalfile = set()
        fixing_related_files = set()

        xcodebuild_command = [
            'xcodebuild',
            '-scheme', scheme,
            '-destination', f'platform=iOS Simulator,id={preferred_simulator_uuid}',
            'build'
        ]

        print(f"xcodebuild_command: {xcodebuild_command}")

        retries = 0
        cleaned = False

        while retries < max_retries:
            self.self_healing.clear_conversation_history()
            self.bugExplainer.clear_conversation_history()

            self.bugExplainer.initial_setup(role)
            self.self_healing.initial_setup(role)

            try:
                if retries > 0 and not cleaned:
                    # Clean the build folder and reset the builder on subsequent retries
                    subprocess.run(['xcodebuild', 'clean', '-scheme', scheme], check=True, text=True, capture_output=True)
                    build_folder_path = os.path.join(project_directory, 'build')
                    if os.path.exists(build_folder_path):
                        subprocess.run(['rm', '-rf', build_folder_path], check=True)
                    subprocess.run(['xcodebuild', '-scheme', scheme, 'clean'], check=True, text=True, capture_output=True)
                    cleaned = True

                subprocess.run(xcodebuild_command, check=True, text=True, capture_output=True)


                self.self_healing.clear_conversation_history()
                self.bugExplainer.clear_conversation_history()

                logger.info(f"Build succeeded after {retries + 1} tries" if retries > 0 else "Build succeeded on the first try")
                return list(totalfile)

            except subprocess.CalledProcessError as e:
                logger.info("Oops! Something went wrong, I will work on the fix right now.")
                if e.returncode == 70:
                    logger.info("Build failed with exit status 70 or 65. I will finalize now and try again later.")
                    return list(totalfile)

                bug_log_content = e.stdout if e.stdout else e.stderr
                overview = self.repo.print_tree()
                damagefile, output_string = self.log_errors(bug_log_content)

                # Ensure basename list is updated without duplicates
                fixing_related_files.update(list(basename))
                fixing_related_files.update(damagefile)
                fixing_related_files.update(list(totalfile))

                # Retry OpenAI API call with delay on HTTP 429 error
                try:
                    logger.info("Start examining bugs and creating fixing plan")
                    fix_plans = await self.bugExplainer.get_bugFixed_suggest_requests(output_string, list(fixing_related_files), overview)
                    logger.info("Done examining bugs and creating fixing plan")

                    logger.info("Now, I am working on file processing")
                    file_result = await self.get_file_planning(fix_plans)
                    await self.process_creation(file_result)
                    logger.info("Completed processing files")

                    logger.info(f"Attempt to fix for {retries + 1} try")
                    steps = fix_plans.get('steps', [])

                    for step in steps:
                        file_name = step['file_name']
                        totalfile.update([file_name])

                    await self.self_healing.get_fixing_requests(steps)

                except requests.exceptions.HTTPError as http_error:
                    if http_error.response.status_code == 429:
                        wait_time = 2 ** retries
                        logger.info(f"Rate limit exceeded, retrying in {wait_time} seconds...")
                        time.sleep(wait_time)  # Exponential backoff
                    else:
                        raise

                retries += 1

        self.self_healing.clear_conversation_history()
        self.bugExplainer.clear_conversation_history()
        logger.info("Build failed after maximum retries")
        

    def log_errors(self, error_log):
        error_lines = []
        damaged_files = set()
        error_details = []

        # Regular expression to match file path and error line details
        error_regex = re.compile(r'(/[^:]+\.swift):(\d+):(\d+): error: (.+)')

        lines = error_log.split('\n')

        for line in lines:
            if "error:" in line.lower():
                print(line)
                error_lines.append(line)
                match = error_regex.search(line)
                if match:
                    full_file_path = match.group(1)
                    file_name = os.path.basename(full_file_path)  # Extract the filename
                    line_number = int(match.group(2))
                    column_number = int(match.group(3))
                    error_message = match.group(4)

                    damaged_files.add(file_name)

                    # Read the damaged file to get the specific line with the error
                    try:
                        with open(full_file_path, 'r') as swift_file:
                            swift_lines = swift_file.readlines()

                        if line_number <= len(swift_lines):
                            damaged_code = swift_lines[line_number - 1].strip()
                        else:
                            damaged_code = "Line number exceeds file length."

                        # Get additional context around the error line
                        error_details.append({
                            'file': file_name,
                            'line': line_number,
                            'column': column_number,
                            'message': error_message,
                            'code': damaged_code
                        })
                    except FileNotFoundError:
                        error_details.append({
                            'file': file_name,
                            'line': line_number,
                            'column': column_number,
                            'message': error_message,
                            'code': "File not found."
                        })
                else:
                    # If the error couldn't be parsed, add the original line
                    error_details.append({
                        'file': 'unknown',
                        'line': 'unknown',
                        'column': 'unknown',
                        'message': line.strip(),
                        'code': 'N/A'
                    })

        output_string = ""
        for error in error_details:
            output_string += f"Damaged code: {error['code']} - Error: {error['message']} - File path: {error['file']}\n"
            output_string += "\n" + "-"*80 + "\n\n"  # Adds a separator between errors

        damaged_files_list = list(damaged_files)  # Convert set to list before returning

        print(f"All error lines have been logged. {damaged_files_list}")

        return damaged_files_list, output_string

    async def get_file_planning(self, idea_plan):
        """Generate idea plans based on user prompt and available files."""
        return await self.fileManager.get_file_plannings(idea_plan)

    async def process_creation(self, data):
        # Check if 'Is_creating' is True
        if data.get('Is_creating'):
            # Extract the processes array
            processes = data.get('Adding_new_files', [])
            # Create a list of process details
            await self.project.execute_files_creation(processes)
        else:
            print("No new file to be added.")

    async def get_tree_txt_files(self):
        return self.repo.print_tree()