import os
import re
import threading
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import UnityPy

from src import ENV
from src.logging import logger
from src.options import CPU_THREADS, UNITY_VERSION, Game


UnityPy.config.FALLBACK_UNITY_VERSION = UNITY_VERSION
UnityPy.config.FALLBACK_VERSION_WARNED = True
lock = threading.Lock()


PATTERN: dict[re.Pattern, bool] = {
    re.compile(r"music_short"): True,
    re.compile(r".*"): False,
}

countCurrent = 0
countTotal = 0


def __extract(file: Path, folder: Path):
    global countCurrent

    for key, val in PATTERN.items():
        if re.search(key, file.name):
            resolution = val
            break

    if not resolution:
        lock.acquire()
        countCurrent += 1
        lock.release()
        return

    asset = UnityPy.load(str(file))

    for obj in asset.objects:
        if obj.type.name == "AudioClip":
            clip = obj.read()

            for name, data in getattr(clip, "samples", {}).items():
                dest = folder.joinpath(name)

                if dest.is_file():
                    logger.info(f'"{name}" skipped')
                else:
                    with open(str(dest), "wb") as f:
                        f.write(data)

                    lock.acquire()
                    countCurrent += 1
                    logger.info(f'$S({countCurrent}/{countTotal}) "{name}" extracted')
                    lock.release()


def main(game: Game):
    assetPath = Path(os.path.join(ENV, game.name, "UnobfuscateAssets"))
    contents = list(assetPath.glob("**/sud/*"))

    exportFolder = Path(os.path.join(ENV, "extracted_audio", game.name))
    exportFolder.mkdir(parents=True, exist_ok=True)

    global countTotal
    countTotal = len(contents)

    executor = ThreadPoolExecutor(max_workers=CPU_THREADS)
    allTasks = [executor.submit(__extract, file, exportFolder) for file in contents]
    wait(allTasks, return_when=ALL_COMPLETED)

    logger.info("Extraction finished")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="🟉 🟊 ⚝ ⛦ Audio Toolkit ⛦ ⚝ 🟊 🟉")

    game = parser.add_mutually_exclusive_group(required=True)
    game.add_argument("--ipr", action="store_true", help="Idoly Pride")
    game.add_argument("--kr", action="store_true", help="Idoly Pride (KR Server)")
    game.add_argument("--gakumas", action="store_true", help="Gakuen Idolmaster")

    args = parser.parse_args()

    if args.kr:
        main(Game.kr)
    elif args.gakumas:
        logger.error("Gakumas songs are already .mp3 files~")
    else:
        main(Game.ipr)
