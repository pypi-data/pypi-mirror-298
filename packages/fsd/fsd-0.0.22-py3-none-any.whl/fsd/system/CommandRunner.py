import subprocess
import os
import sys
import json
from log.logger_config import get_logger
from .FileContentManager import FileContentManager
from .OSEnvironmentDetector import OSEnvironmentDetector
from .ConfigAgent import ConfigAgent
from .TaskErrorPlanner import TaskErrorPlanner
logger = get_logger(__name__)


class CommandRunner:
    def __init__(self, repo):
        """
        Initializes the CommandRunner.
        """
        self.repo = repo
        self.config = ConfigAgent(repo)
        self.errorPlanner = TaskErrorPlanner(repo)
        self.config_manager = FileContentManager()  # Initialize CodeManager in the constructor
        self.detector = OSEnvironmentDetector()
        self.directory_path = repo.get_repo_path()
        self.max_retry_attempts = 3  # Set a maximum number of retry attempts

    async def get_config_requests(self, instructions, file_name):
        """Generate coding requests based on instructions and context."""

        main_path = file_name
        logger.info(f"Processing file: {file_name} in {main_path}")
        logger.info(f"Task: {instructions}")
        result = await self.config.get_config_requests(instructions, main_path)
        if main_path:
            await self.config_manager.handle_ai_response(main_path, result)
            logger.info(f"Done working on {file_name}")
        else:
            logger.warning(f"File not found: {file_name}")

    async def get_error_planner_requests(self, error, config_context, os_architecture, dependency_files):
        """Generate coding requests based on instructions and context."""
        result = await self.errorPlanner.get_task_plans(error, config_context, os_architecture, dependency_files)
        return result

    def run_command(self, command, method='bash'):
        """
        Runs a given command using the specified method.
        Shows real-time output during execution.
        Returns a tuple of (return_code, all_output).
        """
        try:
            # Use bash for all commands
            shell = True
            executable = '/bin/bash'

            # Check if the first part of the command is 'cd'
            if command.startswith('cd '):
                # Change the working directory
                new_dir = command[3:].strip()
                os.chdir(new_dir)
                logger.info(f"Changed directory to: {new_dir}")
                return 0, [f"Changed directory to: {new_dir}"]

            # Log the current working directory
            current_path = os.getcwd()
            logger.info(f"Running command: {command} in: {current_path}")

            # Start the process and capture output
            process = subprocess.Popen(
                command,
                shell=shell,
                executable=executable,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=current_path  # Explicitly set the working directory
            )

            # Read and print output in real-time
            output = []
            for line in process.stdout:
                line = line.strip()
                logger.info(line)
                print(line)
                output.append(line)

            for line in process.stderr:
                line = line.strip()
                logger.error(line)
                print(line)
                output.append(line)

            process.wait()  # Wait for the process to complete
            return_code = process.returncode

            # Combine output and error messages
            return return_code, output

        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return -1, [f"Command execution failed: {str(e)}"]

    def update_file(self, file_name, content):
        """
        Updates the content of a file.
        """
        try:
            with open(file_name, 'a') as file:
                file.write(content + '\n')
            logger.info(f"Successfully updated {file_name}")
            return f"Successfully updated {file_name}"
        except Exception as e:
            logger.error(f"Failed to update {file_name}: {str(e)}")
            return f"Failed to update {file_name}: {str(e)}"

    async def execute_steps(self, steps_json, dependency_files):
        """
        Executes a series of steps provided in JSON format.
        Asks for user permission before executing each step.
        Waits for each command to complete before moving to the next step.
        """
        steps = steps_json['steps']

        for step in steps:
            logger.debug(f"Step: {step['prompt']} - {step['command']}")
            user_permission = input(f"Press Tab to execute this step, or Enter to skip: ")

            if user_permission != '\t':
                logger.info("Step skipped by user.")
                continue

            logger.debug(f"Executing step: {step['prompt']}")

            retry_count = 0
            while retry_count < self.max_retry_attempts:
                if step['method'] == 'bash':
                    # Run the command and get the return code and output
                    return_code, command_output = self.run_command(step['command'])
                    
                    # Check for errors based on the return code
                    if return_code != 0:
                        error_message = '\n'.join(command_output)
                        logger.error(f"Command failed with return code {return_code}: {error_message}")
                        
                        # Check if the error suggests an alternative command
                        if "Did you mean" in error_message:
                            suggested_command = error_message.split("Did you mean")[1].strip().strip('"?')
                            logger.info(f"System suggested alternative command: {suggested_command}")
                            user_choice = input(f"Press Tab to execute the suggested command '{suggested_command}', or Enter to skip: ")
                            if user_choice == '\t':
                                logger.info(f"Executing suggested command: {suggested_command}")
                                return_code, command_output = self.run_command(suggested_command)
                                if return_code == 0:
                                    break  # Command executed successfully
                                else:
                                    # Update error_message with new command output
                                    error_message = '\n'.join(command_output)
                                    logger.error(f"Suggested command also failed with return code {return_code}: {error_message}")
                            else:
                                logger.info("User chose not to run the suggested command.")
                        
                        # Proceed to handle the error
                        fixing_steps = await self.get_error_planner_requests(error_message, step['prompt'], self.detector, dependency_files)
                        await self.execute_fixing_steps(fixing_steps, dependency_files)
                        retry_count += 1
                    else:
                        break  # Command executed successfully without errors
                elif step['method'] == 'update':
                    file_name = step.get('file_name', '')
                    if file_name != 'N/A':
                        await self.get_config_requests(step['prompt'], file_name)
                        logger.info(f"Successfully updated {file_name}")
                    else:
                        logger.warning("Update method specified but no file name provided.")
                    break
                else:
                    logger.error(f"Unknown method: {step['method']}")
                    break

            if retry_count == self.max_retry_attempts:
                logger.error(f"Step failed after {self.max_retry_attempts} attempts: {step['prompt']}")
                error_message = f"Step failed after {self.max_retry_attempts} attempts: {step['prompt']}"
                fixing_steps = await self.get_error_planner_requests(error_message, step['prompt'], self.detector)
                await self.execute_fixing_steps(fixing_steps, dependency_files)
                return f"Step failed after {self.max_retry_attempts} attempts: {step['prompt']}"

            logger.info("Step completed. Moving to the next step.")

        logger.info("All steps completed successfully")
        return "All steps completed successfully"

    async def execute_fixing_steps(self, steps_json, dependency_files):
        """
        Executes a series of steps provided in JSON format to fix dependency issues.
        Asks for user permission before executing each step.
        Waits for each command to complete before moving to the next step.
        """
        steps = steps_json['steps']

        for step in steps:
            logger.debug(f"Step: {step['error_resolution']} - {step['command']}")
            user_permission = input(f"Press Tab to execute this step, or Enter to skip: ")

            if user_permission != '\t':
                logger.info("Step skipped by user.")
                continue

            logger.debug(f"Executing step: {step['error_resolution']}")

            retry_count = 0
            while retry_count < self.max_retry_attempts:
                if step['method'] == 'bash':
                    # Run the command and get the return code and output
                    return_code, command_output = self.run_command(step['command'])
                    
                    # Check for errors based on the return code
                    if return_code != 0:
                        error_message = '\n'.join(command_output)
                        logger.error(f"Command failed with return code {return_code}: {error_message}")
                        # Proceed to handle the error
                        fixing_steps = await self.get_error_planner_requests(error_message, step['error_resolution'], self.detector, dependency_files)
                        await self.execute_fixing_steps(fixing_steps, dependency_files)
                        retry_count += 1
                    else:
                        break  # Command executed successfully without errors
                elif step['method'] == 'update':
                    file_name = step.get('file_name', '')
                    if file_name != 'N/A':
                        await self.get_config_requests(step['error_resolution'], file_name)
                        logger.info(f"Successfully updated {file_name}")
                    else:
                        logger.warning("Update method specified but no file name provided.")
                    break
                else:
                    logger.error(f"Unknown method: {step['method']}")
                    break

            if retry_count == self.max_retry_attempts:
                logger.error(f"Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}")
                error_message = f"Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}"
                fixing_steps = await self.get_error_planner_requests(error_message, step['error_resolution'], self.detector)
                await self.execute_fixing_steps(fixing_steps, dependency_files)
                return f"Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}"

            logger.info("Step completed. Moving to the next step.")

        logger.info("All fixing steps completed successfully")
        return "All fixing steps completed successfully"
