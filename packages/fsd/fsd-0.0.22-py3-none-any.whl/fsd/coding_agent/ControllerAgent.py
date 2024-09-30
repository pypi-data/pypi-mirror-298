import os
import sys
import json

from .CodingAgent import CodingAgent
from .FormattingAgent import FormattingAgent
from .FileManagerAgent import FileManagerAgent
from .FileFinderAgent import FileFinderAgent
from .IdeaDevelopment import IdeaDevelopment
from .PrePromptAgent import PrePromptAgent
from .LanguageAgent import LanguageAgent
from .TaskPlanner import TaskPlanner

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.ImageAgent.ImageControllerAgent import ImageControllerAgent
from fsd.MainOperation.ProjectManager import ProjectManager
from fsd.MainOperation.ProjectsRunner import ProjectsRunner
from fsd.system.FileContentManager import FileContentManager
from fsd.Crawler.CrawlerAgent import CrawlerAgent
from fsd.Crawler.CrawlerTaskPlanner import CrawlerTaskPlanner
from fsd.dependency.DependencyControllerAgent import DependencyControllerAgent
from fsd.compile.CompileControllerAgent import CompileControllerAgent
from fsd.util import utils
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class ControllerAgent:
    def __init__(self, repo):
        self.repo = repo
        directory_path = self.repo.get_repo_path()
        self.directory_path = directory_path
        self.idea = IdeaDevelopment(repo)
        self.preprompt = PrePromptAgent(repo)
        self.taskPlanner = TaskPlanner(repo)
        self.coder = CodingAgent(repo)
        self.project = ProjectManager(repo)
        self.image = ImageControllerAgent(repo)
        self.compile = CompileControllerAgent(repo)
        self.runner = ProjectsRunner(repo)
        self.format = FormattingAgent(repo)
        self.fileManager = FileManagerAgent(repo)
        self.fileFinder = FileFinderAgent(repo)
        self.lang = LanguageAgent(repo)
        self.code_manager = FileContentManager()  # Initialize CodeManager in the constructor
        self.crawler = CrawlerAgent("fc-ce5f3e7178184ee387e17e9de608781f")
        self.crawlerPlaner = CrawlerTaskPlanner(repo)
        self.dependency = DependencyControllerAgent(repo)

    def filter_non_asset_files(self, file_set):
        # Define a set of common code file extensions
        code_extensions = {
            # Programming languages
            '.py', '.pyw',  # Python
            '.js', '.jsx', '.ts', '.tsx',  # JavaScript/TypeScript
            '.java',  # Java
            '.c', '.h', '.cpp', '.hpp', '.cc', '.cxx', '.hh', '.hxx', '.ino',  # C/C++
            '.cs',  # C#
            '.go',  # Go
            '.rb', '.rbw', '.rake', '.gemspec', '.rhtml',  # Ruby
            '.php', '.phtml', '.php3', '.php4', '.php5', '.php7', '.phps', '.phpt',  # PHP
            '.kt', '.kts',  # Kotlin
            '.swift',  # Swift
            '.m', '.mm',  # Objective-C
            '.r', '.rdata', '.rds', '.rda', '.rproj',  # R
            '.pl', '.pm', '.t',  # Perl
            '.sh', '.bash', '.bats', '.zsh', '.ksh', '.csh',  # Shell scripts
            '.lua',  # Lua
            '.erl', '.hrl',  # Erlang
            '.ex', '.exs',  # Elixir
            '.ml', '.mli', '.fs', '.fsi', '.fsx', '.fsscript',  # OCaml/F#
            '.scala', '.sbt', '.sc',  # Scala
            '.jl',  # Julia
            '.hs', '.lhs',  # Haskell
            '.clj', '.cljs', '.cljc', '.edn',  # Clojure
            '.groovy', '.gvy', '.gy', '.gsh',  # Groovy
            '.v', '.vh', '.sv', '.svh',  # Verilog/SystemVerilog
            '.vhd', '.vhdl',  # VHDL
            '.adb', '.ads', '.ada',  # Ada
            '.d', '.di',  # D
            '.nim', '.nims',  # Nim
            '.rs',  # Rust
            '.cr',  # Crystal
            # Markup and stylesheets
            '.html', '.htm', '.xhtml', '.jhtml',  # HTML
            '.css', '.scss', '.sass', '.less',  # CSS and preprocessors
            '.xml', '.xsl', '.xslt', '.xsd', '.dtd', '.wsdl',  # XML
            '.md', '.markdown', '.mdown', '.mkdn', '.mkd', '.rst', '.adoc', '.asciidoc',  # Markdown/AsciiDoc/ReStructuredText
            # Configuration files often edited directly
            '.json', '.yml', '.yaml', '.ini', '.cfg', '.conf', '.toml', '.plist', '.env', '.editorconfig',
            # iOS-specific
            '.nib', '.xib', '.storyboard',  # iOS
            # Android-specific
            '.gradle', '.pro', '.aidl', '.rs', '.rsh', '.xml',  # Android (note: '.rs' is Rust, so might need context-specific filtering)
            # Desktop app specific
            '.manifest', '.rc', '.resx', '.xaml', '.appxmanifest',  # App manifests and resource files
            # Web app specific
            '.asp', '.aspx', '.ejs', '.hbs', '.jsp', '.jspx', '.php', '.cfm',  # Server-side scripts
            # Database related
            '.sql',  # SQL scripts
            # Others
            '.tex', '.bib', '.txt',  # Text and documentation
            '.svg',  # Scalable Vector Graphics
        }

        # Use a set comprehension to filter files with code extensions
        code_files = {file for file in file_set if any(file.endswith(ext) for ext in code_extensions)}

        return code_files

    def is_coding_file(self, filename):
        # Define a set of common code file extensions
        code_extensions = {
            # Programming languages
            '.py', '.pyw',  # Python
            '.js', '.jsx', '.ts', '.tsx',  # JavaScript/TypeScript
            '.java',  # Java
            '.c', '.h', '.cpp', '.hpp', '.cc', '.cxx', '.hh', '.hxx', '.ino',  # C/C++
            '.cs',  # C#
            '.go',  # Go
            '.rb', '.rbw', '.rake', '.gemspec', '.rhtml',  # Ruby
            '.php', '.phtml', '.php3', '.php4', '.php5', '.php7', '.phps', '.phpt',  # PHP
            '.kt', '.kts',  # Kotlin
            '.swift',  # Swift
            '.m', '.mm',  # Objective-C
            '.r', '.rdata', '.rds', '.rda', '.rproj',  # R
            '.pl', '.pm', '.t',  # Perl
            '.sh', '.bash', '.bats', '.zsh', '.ksh', '.csh',  # Shell scripts
            '.lua',  # Lua
            '.erl', '.hrl',  # Erlang
            '.ex', '.exs',  # Elixir
            '.ml', '.mli', '.fs', '.fsi', '.fsx', '.fsscript',  # OCaml/F#
            '.scala', '.sbt', '.sc',  # Scala
            '.jl',  # Julia
            '.hs', '.lhs',  # Haskell
            '.clj', '.cljs', '.cljc', '.edn',  # Clojure
            '.groovy', '.gvy', '.gy', '.gsh',  # Groovy
            '.v', '.vh', '.sv', '.svh',  # Verilog/SystemVerilog
            '.vhd', '.vhdl',  # VHDL
            '.adb', '.ads', '.ada',  # Ada
            '.d', '.di',  # D
            '.nim', '.nims',  # Nim
            '.rs',  # Rust
            '.cr',  # Crystal
            # Markup and stylesheets
            '.html', '.htm', '.xhtml', '.jhtml',  # HTML
            '.css', '.scss', '.sass', '.less',  # CSS and preprocessors
            '.xml', '.xsl', '.xslt', '.xsd', '.dtd', '.wsdl',  # XML
            '.md', '.markdown', '.mdown', '.mkdn', '.mkd', '.rst', '.adoc', '.asciidoc',  # Markdown/AsciiDoc/ReStructuredText
            # Configuration files often edited directly
            '.json', '.yml', '.yaml', '.ini', '.cfg', '.conf', '.toml', '.plist', '.env', '.editorconfig',
            # iOS-specific
            '.nib', '.xib', '.storyboard',  # iOS
            # Android-specific
            '.gradle', '.pro', '.aidl', '.rs', '.rsh', '.xml',  # Android (note: '.rs' is Rust, so might need context-specific filtering)
            # Desktop app specific
            '.manifest', '.rc', '.resx', '.xaml', '.appxmanifest',  # App manifests and resource files
            # Web app specific
            '.asp', '.aspx', '.ejs', '.hbs', '.jsp', '.jspx', '.php', '.cfm',  # Server-side scripts
            # Database related
            '.sql',  # SQL scripts
            # Others
            '.tex', '.bib', '.txt',  # Text and documentation
            '.svg',  # Scalable Vector Graphics
        }

        # Check if the file has a code extension
        return any(filename.endswith(ext) for ext in code_extensions)

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

    async def get_prompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.prompt.get_prompt_plans(user_prompt)

    async def get_prePrompt(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.preprompt.get_prePrompt_plans(user_prompt)

    async def get_taskPlanner(self, instruction, file_lists):
        """Generate idea plans based on user prompt and available files."""
        return await self.taskPlanner.get_task_plans(instruction, file_lists)

    async def get_idea_plans(self, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.idea.get_idea_plans(user_prompt)

    async def get_bugs_plans(self, files, user_prompt):
        """Generate idea plans based on user prompt and available files."""
        return await self.bug_scanner.get_idea_plans(files, user_prompt)

    async def get_long_idea_plans(self, files, user_prompt, is_first):
        """Generate idea plans based on user prompt and available files."""
        return await self.long.get_idea_plans(files, user_prompt, is_first)

    async def get_file_planning(self, idea_plan):
        """Generate file planning based on idea plan and directory tree."""
        return await self.fileManager.get_file_plannings(idea_plan)

    async def get_adding_file_planning(self, idea_plan, tree):
        """Generate file planning for adding new files based on idea plan and directory tree."""
        return await self.fileManager.get_adding_file_plannings(idea_plan, tree)

    async def get_moving_file_planning(self, idea_plan, tree):
        """Generate file planning for adding new files based on idea plan and directory tree."""
        return await self.fileManager.get_moving_file_plannings(idea_plan, tree)

    async def get_formatting_files(self, prompt):
        """Generate formatting plans based on user prompt and directory tree."""
        return await self.fileFinder.get_file_plannings(prompt)

    async def run_requests(self, initial_instruction, request_list, role):
        """Run project requests."""
        return await self.runner.run_project(initial_instruction, request_list, role)

    async def process_creation(self, data):
        """Process the creation of new files based on provided data."""
        if data.get('Is_creating'):
            processes = data.get('Adding_new_files', [])
            await self.project.execute_files_creation(processes)

    async def process_moving(self, data):
        """Process the creation of new files based on provided data."""
        if data.get('Is_moving'):
            processes = data.get('Moving_new_files', [])
            await self.project.execute_files_creation(processes)

    async def build_existing_context(self, existing_files):
        """Build and return the context of existing files."""
        all_context = ""
        for path in existing_files:
            file_context = self.read_file_content(path)
            all_context += f"\n\nFile: {path}:\n{file_context}"

        return all_context

    async def get_coding_requests(self, instructions, context, file_lists, context_files, role, crawl_logs):
        """Generate coding requests based on instructions and context."""
        self.coder.initial_setup(context_files, instructions, context, role, crawl_logs)

        logger.info("Alright, let's get organized! Preparing the task and getting my digital gears turning.")
        plan = await self.get_taskPlanner(instructions, file_lists)
        logger.info(f"Completed preparing task!")

        is_first = True
        for step in plan.get('steps', []):
            file_name = step.get('file_name')
            if self.is_coding_file(file_name):
                main_path = file_name
                if main_path:
                    techStack = step.get('techStack')

                    logger.info(f"Processing file: {file_name}")

                    result = await self.coder.get_coding_requests(is_first, file_name, techStack)
                    await self.code_manager.handle_ai_response(main_path, result)

                    logger.info(f"Done working on {file_name}")
                    is_first = False
                else:
                    logger.warning(f"File not found: {file_name}")

    async def replace_all_code_in_file(self, file_path, new_code_snippet):
        """Replace the entire content of a file with the new code snippet."""
        try:
            with open(file_path, 'w') as file:
                file.write(new_code_snippet)
            logger.debug(f"The codes have been successfully written in... {file_path}.")
        except Exception as e:
            logger.error(f"Error writing code. Error: {e}")

    async def code_format_pipeline(self, finalPrompt, role):
        """Pipeline for code formatting."""
        logger.info("\n Now, I am working on `file processing`")
        file_result = await self.get_formatting_files(finalPrompt)
        logger.info(file_result)
        await self.process_creation(file_result)
        logger.info("\n Completed `processing files`")
        logger.info(f"Next, I will start the `formatting/refactoring phase`")
        working_files = file_result.get('working_files', [])
        logger.info(f"Formatting: {working_files}")
        if working_files:
            await self.format.get_formats(working_files, finalPrompt, role)
            self.format.clear_conversation_history()
            logger.info(f"Next, I will build to check if any compile error was made")
            await self.build_and_fix_compile_error(finalPrompt, working_files, role)
            logger.info(f"`Formatting/refactoring` phase done")
    

    async def build_and_fix_compile_error(self, initial_instruction, file_list, role):
        """Build project and fix compile errors."""
        await self.run_requests(initial_instruction, file_list, role)


    async def fix_compile_error_pipeline(self, initial_instruction, file_list, role):
        """Pipeline for fixing compile errors."""
        await self.build_and_fix_compile_error(initial_instruction, file_list, role)


    async def add_files_folders_pipeline(self, finalPrompt, role):
        """Pipeline for adding files and folders."""
        tree = self.repo.print_tree()
        logger.debug("add_files_folders_pipeline")
        logger.info("Now, I am working on file processing")
        file_result = await self.get_adding_file_planning(finalPrompt, tree)
        await self.process_creation(file_result)
        files = []
        if file_result.get('Is_creating'):
            processes = file_result.get('Adding_new_files', [])
            for process in processes:
                file_name = process['Parameters']['file_name']
                files.append(file_name)
        files = [file for file in files if file]

    async def move_files_folders_pipeline(self, finalPrompt, role):
        """Pipeline for adding files and folders."""
        tree = self.get_tree_txt_files()
        logger.debug("move_files_folders_pipeline")
        logger.info("Now, I am working on file processing")
        file_result = await self.get_moving_file_planning(finalPrompt, tree)
        logger.info(file_result)
        await self.process_moving(file_result)

    async def replace_code_pipeline(self, finalPrompt, role):
        """Pipeline for replacing code."""
        logger.debug("replace_code_pipeline")


    async def regular_code_task_pipeline(self, finalPrompt, role):
        """Pipeline for regular coding tasks."""
        logger.debug("regular_code_task_pipeline")

        self.idea.initial_setup(role)

        crawl_plan = await self.crawlerPlaner.get_crawl_plans(finalPrompt)
        crawl_logs = []
        if crawl_plan:
            for step in crawl_plan.get('crawl_tasks', []):
                crawl_url = step.get('crawl_url')
                crawl_format = step.get('crawl_format')
                if crawl_url:
                    logger.info(f"Reading: {crawl_url}")
                    result = self.crawler.process(crawl_url, crawl_format)
                    logger.info(f"Done reading: {crawl_url}")
                    crawl_logs.append({
                        'url': crawl_url,
                        'result': result
                    })
        
        logger.info("Now I will create an initial development plan for clarification.")

        idea_plan = ""

        if crawl_logs:
            idea_plan = await self.get_idea_plans(finalPrompt + f"crawled data: {crawl_logs}")
        else:
            idea_plan = await self.get_idea_plans(finalPrompt)

        logger.info(f"This is my initial development plan: {idea_plan}")

        while True:
            logger.info(
                "Are you satisfied with this development plan? Enter \"yes\" if satisfied, or provide feedback for modifications: ")

            user_prompt_json = input()
            user_prompt, _ = self.parse_payload(user_prompt_json)
            user_prompt = user_prompt.lower()

            if user_prompt == "" or user_prompt == "yes" or user_prompt == "y":
                break
            else:
                logger.info(f"Let's me update my development plan!")
                eng_prompt = await self.lang.get_language_plans(user_prompt, role)
                finalPrompt = finalPrompt + " " + eng_prompt
                self.idea.remove_latest_conversation()
                if crawl_logs:
                    idea_plan = await self.get_idea_plans(finalPrompt + f"crawled data: {crawl_logs}")
                else:
                    idea_plan = await self.get_idea_plans(finalPrompt)
                logger.info(f"This is my updated development plan: {idea_plan}")

        self.idea.clear_conversation_history()
        logger.info("Now, I am working on file processing")
        file_result = await self.get_file_planning(idea_plan)
        await self.process_creation(file_result)
        logger.info("Completed processing files")
        logger.info("Dependency checking")
        await self.dependency.get_started_coding_pipeline(idea_plan)
        logger.info("Done with dependency")
        logger.info(f"Next, I will start the coding phase")
        existing_files = file_result.get('Existing_files', [])
        new_adding_files = []
        context_files = file_result.get('Context_files', [])
        adding_new_files = file_result.get('Adding_new_files', [])
        if adding_new_files:
            for item in adding_new_files:
                file_info = item['Parameters']
                full_path = os.path.join(file_info['project_root_path'], file_info['relative_path'], file_info['file_name'])
                new_adding_files.append(full_path)

        final_working_files = set()
        final_working_files.update(existing_files)
        final_working_files.update(new_adding_files)
        final_working_files = self.filter_non_asset_files(final_working_files)
        all_context = await self.build_existing_context(list(final_working_files))
        await self.get_coding_requests(idea_plan, all_context, list(final_working_files), context_files, role, crawl_logs)
        await self.image.get_started(idea_plan)
        logger.info(f"Next, I will build to check if any compile error was made")
        await self.build_and_fix_compile_error(idea_plan, final_working_files, role)
    
        logger.info(f"Coding phase done")


    async def explainer_task_pipeline(self, finalPrompt, language, role):
        logger.debug("explainer_task_pipeline")
        logger.info(await self.get_explainer(finalPrompt, language, role))

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
        logger.info(f"Hi I am Zinley, I will process your prompt now: `{user_prompt}`")

        prePrompt = await self.get_prePrompt(user_prompt)
        role = prePrompt['role']
        finalPrompt = prePrompt['processed_prompt']
        pipeline = prePrompt['pipeline']

        if pipeline == "1":
            await self.fix_compile_error_pipeline("", list(), role)  # add a missing parameter
        elif pipeline == "2":
            await self.add_files_folders_pipeline(finalPrompt, role)
        elif pipeline == "3":
            await self.move_files_folders_pipeline(finalPrompt, role)
        elif pipeline == "4":
            await self.code_format_pipeline(finalPrompt, role)
        elif pipeline == "5":
            await self.regular_code_task_pipeline(finalPrompt, role)
        elif pipeline == "6":
            await self.dependency.get_started(finalPrompt)
        elif pipeline == "7":
            await self.compile.get_started(finalPrompt)
        elif pipeline == "8":
            await self.image.get_started(finalPrompt)

        logger.info(f"Done work for: `{user_prompt}`")
