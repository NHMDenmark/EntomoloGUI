import logging
import requests
import numpy as np

from PIL import Image
from logging import handlers
from PIL.ImageQt import ImageQt


def init_logger(debug):
    """Initialize Logger

    Args:
        debug (bool): Sets debug mode for logging. Default False.

    Returns:
        logger: logger instance
    """
    # sets format
    logFormatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s in %(pathname)s:%(lineno)d"
    )
    logger = logging.getLogger()

    # sets logging level
    log_level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(log_level)

    # Use rotating file handler so log file does not get too big
    fileHandler = handlers.RotatingFileHandler(
        "log.log", maxBytes=(1048576 * 5), backupCount=2
    )
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    # Log to console as well
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    return logger


def try_url(url):
    """Try Url
    Attempts to get a response from a url. Returns response if successful, None if failed.

    Args:
        url (_type_): _description_

    Returns:
        (response or None): returns response if successful, None if failed
    """
    log = logging.getLogger("UThread")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as err:
        log.debug(
            f'RequestException encountered connecting to url: "{url}", Exception raised: "{err}"'
        )
    except requests.exceptions.HTTPError as errh:
        log.debug(
            f'HTTPError encountered connecting to url: "{url}", Exception raised: "{errh}"'
        )
    except requests.exceptions.ConnectionError as errc:
        log.debug(
            f'ConnectionError encountered connecting to url: "{url}", Exception raised: "{errc}"'
        )
    except requests.exceptions.Timeout as errt:
        log.debug(
            f'Timeout encountered connecting to url: "{url}", Exception raised: "{errt}"'
        )
    except Exception as e:
        log.debug(f'Error connecting to url: "{url}", Exception raised: "{e}"')

    return None


def make_x_image(width, height):
    """Make X Image
    Returns an image of size (width, height) with a large white X in the center
    This is a placeholder image for when something has gone wrong connecting to the camera

    Args:
        width (int): width of the image to be returned
        height (int): height of the image to be returned

    Returns:
        (ImageQt): ImageQt format image of a x image
    """
    size = max(width, height)
    thickness = 5  # sets the thickness of the X in pixels

    # make a square x first, larger than the desired image,
    #   this makes it easier to generate the x
    big_x = np.abs(np.add.outer(np.arange(size), -np.arange(size))) < thickness
    big_x = (big_x | np.fliplr(big_x)).astype("uint8") * 255
    big_x = np.repeat(big_x[..., np.newaxis], 3, axis=-1)

    start_row = big_x.shape[0] // 2 - height // 2
    end_row = big_x.shape[0] // 2 + height // 2
    start_col = big_x.shape[0] // 2 - width // 2
    end_col = big_x.shape[0] // 2 + width // 2

    # reduce the size of the image to the requested width and height
    big_x = big_x[start_row:end_row, start_col:end_col]
    return ImageQt(Image.fromarray(big_x))
