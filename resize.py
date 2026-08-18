import os
import re
import threading
import warnings
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path
from typing import TYPE_CHECKING

import UnityPy

if TYPE_CHECKING:
    from UnityPy.classes import Texture2D

from PIL import Image

from src import ENV
from src.logging import logger
from src.options import CPU_THREADS, FORMAT, LOSSLESS, OPTIMIZE, UNITY_VERSION, Game

warnings.simplefilter("ignore", UnityPy.exceptions.UnityVersionFallbackWarning)
UnityPy.config.FALLBACK_UNITY_VERSION = UNITY_VERSION

lock = threading.Lock()


RESOLUTION: dict[re.Pattern, tuple[int, int, int | None] | None] = {
    re.compile(r"img_card_full_1"): (1920, 1080, None),
    re.compile(r"img_card_full_0"): (None, None, None),
    re.compile(r"music_jacket"): (None, None, None),
    re.compile(r"img_chr_full"): (None, None, None),
    re.compile(r"img_group_kv"): (None, None, None),
    re.compile(r"img_story_still_love"): (3840, 2160, None),
    re.compile(r"img_general_csprt.+full"): (1920, 1080, None),
    re.compile(r"img_general_comic_"): (1024, 760, 2),
    re.compile(r"img_general_comic4(?!.+thumb)"): (512, 1536, None),
    re.compile(r".*"): None,  # (None, None, None)
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
        with lock:
            countCurrent += 1
        return

    size = resolution[0:2]
    crop = resolution[2]

    asset = UnityPy.load(str(file))

    for obj in asset.objects:
        if obj.type.name in ("Texture2D", "Sprite"):
            data: "Texture2D" = obj.read()
            dest = folder.joinpath(f"{data.m_Name}.{FORMAT}")

            if dest.is_file():
                with lock:
                    countCurrent += 1
                logger.info(f'({countCurrent}/{countTotal}) "{data.m_Name}" skipped')
                continue

            img = data.image

            if size[0] and size[1]:
                img = img.resize(size, Image.Resampling.LANCZOS)
            if crop is not None:
                img = img.crop((crop, crop, size[0] - crop, size[1] - crop))

            img.save(dest, optimize=OPTIMIZE, quality=100, lossless=LOSSLESS)
            with lock:
                countCurrent += 1
            logger.info(f'$S({countCurrent}/{countTotal}) "{data.m_Name}" resized')


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
    game.add_argument("--gakumas", action="store_true", help="Gakuen Idolmaster")

    args = parser.parse_args()

    if args.gakumas:
        main(Game.gakumas)
    else:
        main(Game.ipr)
