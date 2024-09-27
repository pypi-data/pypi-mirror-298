from typing import Union
import numpy as np
from PIL import Image


def load_image(file_path: str) -> Image.Image:
    """
    Loads an image from the specified file path using Pillow.

    :param file_path: The path to the image file to be loaded.
    :returns: The loaded image as a PIL Image object.
    """
    image = Image.open(file_path)
    image.load()  # Ensure the image is fully loaded
    return image


def save_image(image: Image.Image, file_path: str, format: str = None) -> None:
    """
    Saves a given image to the specified file path using Pillow.

    :param image: The PIL Image object to be saved.
    :param file_path: The path where the image will be saved.
    :param format: Optional. The format to use for saving (e.g., 'JPEG', 'PNG'). 
                   If None, the format is inferred from the file extension.
    :returns: None
    """
    image.save(file_path, format=format)


def _load_or_return_image(image: Union[Image.Image, str]) -> Image.Image:
    """
    Loads an image if a file path is provided, otherwise returns the image.

    :param image: Either a PIL Image object or a file path to an image.
    :returns: A PIL Image object.
    """
    if isinstance(image, str):
        return load_image(image)
    return image


def crop_image(image: Union[Image.Image, str], size: tuple[int, int]) -> Image.Image:
    """
    Crops an image from the center to the specified size. 
    If the specified size is larger than the image, the extra area is filled with transparent black pixels.

    :param image: Either a PIL Image object or a file path to an image.
    :param size: A tuple (width, height) specifying the size of the crop.
    :returns: A new PIL Image object that is the cropped version of the original image.
    """
    image = _load_or_return_image(image)

    target_width, target_height = size
    original_width, original_height = image.size

    # Calculate the center crop box
    left = max((original_width - target_width) // 2, 0)
    top = max((original_height - target_height) // 2, 0)
    right = min(left + target_width, original_width)
    bottom = min(top + target_height, original_height)

    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))

    # If the crop size is larger than the original image, create a new image with transparency
    if target_width > original_width or target_height > original_height:
        # Create a new transparent image
        new_image = Image.new('RGBA', size, (0, 0, 0, 0))  # Transparent black

        # Calculate the position to paste the cropped image onto the new image
        paste_x = (target_width - cropped_image.width) // 2
        paste_y = (target_height - cropped_image.height) // 2

        # Paste the cropped image onto the transparent background
        new_image.paste(cropped_image, (paste_x, paste_y))
        return new_image

    # If no padding is needed, just return the cropped image
    return cropped_image


def resize_image(image: Union[Image.Image, str], size: tuple[int, int], keep_aspect_ratio: bool = False) -> Image.Image:
    """
    Resizes an image to the specified size. If keep_aspect_ratio is True, the image
    will be resized while maintaining its aspect ratio, and any extra space will be filled
    with transparent pixels.

    :param image: Either a PIL Image object or a file path to an image.
    :param size: A tuple (width, height) specifying the target size.
    :param keep_aspect_ratio: Boolean to decide whether to maintain the original aspect ratio. Default is False.
    :returns: A new PIL Image object that is the resized version of the original image.
    """
    image = _load_or_return_image(image)

    if keep_aspect_ratio:
        original_width, original_height = image.size
        target_width, target_height = size

        # Calculate the new size while keeping the aspect ratio
        aspect_ratio = original_width / original_height
        if target_width / target_height > aspect_ratio:
            new_height = target_height
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = target_width
            new_height = int(new_width / aspect_ratio)

        # Resize the image with the new dimensions
        resized_image = image.resize(
            (new_width, new_height), Image.Resampling.LANCZOS)

        # Create a new transparent image with the target size
        new_image = Image.new("RGBA", size, (0, 0, 0, 0))

        # Paste the resized image onto the new transparent image
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        new_image.paste(resized_image, (paste_x, paste_y))

        return new_image
    else:
        # Resize directly to the target size without keeping aspect ratio
        return image.resize(size, Image.Resampling.LANCZOS)


def thumbnail(image: Union[Image.Image, str], size: tuple[int, int]) -> Image.Image:
    """
    Creates a thumbnail of the specified size by first resizing the image while
    maintaining the aspect ratio, then cropping it to fit the exact size.

    :param image: Either a PIL Image object or a file path to an image.
    :param size: A tuple (width, height) specifying the size of the thumbnail.
    :returns: A new PIL Image object that is the thumbnail version of the original image.
    """
    image = _load_or_return_image(image)

    # Step 1: Resize the image while maintaining aspect ratio
    resized_image = resize_image(image, size, keep_aspect_ratio=True)

    # Step 2: Crop the resized image to the exact size
    cropped_thumbnail = crop_image(resized_image, size)

    return cropped_thumbnail
