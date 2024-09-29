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

class FileManagerAgent:
    def __init__(self, repo):
        """
        Initialize the FileManagerAgent with directory path, API key, endpoint, deployment ID, and max tokens for API requests.

        Args:
            directory_path (str): Path to the directory containing .txt files.
            api_key (str): API key for Azure OpenAI API.
            endpoint (str): Endpoint URL for Azure OpenAI.
            deployment_id (str): Deployment ID for the model.
            max_tokens (int): Maximum tokens for the Azure OpenAI API response.
        """
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

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


    async def get_file_planning(self, idea):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            idea (str): The general plan idea.
            tree (str): The project structure.

        Returns:
            dict: JSON response with the plan or an error reason.
        """
            # Start of Selection
        prompt = (
                "From the provided development plan, build a JSON to add all new files to be created and list all Existing_files to be used. Provide only a JSON response without any additional text or Markdown formatting. "
                "Adding_new_files must include all new files that need to be created, excluding all dependency files (such as requirements.txt, package.json, Podfile, etc.). For image files, only include files with the .svg extension and exclude all other image types. "
                "Existing_files must include all existing full path for file names. "
                "Context_files must include all full path context file names only "
                "If no file needs to be created, follow this JSON format:\n"
                "{\n"
                "    \"Is_creating\": false,\n"
                "    \"Existing_files\": [\"/full/path/to/file1.extension\", \"/full/path/to/file2.extension\", \"/full/path/to/file3.extension\"],\n"
                "    \"Context_files\": [\"/full/path/to/file1.extension\", \"/full/path/to/file2.extension\", \"/full/path/to/file3.extension\"],\n"
                "    \"Adding_new_files\": []\n"
                "}\n\n"
                "If there are files that will need to be created, follow this JSON format:\n"
                "Pipeline should follow this rule, choose either 1 or 2 that most fits:\n"
                "1. If this is an Xcode project.\n"
                "2. If this is not an Xcode project.\n"
                "{\n"
                "    \"Is_creating\": true,\n"
                "    \"Existing_files\": [\"/full/path/to/file1.extension\", \"/full/path/to/file2.extension\", \"/full/path/to/file3.extension\"],\n"
                "    \"Context_files\": [\"/full/path/to/file1.extension\", \"/full/path/to/file2.extension\", \"/full/path/to/file3.extension\"],\n"
                "    \"Adding_new_files\": [\n"
                "        {\n"
                "            \"Title\": \"Creating a new file\",\n"
                "            \"Pipeline\": \"1 or 2\",\n"
                "            \"Function_to_call\": \"create_and_add_file_to_xcodeproj\",\n"
                "            \"Parameters\": {\n"
                "                \"project_root_path\": \"" + self.repo.get_repo_path() + "\",\n"
                "                \"relative_path\": \"full correct relative path from provided development plan, never skip project folder\",\n"
                "                \"file_name\": \"example.extension\"\n"
                "            }\n"
                "        }\n"
                "    ]\n"
                "}\n\n"
                "Existing_files must include the full path for each file.\n"
                "Context_files must include the full path for each file.\n"
                "relative_path must not overlap with project_root_path, must be full correct relative path from provided development plan.\n"
                f"project_root_path must be the same as \"{self.repo.get_repo_path()}\"\n"
                "Return only valid JSON without Markdown symbols or invalid escapes."
            )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is the development plan:\n{idea}\nThis is the current project structure:\n{self.repo.print_tree()}\n"
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0, 0)
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            return {
                "reason": str(e)
            }


    async def get_adding_file_planning(self, idea, tree):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            idea (str): The general plan idea.
            tree (str): The project structure.

        Returns:
            dict: JSON response with the plan or an error reason.
        """
        prompt = (
            "From the provided development plan, build a JSON to add all new files to be created. Provide only a JSON response without any additional text or Markdown formatting. "
            "Adding_new_files must include all new files that need to be created. "
            "Pipeline should follow this rule, choose either 1 or 2 that most fits:\n"
            "1. If this is an Xcode project.\n"
            "2. If this is not an Xcode project.\n"
            "If there are files that will need to be created, follow this JSON format:\n"
            "{\n"
            "    \"Is_creating\": true,\n"
            "    \"Adding_new_files\": [\n"
            "        {\n"
            "            \"Title\": \"Creating a new file\",\n"
            "            \"Function_to_call\": \"create_and_add_file_to_xcodeproj\",\n"
            "            \"Pipeline\": \"1 or 2\",\n"
            "            \"Parameters\": {\n"
            "                \"project_root_path\": \"" + self.repo.get_repo_path() + "\",\n"
            "                \"relative_path\": \"folder path\",\n"
            "                \"file_name\": \"example.extension\"\n"
            "            }\n"
            "        }\n"
            "    ]\n"
            "}\n\n"
            "If there are folders only that will need to be created, mark file_name = empty string.\n"
            "relative_path must not overlap with project_root_path, must only show the new path.\n"
            f"project_root_path must be the same as \"{self.repo.get_repo_path()}\"\n"
            "Return only valid JSON without Markdown symbols or invalid escapes."
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is the development plan:\n{idea}\nThis is the current project structure:\n{tree}\n"
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
            return {
                "reason": str(e)
            }


    async def get_moving_file_planning(self, idea, tree):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            idea (str): The general plan idea.
            tree (str): The project structure.

        Returns:
            dict: JSON response with the plan or an error reason.
        """
        prompt = (
            "From the provided development plan, build a JSON to move files. Provide only a JSON response without any additional text or Markdown formatting. "
            "Moving_files must include all files that need to be moved. "
            "Pipeline should follow this rule, choose either 1 or 2 that most fits:\n"
            "1. If this is an Xcode project.\n"
            "2. If this is not an Xcode project.\n"
            "If there are files that will need to be moved, follow this JSON format:\n"
            "{\n"
            "    \"Is_moving\": true,\n"
            "    \"Moving_files\": [\n"
            "        {\n"
            "            \"Title\": \"Moving a file\",\n"
            "            \"Function_to_call\": \"move_file_within_xcodeproj\",\n"
            "            \"Pipeline\": \"1 or 2\",\n"
            "            \"Parameters\": {\n"
            "                \"new_project_root_path\": \"" + self.repo.get_repo_path() + "\",\n"
            "                \"new_relative_path\": \"New folder path\",\n"
            "                \"file_name\": \"example.extension\"\n"
            "            }\n"
            "        }\n"
            "    ]\n"
            "}\n\n"
            "If there are folders only that will need to be created, mark file_name = empty string.\n"
            "new_relative_path must not overlap with new_project_root_path, must only show the new path.\n"
            f"new_project_root_path must be the same as \"{self.repo.get_repo_path()}\"\n"
            "Return only valid JSON without Markdown symbols or invalid escapes."
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is the development plan:\n{idea}\nThis is the current project structure:\n{tree}\n"
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
            logger.info(f"Failed: {e}")
            return {
                "reason": str(e)
            }

    async def get_moving_file_plannings(self, idea, tree):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            tree (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the plan.
        """
        all_file_contents = self.repo.print_tree()

        plan = await self.get_moving_file_planning(idea, all_file_contents)
        return plan

    async def get_adding_file_plannings(self, idea, tree):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            tree (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the plan.
        """
        all_file_contents = self.repo.print_tree()

        plan = await self.get_adding_file_planning(idea, all_file_contents)
        return plan

    async def get_file_plannings(self, idea):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            tree (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the plan.
        """
        plan = await self.get_file_planning(idea)
        return plan