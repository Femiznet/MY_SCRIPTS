from lib import get_directory, organize_folder
from log import logger


if __name__ == "__main__":

    logger.info("Starting program: FILE ORGANIZER")

    try:
        directory = get_directory()

        organize_folder(directory)

    except NotADirectoryError as e:
        logger.info(f"ERROR: {e}")
    except TypeError as e:
        logger.info(f"ERROR: {e}")
    except Exception as e:
        print("Error: Something went wrong")
        logger.debug(e)

    logger.info("Program completed")
