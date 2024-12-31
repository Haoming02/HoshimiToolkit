import os
import re
import threading
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

import UnityPy
from PIL import Image

from src import ENV
from src.logging import logger
from src.options import CPU_THREADS, OPTIMIZE, UNITY_VERSION, Game


UnityPy.config.FALLBACK_UNITY_VERSION = UNITY_VERSION
UnityPy.config.FALLBACK_VERSION_WARNED = True
lock = threading.Lock()


RESOLUTION: dict[re.Pattern, tuple[int, int, bool | int]] = {
    r"img_card_full_1": (1920, 1080, None),
    r"img_general_csprt.*full": (1920, 1080, None),
    r"img_general_comic": (1024, 760, 2),
    r".*": None,
}

countCurrent = 0
countTotal = 0


def __resize(file: Path, folder: Path):
    global countCurrent

    for key, vals in RESOLUTION.items():
        if re.search(key, file.name):
            resolution = vals
            break

    if resolution is None:
        lock.acquire()
        countCurrent += 1
        lock.release()
        return

    size = resolution[0:2]
    crop = resolution[2]

    asset = UnityPy.load(str(file))

    for obj in asset.objects:
        if obj.type.name in ("Texture2D", "Sprite"):
            data = obj.read()
            dest = folder.joinpath(f"{data.name}.png")

            if dest.is_file():
                lock.acquire()
                countCurrent += 1
                logger.info(f'({countCurrent}/{countTotal}) "{data.name}" skipped')
                lock.release()
                continue

            img = data.image.resize(size, Image.Resampling.LANCZOS)

            if crop is not None:
                img = img.crop((crop, crop, size[0] - crop, size[1] - crop))

            img.save(dest, optimize=OPTIMIZE)
            lock.acquire()
            countCurrent += 1
            logger.info(f'$S({countCurrent}/{countTotal}) "{data.name}" resized')
            lock.release()


def main(game: Game):
    assetPath = Path(os.path.join(ENV, game.name, "UnobfuscateAssets"))
    contents = list(assetPath.glob("**/img/*"))

    exportFolder = Path(os.path.join(ENV, "resized_images", game.name))
    exportFolder.mkdir(parents=True, exist_ok=True)

    global countTotal
    countTotal = len(contents)

    executor = ThreadPoolExecutor(max_workers=CPU_THREADS)
    allTasks = [executor.submit(__resize, file, exportFolder) for file in contents]
    wait(allTasks, return_when=ALL_COMPLETED)

    logger.info("Resizing finished")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="🟉 🟊 ⚝ ⛦ Resize Toolkit ⛦ ⚝ 🟊 🟉")

    game = parser.add_mutually_exclusive_group(required=True)
    game.add_argument("--ipr", action="store_true", help="Idoly Pride")
    game.add_argument("--kr", action="store_true", help="Idoly Pride (KR Server)")
    game.add_argument("--gakumas", action="store_true", help="Gakuen Idolmaster")

    args = parser.parse_args()

    if args.kr:
        main(Game.kr)
    elif args.gakumas:
        main(Game.gakumas)
    else:
        main(Game.ipr)
