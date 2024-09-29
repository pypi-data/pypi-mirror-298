import os
import sys
import asyncio
import re
from json_repair import repair_json
import aiohttp
import json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class BugExplainer:
    def __init__(self, repo):
        self.repo = repo
        self.conversation_history = []
        self.ai = AIGateway('bedrock')

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def initial_setup(self, role):
        """Set up the initial prompt for the bug-fixing agent."""
        prompt = (
            f"You are a senior {role} working as a bug-fixing agent. Your task is to analyze the provided project context and current errors, identify the root cause of each bug, and provide detailed, structured steps to fix the project. "
            "Focus on identifying and fixing the root cause rather than applying fixes to all affected files. "
            "Please adhere to the following rules: "
            "(1) Each step must involve a single file only. \n"
            "(2) The 'file_name' must include the full path of the file that needs to be worked on. \n"
            "(3) The 'list_related_file_name' must include the full paths of files that could potentially be related to or impacted by the changes made in the working file; if there are no such files, return an empty list. \n"
            "(4) The 'is_new' flag should be set to 'True' if the file needs to be newly created (e.g., if it was accidentally deleted or is missing). Otherwise, set 'is_new' to 'False'. \n"
            "(5) The 'new_file_location' should specify the relative path and folder where the new file will be created, if necessary. \n"
            "The JSON response must strictly follow this format:\n\n"
            "{\n"
            "    \"steps\": [\n"
            "        {\n"
            "            \"Step\": 1,\n"
            "            \"file_name\": \"Full/Path/To/ExampleFile.extension\",\n"
            "            \"tech_stack\": \"Programming language used for this file\",\n"
            "            \"is_new\": \"True/False\",\n"
            "            \"new_file_location\": \"Relative/Path/To/Folder\",\n"
            "            \"list_related_file_name\": [\"Full/Path/To/RelatedFile1.extension\", \"Full/Path/To/RelatedFile2.extension\"],\n"
            "            \"Solution_detail_title\": \"Brief description of the issue being fixed.\",\n"
            "            \"all_comprehensive_solutions_for_each_bug\": \"Detailed descriptions and explanations, step by step, on how to fix each problem and bug. Include the exact scope of the damaged code and how to fix it.\"\n"
            "        }\n"
            "    ]\n"
            "}\n"
            "Do not add any additional content beyond the example above. "
            "Return only a valid JSON response without any additional text, Markdown symbols, or invalid escapes."
        )

        self.conversation_history.append({"role": "system", "content": prompt})


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

    async def get_bugFixed_suggest_request(self, bug_logs, all_file_contents, overview):
        """
        Get development plan for all txt files from Azure OpenAI based on user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            overview (str): Project overview description.

        Returns:
            dict: Development plan or error reason.
        """

        error_prompt = (
            f"Current working file:\n{all_file_contents}\n\n"
            f"Project overview:\n{overview}\n\n"
            f"Bug logs:\n{bug_logs}\n\n"
            "Return only a valid JSON format bug fix response without additional text or Markdown symbols or invalid escapes.\n\n"
        )

        self.conversation_history.append({"role": "user", "content": error_prompt})

        try:
            response = await self.ai.prompt(self.conversation_history, 4096, 0.6, 0.7)
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.info(f"Failed: {e}")
            return {
                "reason": e
            }


    async def get_bugFixed_suggest_requests(self, bug_logs, files, overview):
        """
        Get development plans for a list of txt files from Azure OpenAI based on user prompt.

        Args:
            bug_logs (str): bug_logs.
            files (list): List of file paths.
            overview (str): Overview description.

        Returns:
            dict: Development plan or error reason.
        """
        # Step to remove all empty files from the list
        filtered_lists = [file for file in files if file]

        logger.debug(f"Scanning: {filtered_lists}")

        all_file_contents = ""

        # Scan needed files based on the filtered list
        final_files_paths = filtered_lists

        for file_path in final_files_paths:
            try:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}\n{file_content}"
            except Exception as e:
                all_file_contents += f"\n\nFailed to read file {file_path}: {str(e)}"

        # Get the bug-fixed suggestion request
        plan = await self.get_bugFixed_suggest_request(bug_logs, all_file_contents, overview)
        return plan