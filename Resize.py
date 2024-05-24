from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

from rich.console import Console
from PIL import Image
from enum import Enum
import threading
import UnityPy
import os
import re

# Configurations
maxResizeThread = 20


class MODE(Enum):
    ipr = 1
    gakumas = 2


VERSION = {"ipr": "2020.3.18f1", "gakumas": "2022.3.21f1"}
FILTER: dict[MODE, dict[str, str]] = {
    MODE.ipr: (),
    MODE.gakumas: {
        "card": r"img_general_csprt-\d-\d{4}_full",
        "comic": r"img_general_comic_\d{4}",
    },
}

RESOLUTION: dict[MODE, dict[str, tuple[int, int]]] = {
    MODE.ipr: (),
    MODE.gakumas: {"card": (1920, 1080, 0), "comic": (1024, 760, 2)},
}

lock = threading.Lock()
console = Console()
countAll = 0
count = 0


def __validate_folder(folder: str) -> MODE:
    assert os.path.isdir(folder)

    if "ipr" in folder:
        UnityPy.config.FALLBACK_UNITY_VERSION = VERSION["ipr"]
        return MODE.ipr
    elif "gakumas" in folder:
        UnityPy.config.FALLBACK_UNITY_VERSION = VERSION["gakumas"]
        return MODE.gakumas
    else:
        print("\nUsage:\n(venv) > python Resize.py <path to img folder>")
        raise SystemExit


def resize(file_path: str, folder: str, resolution: tuple[int, int, int]):
    global count

    size = resolution[0:2]
    crop = resolution[2]

    asset = UnityPy.load(file_path)
    for obj in asset.objects:

        if obj.type.name in ("Texture2D", "Sprite"):
            data = obj.read()
            dest = f"{os.path.join(folder, data.name)}.png"

            if os.path.isfile(dest):
                lock.acquire()
                count += 1
                console.print(
                    f"\n[bold yellow]>>> ({count}/{countAll}) [Warning][/bold yellow] '{dest}' already exists."
                )
                lock.release()

            else:
                img = data.image.resize(size, Image.Resampling.LANCZOS)

                if crop > 0:
                    img = img.crop((crop, crop, size[0] - crop, size[1] - crop))

                img.save(dest)
                lock.acquire()
                count += 1
                console.print(
                    f"\n[bold green]>>> ({count}/{countAll}) [Succeed][/bold green] '{dest}' has been successfully resized."
                )
                lock.release()


def main(folder: str):
    mode = __validate_folder(folder)

    os.makedirs("resized_images", exist_ok=True)

    # === ToDo ===
    if mode == MODE.ipr:
        raise NotImplementedError
    # === ToDo ===

    files = os.listdir(folder)
    filters = FILTER[mode]

    targets = {}
    for image_type in filters.keys():
        targets[image_type] = []

    global count
    count = 0
    global countAll
    countAll = 0

    for file in files:
        filename = os.path.splitext(file)[0]

        for image_type, pattern in filters.items():
            if re.match(pattern, filename):
                targets[image_type].append(os.path.join(folder, file))
                countAll += 1

    console.print(
        f"[bold green]>>> [Succeed][/bold green] Start resizing images, this may take some time...\n"
    )

    executor = ThreadPoolExecutor(max_workers=maxResizeThread)

    allTasks = []

    for image_type in filters.keys():
        if len(targets[image_type]) == 0:
            continue

        save_folder = os.path.join("resized_images", image_type)
        os.makedirs(save_folder, exist_ok=True)

        allTasks.extend(
            [
                executor.submit(resize, file, save_folder, RESOLUTION[mode][image_type])
                for file in targets[image_type]
            ]
        )

    wait(allTasks, return_when=ALL_COMPLETED)
    console.print(
        f"\n[bold white]>>> [Info][/bold white] Resize operation has been done."
    )


if __name__ == "__main__":
    import sys

    path = sys.argv[1].strip()
    main(os.path.abspath(path))
