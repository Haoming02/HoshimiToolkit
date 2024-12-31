import os
import re
import threading
import time
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import requests

from . import ENV
from .logging import logger
from .options import CPU_THREADS, FILTER, MAX_RETRY, Game

lock = threading.Lock()

countCurrent = 0
countError = 0
countTotal = 0

existingFilenames = []


def __download(url: str, filePath: Path):
    for i in range(MAX_RETRY):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                filePath.write_bytes(r.content)
                return
            else:
                raise ConnectionError(f"Status: {r.status_code}")
        except Exception as e:
            logger.debug(f'Failed to download "{url}" - {e}')
            time.sleep(5 * i)

    raise TimeoutError


def __downloadSingle(path: Path, item: dict, _type: str, url_format: str):
    global countCurrent
    global countError

    md5 = item["md5"]
    if md5 in existingFilenames:
        lock.acquire()
        countCurrent = countCurrent + 1
        logger.warning(f'({countCurrent}/{countTotal}) File "{md5}" already exists')
        lock.release()
        return

    if not re.search(FILTER, item["name"]):
        lock.acquire()
        countCurrent = countCurrent + 1
        logger.info(f'$S({countCurrent}/{countTotal}) File "{md5}" skipped')
        lock.release()
        return

    url = url_format.format(
        v=str(item["uploadVersionId"]),
        o=str(item["objectName"]),
        g=str(item["generation"]),
        type=str(_type),
    )

    try:
        __download(url, path.joinpath(md5))
        lock.acquire()
        countCurrent += 1
        logger.info(f'$S({countCurrent}/{countTotal}) File "{md5}" downloaded')
        lock.release()
    except Exception:
        lock.acquire()
        countCurrent += 1
        countError += 1
        logger.error(f'({countCurrent}/{countTotal}) File "{md5}" failed to download')
        lock.release()


def DownloadAll(jsonDB: dict, game: Game):
    downloadPath = os.path.join(ENV, game.name, "Assets")
    path = Path(downloadPath)
    path.mkdir(parents=True, exist_ok=True)
    contents = path.glob("**/*")

    global existingFilenames
    existingFilenames = [file.name for file in contents]

    assetBundleList: list = jsonDB["assetBundleList"]
    resourceList: list = jsonDB["resourceList"]

    global countTotal
    countTotal = len(assetBundleList) + len(resourceList)
    logger.info("Started downloading assets...")

    executor = ThreadPoolExecutor(max_workers=CPU_THREADS)
    urlFormat: str = jsonDB["urlFormat"]

    allTasks = [
        executor.submit(__downloadSingle, path, item, "assetbundle", urlFormat)
        for item in assetBundleList
    ]

    allTasks.extend(
        [
            executor.submit(__downloadSingle, path, item, "resources", urlFormat)
            for item in resourceList
        ]
    )

    wait(allTasks, return_when=ALL_COMPLETED)

    logger.info(f"Download finished with {countError} error(s)")
