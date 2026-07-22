from lib import get_directory, organize_folder
from lib import OrganizeFolderError, InvalidDirectoryError
from log import logger

def main():

    logger.info("Starting program: FILE ORGANIZER")

    try:

        directory = get_directory()
        organize_folder(directory)

    except InvalidDirectoryError as e:
        logger.info(f"ERROR: {e}")
    except OrganizeFolderError as e:
        print("Error: Something went wrong")
        logger.debug(e)

    logger.info("Program completed")


if __name__ == "__main__":
    main()