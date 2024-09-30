import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.portkey import AIGateway
from json_repair import repair_json
from log.logger_config import get_logger
logger = get_logger(__name__)

class DependencyPrePromptAgent:
    def __init__(self, repo):
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
            logger.error(f"Failed to read file {file_path} in binary mode: {e}")
        
        return None

    async def get_prePrompt_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        all_file_contents = self.repo.print_tree()
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an ELITE DevOps engineering specialist with UNPARALLELED expertise in dependency management. METICULOUSLY analyze the provided project files and user prompt, then deliver a COMPREHENSIVE response in JSON format. STRICTLY ADHERE to these CRITICAL guidelines:\n\n"
                    "processed_prompt: Transform the user's prompt into a CRYSTAL-CLEAR, HIGHLY DETAILED directive focused EXCLUSIVELY on dependency installation. If not in English, provide an IMPECCABLE translation. ELEVATE the prompt by incorporating project-specific insights related ONLY to dependencies. Your refined prompt MUST serve as an AUTHORITATIVE roadmap for dependency installation. If pipeline is 2, EXPLICITLY DIRECT another AI agent on which CLI method to use (e.g., CocoaPods, npm, pip). Provide LEADING EXAMPLES for clarity.\n"
                    "pipeline: Determine the OPTIMAL course of action with SURGICAL PRECISION. Respond with a number (0, 1, or 2) based on these EXACTING criteria:\n"
                    "For dependency management:\n"
                    "0. Null operation: Employ ONLY when the user DOES NOT MENTION any dependencies to be installed or updated.\n"
                    "1. Expert intervention imperative: Utilize ONLY when the user EXPLICITLY MENTIONS manipulating an IDE for installation. In this case, EXPLAIN why CLI methods cannot be used.\n"
                    "2. Automated resolution feasible: SELECT THIS OPTION FOR ALL OTHER CASES. FORCE all dependency installations into CLI methods, even if not explicitly mentioned by the user. This includes ALL package managers like CocoaPods, npm, pip, etc.\n"
                    "explainer: For pipeline 1 scenarios, craft an EXHAUSTIVE, TECHNICALLY RIGOROUS explanation detailing why automated installation is IMPOSSIBLE. For pipeline 2, provide ONLY the following information: dependencies to be installed, their versions (if specified by the user or use latest if not mentioned), and the SPECIFIC CLI method for installation. Include ONLY CRITICAL warnings if absolutely necessary. This explanation MUST be delivered in the user's original language, ensuring UTMOST clarity and precision in communication.\n"
                    "The JSON response MUST STRICTLY adhere to this structure, with ABSOLUTELY NO DEVIATIONS:\n\n"
                    "{\n"
                    '    "processed_prompt": "EXHAUSTIVE, STRATEGICALLY ENHANCED user directive, ONLY dependency installation, IGNORE ALL integration parts",\n'
                    '    "pipeline": "0, 1, or 2",\n'
                    '    "explainer": ""\n'
                    "}\n\n"
                    "Your response MUST be a FLAWLESSLY formatted JSON object, DEVOID of ANY extraneous text, comments, or markdown elements. FOCUS SOLELY ON DEPENDENCY INSTALLATION AND MANAGEMENT. STRICTLY ENFORCE these guidelines in all cases."
                )
            },
            {
                "role": "user",
                "content": (
                    f"CRITICAL project context:\n{all_file_contents}\n\n"
                    f"User directive:\n{user_prompt}\n"
                )
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.info(f"Failed: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        plan = await self.get_prePrompt_plan(user_prompt)
        return plan
