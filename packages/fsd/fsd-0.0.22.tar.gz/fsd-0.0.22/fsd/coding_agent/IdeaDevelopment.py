import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class IdeaDevelopment:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway('bedrock')

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, role):
        """
        Initialize the conversation with a system prompt and user context.
        """


        all_file_contents = self.repo.print_summarize_with_tree()

            # Start of Selection
            # Start of Selection
        system_prompt = (
                    f"You are a senior {role}. Your task is to thoroughly analyze the provided project files and develop a comprehensive development plan. Follow these guidelines:\n\n"

                    "**Guidelines:**\n"
                    "- **Enterprise-Level Focus:** Ensure the plan meets enterprise standards for scalability, performance, and security.\n"
                    "- If the user provides a link to external resources, scraping, or documentation, assume that the data will be provided in a subsequent step through the Zinley crawler agent. Guide the coder to utilize this data correctly within the development plan.\n"
                    "- Ensure all references to external data sources are properly documented and integrated into the plan without directly including the data.\n"
                    "- If the user requests to read a website, note that the data will be provided as an example later and will be provided again during the coding stage. Make sure to follow the user's requests regarding website data.\n"
                    "- **No Code in Plan:** Focus on technical and architectural planning; do not include source code.\n"
                    "- **File Integrity:** Modify content within existing files without renaming them. Create new files if necessary. Clearly describe how each file will be updated or integrated.\n"
                    "- **Image Handling:** All image assets must adhere to the following detailed specifications to ensure clarity and consistency. Do not make any assumptions about directories or file name or which one to be created/used; specify each aspect explicitly.\n"
                    "    - **File Formats:**\n"
                    "        - Use `.svg` for icons, logos, illustrations, simple graphics, and interactive graphics.\n"
                    "        - Use `.png` or `.jpg` for product representations and large images that require high quality.\n"
                    "    - **File Sizes:**\n"
                    "        - **Icons and Logos:** Dimensions must be between 24x24px and 512x512px.\n"
                    "        - **Illustrations and Simple Graphics:** Dimensions must not exceed 1024x1024px.\n"
                    "        - **Product Representations and Large Images:** Dimensions must not exceed 2048x2048px.\n"
                    "    - **Directory Structure:**\n"
                    "        - Store icons and logos in the `assets/icons/` directory.\n"
                    "        - Store illustrations and simple graphics in the `assets/illustrations/` directory.\n"
                    "        - Store product representations and large images in the `assets/products/` directory.\n"
                    "    - **Naming Conventions:**\n"
                    "        - Use descriptive and specific file names for each asset (e.g., `latte.svg`, `cappuccino.svg`).\n"
                    "    - **Plan Submission:**\n"
                    "        - All new files and images must have an exact, detailed plan. For example:\n"
                    "            - Create individual `.svg` files for each menu item:\n"
                    "                - `latte.svg` - Dimensions: 128x128px.\n"
                    "                - `cappuccino.svg` - Dimensions: 128x128px.\n"
                    "- **README Documentation:** Mention that a comprehensive README should be included or updated, but do not provide the README details in this plan. Focus solely on technical implementation and structural planning.\n"
                    "- **File Structure and Naming:** Propose a clear, logical file and folder structure to support long-term use and expansion. Use meaningful names to avoid conflicts. Describe the desired directory structure and navigation path.\n"
                    "- **UI Design:** Ensure a well-designed UI if the task involves UI elements, whether for web or app. Create a compelling UI for each platform individually.\n\n"

                    "**2. Must Always Strictly Follow this Guide:**\n"

                    "**2.0 Ultimate Goal:**\n"
                    "- Clearly state the project's ultimate goal. Explain what the final product should achieve, who the end users are, and how this project will meet their needs. Provide a concise summary of the main objectives and deliverables.\n\n"

                    "**2.1 Existing Files (Must follow, mention if present):**\n"
                    "- Detail what needs to be implemented in these files.\n"
                    "- Suggest algorithms, special dependencies, functions, or classes to be used for specific purposes.\n"
                    "- Identify any dependencies or relationships with other files that may impact or be impacted by these changes. Describe how these relationships affect the overall system.\n"
                    "- Detail the usage of any image, video, or audio assets in these files, specifying where they are included, what they represent, and why they are necessary for functionality or user experience. Include exact filenames and placement details. For new images, use the `.svg` format whenever possible.\n\n"

                    "**2.2 New Files (Must follow, mention if to be created or not):**\n"
                    "- Structure files at an enterprise level, avoiding combining unrelated functionalities into single files.\n"
                    "- Detail what needs to be implemented in these new files.\n"
                    "- Suggest algorithms, special dependencies, functions, or classes to be used for specific purposes.\n"
                    "- Describe how each new file will integrate with existing files and systems, ensuring smooth interoperability. Detail any data flow, API calls, or interactions that are necessary, and specify how this integration will be achieved.\n"
                    "- Detail the usage of any image, video, or audio assets in these files, specifying where they are included, what they represent, and why they are necessary for functionality or user experience. Include exact filenames and placement details. For new images, use the `.svg` format whenever possible.\n"
                    "- For all new images, provide a detailed description, including the content, style, color scheme, dimensions, and purpose. Specify the exact dimensions that best fit the project's needs, adhering to the size guidelines mentioned earlier.\n"
                    "    - Create individual `.svg` files for each menu item (e.g., `latte.svg`, `cappuccino.svg`, etc.).\n"
                    "    - Dimensions: 128x128px for each icon.\n"
                    "- Provide the complete new tree structure expected after the task is fully built.\n"
                    f"- Must mention the main new project folder where all new files will be added, if applicable, as it will be the new home for all new files. Also, must mention the current project root path: {self.repo.get_repo_path()}."

                    "**2.3 Dependencies (Must follow, mention if needed or not):**\n"
                    "- Provide a list of dependencies required for the current task only, indicating which are already installed and which need installation. Include their roles and relevance to the project.\n"
                    "- Use the latest version of each dependency. Do not specify version numbers unless the user explicitly requests a specific version.\n"
                    "- Include considerations for dependency updates or replacements that might improve security or performance. Justify any recommendations for changes.\n"
                    "- Only include dependencies that can be installed through CLI commands. Always mention the specific CLI installation method (e.g., npm, pip, CocoaPods) for each dependency.\n"
                    "- Provide the exact CLI command for installing each dependency. Do not include version numbers unless specified by the user.\n"
                    "- Skip any dependencies that require IDE manipulation or cannot be installed via CLI.\n"
                    "- Prioritize compatibility when selecting dependencies, ensuring they work well together and with the existing system.\n\n"

                    "**2.4 Existing Context Files (Must follow, mention if present):**\n"
                    "- Provide a list of relevant existing context files necessary for understanding and completing the task, such as configuration files, environment settings, or other critical resources. Explain their importance and how they will be used.\n"
                    "- Exclude non-essential files like assets, development environment configurations, and IDE-specific files. Clarify why these files are not included.\n"
                    "- Ensure there is no overlap with Existing Files (2.1) and New Files (2.2). Clearly differentiate their roles and usage. Provide explanations to avoid confusion.\n"
                    "- Existing Context Files will be used for RAG purposes, so please list relevant files needed for these tasks if any.\n"
                    "- If no relevant context files are found, mention this briefly, confirming that all necessary files have been accounted for. Clearly state that all essential files are included and identified.\n"
                    "- Return a well-formatted markdown.\n\n"

                    "**(No need to add anything extra from the guidelines):**\n"
                )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current project structure and files summary:\n{all_file_contents}\n"})
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
            response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            return response.choices[0].message.content
        except Exception as e:
            logger.info(f"Failed: {e}")
            return {
                "reason": str(e)
            }

    async def get_idea_plans(self, user_prompt):
        return await self.get_idea_plan(user_prompt)
            
