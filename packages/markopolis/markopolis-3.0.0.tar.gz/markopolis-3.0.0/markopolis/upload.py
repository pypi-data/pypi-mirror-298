import requests
from pathlib import Path
from loguru import logger
import sys
import fire
import os

logger.remove()
logger.add(sys.stdout, level="INFO")


def mdsync(path=".", api_key=None):
    domain = os.getenv("MARKOPOLIS_DOMAIN")
    api_key = os.getenv("MARKOPOLIS_API")
    if not api_key:
        logger.error("API key is required")
        return

    api_endpoint = f"{domain}/api/upload"

    headers = {"X-API-Key": api_key}

    path = Path(path)
    if not path.is_dir():
        logger.error(f"{path} is not a valid directory")
        return

    # Get list of all files in the local directory
    local_files = set()
    for file_path in path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in [
            ".md",
            ".markdown",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
        ]:
            relative_path = str(file_path.relative_to(path))
            local_files.add(relative_path)

    # Upload local files
    for file_path in path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in [
            ".md",
            ".markdown",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
        ]:
            relative_path = file_path.relative_to(path)
            url = f"{relative_path}"
            logger.info(f"url: {url}")
            try:
                with open(file_path, "rb") as file:
                    files = {"file": file}
                    data = {"url": url}
                    logger.info(f"Uploading {file_path}")
                    response = requests.post(
                        api_endpoint, files=files, data=data, headers=headers
                    )
                    if response.status_code == 200:
                        logger.info(f"Successfully uploaded {file_path}")
                    else:
                        logger.error(
                            f"Failed to upload {file_path}. Status code: {response.status_code}"
                        )
            except Exception as e:
                logger.error(f"Error uploading {file_path}: {str(e)}")

    # Get list of files from the API
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            remote_files = set(response.json())
        else:
            logger.error(
                f"Failed to get file list from API. Status code: {response.status_code}"
            )
            return
    except Exception as e:
        logger.error(f"Error getting file list from API: {str(e)}")
        return

    # Delete files not present locally
    files_to_delete = remote_files - local_files
    for file_to_delete in files_to_delete:
        try:
            logger.info(f"Deleting {file_to_delete}")
            response = requests.delete(
                api_endpoint, json={"url": file_to_delete}, headers=headers
            )
            if response.status_code == 200:
                logger.info(f"Successfully deleted {file_to_delete}")
            elif response.status_code == 404:
                logger.warning(f"File {file_to_delete} not found on the server")
            else:
                logger.error(
                    f"Failed to delete {file_to_delete}. Status code: {response.status_code}"
                )
        except Exception as e:
            logger.error(f"Error deleting {file_to_delete}: {str(e)}")


if __name__ == "__main__":
    fire.Fire(mdsync)
