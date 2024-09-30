import os
import asyncio
import base64
from typing import Dict, List, Tuple
from fsd.log.logger_config import get_logger
from fsd.util.portkey import AIGateway
from PIL import Image
import io
import aiohttp

logger = get_logger(__name__)

class ImageGenAgent:
    """
    An agent responsible for generating images based on provided prompts and parameters.
    """

    def __init__(self, repo):
        self.repo = repo
        self.ai = AIGateway(model_type="dalle3")  # Initialize with DALL-E 3 model

    def validate_dimensions(self, dalle_dimension: str) -> str:
        """
        Validates the requested image dalle_dimension against supported sizes.
        """
        supported_sizes = ['1024x1024', '1792x1024', '1024x1792']
        if dalle_dimension in supported_sizes:
            return dalle_dimension
        else:
            logger.warning(f"Requested size '{dalle_dimension}' is not supported. Using '1024x1024' instead.")
            return '1024x1024'  # Default to a supported size

    def normalize_image_format(self, image_format: str) -> str:
        """
        Normalizes the image format string for compatibility with PIL.
        """
        format_upper = image_format.upper()
        if format_upper == 'JPG':
            return 'JPEG'
        else:
            return format_upper

    def save_image_data(self, image_data: str, file_path: str, image_format: str):
        """
        Saves base64-encoded image data to a file.
        """
        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))

            # Normalize image format
            image_format = self.normalize_image_format(image_format)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save the image
            image.save(file_path, format=image_format)
            logger.info(f"Image saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save image to {file_path}: {str(e)}")
            raise

    def save_and_resize_image(self, image_data: str, file_path: str, image_format: str, target_size: Tuple[int, int]):
        """
        Saves and resizes base64-encoded image data to a file.
        """
        try:
            # Decode the base64 image data
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))

            # Resize the image while maintaining aspect ratio
            image = self.resize_image_with_aspect_ratio(image, target_size)

            # Normalize image format
            image_format = self.normalize_image_format(image_format)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save the image
            image.save(file_path, format=image_format)
            logger.info(f"Image saved and resized to {target_size} at {file_path}")
        except Exception as e:
            logger.error(f"Failed to save and resize image: {str(e)}")
            raise

    def resize_image_with_aspect_ratio(self, image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """
        Resizes an image while maintaining aspect ratio and crops it to fit the target size.
        """
        target_width, target_height = target_size
        target_aspect = target_width / target_height

        # Resize the image while maintaining aspect ratio
        image_aspect = image.width / image.height
        if image_aspect > target_aspect:
            # Image is wider than target aspect ratio
            new_height = target_height
            new_width = int(new_height * image_aspect)
        else:
            # Image is taller than target aspect ratio
            new_width = target_width
            new_height = int(new_width / image_aspect)

        # Use Image.LANCZOS for high-quality downsampling
        image = image.resize((new_width, new_height), Image.LANCZOS)

        # Center crop the image
        left = (new_width - target_width) / 2
        top = (new_height - target_height) / 2
        right = (new_width + target_width) / 2
        bottom = (new_height + target_height) / 2
        image = image.crop((left, top, right, bottom))

        return image

    def extract_image_data(self, response):
        """
        Extracts image data from the API response, either base64-encoded or via URL.
        """
        try:
            # Check for errors in the response
            if hasattr(response, 'error') and response.error:
                error_message = getattr(response.error, 'message', 'Unknown error')
                raise Exception(f"API returned an error: {error_message}")

            # Extract the image data
            if hasattr(response, 'data') and response.data:
                data_item = response.data[0]
            else:
                raise ValueError("No image data found in the response.")

            image_data_b64 = getattr(data_item, 'b64_json', None)
            if image_data_b64:
                return image_data_b64, 'base64'
            else:
                image_url = getattr(data_item, 'url', None)
                if image_url:
                    return image_url, 'url'
                else:
                    raise ValueError("No image data (base64 or URL) found in the response.")
        except Exception as e:
            logger.error(f"Failed to extract image data from response: {str(e)}")
            logger.debug(f"Response content: {response}")
            raise

    async def fetch_and_save_image_from_url(self, url: str, file_path: str, image_format: str, target_size: Tuple[int, int] = None):
        """
        Fetches an image from a URL and saves (and optionally resizes) it to a file.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        image_bytes = await resp.read()
                        image = Image.open(io.BytesIO(image_bytes))

                        # Resize if target_size is specified
                        if target_size:
                            image = self.resize_image_with_aspect_ratio(image, target_size)

                        # Normalize image format
                        image_format = self.normalize_image_format(image_format)

                        # Ensure the directory exists
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)

                        # Save the image
                        image.save(file_path, format=image_format)
                        logger.info(f"Image fetched from URL and saved to {file_path}")
                    else:
                        raise Exception(f"Failed to fetch image from URL. HTTP status code: {resp.status}")
        except Exception as e:
            logger.error(f"Failed to fetch and save image from URL: {str(e)}")
            raise

    async def generate_image(self, prompt: str, dalle_dimension: str, actual_dimension: str, image_format: str, file_path: str):
        """
        Generates an image using the AI model and saves it to a file.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Validate and get a supported size
                supported_size = self.validate_dimensions(dalle_dimension)

                # Generate the image with the supported size
                response = self.ai.generate_image(
                    prompt=prompt,
                    size=supported_size
                )

                # Extract the image data
                image_data, data_type = self.extract_image_data(response)

                # Handle based on data type
                if data_type == 'base64':
                    if dalle_dimension != actual_dimension:
                        target_size = tuple(map(int, actual_dimension.lower().split('x')))
                        self.save_and_resize_image(
                            image_data=image_data,
                            file_path=file_path,
                            image_format=image_format,
                            target_size=target_size
                        )
                    else:
                        self.save_image_data(
                            image_data=image_data,
                            file_path=file_path,
                            image_format=image_format
                        )
                elif data_type == 'url':
                    # Fetch the image from the URL
                    target_size = tuple(map(int, actual_dimension.lower().split('x'))) if dalle_dimension != actual_dimension else None
                    await self.fetch_and_save_image_from_url(
                        url=image_data,
                        file_path=file_path,
                        image_format=image_format,
                        target_size=target_size
                    )
                else:
                    raise ValueError("Unsupported image data type.")

                logger.info(f"Image generated and saved to {file_path}")
                break  # Exit the retry loop on success
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)  # Wait before retrying
                else:
                    logger.error("Max retries reached. Giving up.")
                    logger.debug(f"Prompt: {prompt}")
                    raise

    async def process_image_generation(self, steps: List[Dict]):
        """
        Processes each image generation step sequentially.
        """
        for step in steps:
            try:
                await self.generate_image(
                    prompt=step['prompt'],
                    dalle_dimension=step['dalle_dimension'],
                    actual_dimension=step['actual_dimension'],
                    image_format=step['format'],
                    file_path=step['file_path']
                )
                logger.info(f"Successfully generated image for step: {step['file_path']}")
            except Exception as e:
                logger.error(f"Failed to generate image for step {step}: {str(e)}")
                continue

    async def generate_images(self, task: Dict):
        """
        Generates images based on the given task.
        """
        steps = task.get('steps', [])
        print(steps)
        if not steps:
            logger.warning("No steps provided for image generation.")
            return
        logger.info(f"Starting to generate {len(steps)} image(s).")
        await self.process_image_generation(steps)
        logger.info("Image generation process completed.")