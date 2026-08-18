import os
import threading
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

from . import ENV
from .logging import logger
from .options import CPU_THREADS, Game

lock = threading.Lock()

UNITY_SIGNATURE = b"\x55\x6e\x69\x74\x79"

countCurrent = 0
countError = 0
countTotal = 0


def __unobfuscate(
    path: Path,
    outputPath: Path,
    dict_md5_name: dict,
    dict_md5_type: dict,
    jsonDB: dict,
    offset: int = 0,
    streamPos: int = 0,
    headerLength: int = 256,
):
    global countCurrent
    global countError

    buff = path.read_bytes()
    md5 = path.name
    name = dict_md5_name[md5]
    rev = str(jsonDB["revision"])

    if buff[0:5] == UNITY_SIGNATURE:
        contentType = dict_md5_type[md5]
        exportFolder = outputPath.joinpath(rev).joinpath(contentType)
        exportFolder.mkdir(parents=True, exist_ok=True)
        exportFolder.joinpath(f"{name}.unity3d").write_bytes(buff)

        with lock:
            countCurrent = countCurrent + 1
        ratio = f"({countCurrent}/{countTotal})"
        logger.info(f'{ratio} Assetbundle "{name}.unity3d" is not obfuscated')
        return

    unityFS = __cryptByString(
        buff,
        dict_md5_name[md5],
        offset,
        streamPos,
        headerLength,
    )

    if len(unityFS) > 0 and unityFS[0:5] == UNITY_SIGNATURE:
        contentType = dict_md5_type[md5]
        exportFolder = Path(outputPath).joinpath(rev).joinpath(contentType)
        exportFolder.mkdir(parents=True, exist_ok=True)
        flag = exportFolder.joinpath(name + ".unity3d").write_bytes(unityFS)

        if flag:
            with lock:
                countCurrent += 1
            ratio = f"({countCurrent}/{countTotal})"
            logger.info(f'$S{ratio} Assetbundle "{name}.unity3d" is unobfuscated')

        else:
            with lock:
                countError += 1
                countCurrent += 1
            ratio = f"({countCurrent}/{countTotal})"
            logger.error(f'$S{ratio} Failed to write "{name}.unity3d"')

    else:
        with lock:
            countError += 1
            countCurrent += 1
        ratio = f"({countCurrent}/{countTotal})"
        logger.error(f'$S{ratio} Failed to unobfuscate "{name}.unity3d"')


def Unobfuscate(jsonDB: dict, game: Game) -> bool:
    __inputDirectory = os.path.join(ENV, game.name, "Assets")
    __outputPath = os.path.join(ENV, game.name, "UnobfuscateAssets")

    if not os.path.isdir(__inputDirectory):
        logger.error(f'Folder "{__inputDirectory}" does not exist...')
        return False

    assetList: list = jsonDB["assetBundleList"]
    dict_md5_name = {item["md5"]: item["name"] for item in assetList}
    dict_md5_type = {item["md5"]: item["type"] for item in assetList}

    contents = Path(__inputDirectory).glob("**/*")
    filePaths = [path for path in contents if path.name in dict_md5_name]

    global countTotal
    countTotal = len(filePaths)

    executor = ThreadPoolExecutor(max_workers=CPU_THREADS)

    outputPath = Path(__outputPath)

    allTasks = [
        executor.submit(
            __unobfuscate,
            path,
            outputPath,
            dict_md5_name,
            dict_md5_type,
            jsonDB,
        )
        for path in filePaths
    ]

    wait(allTasks, return_when=ALL_COMPLETED)

    logger.info(f"Unobfuscation finished with {countError} error(s)")
    return True


def RenameAll(jsonDB: dict, game: Game) -> bool:
    __inputDirectory = os.path.join(ENV, game.name, "Assets")
    __outputPath = os.path.join(ENV, game.name, "UnobfuscateAssets")

    if not os.path.isdir(__inputDirectory):
        logger.error(f'Folder "{__inputDirectory}" does not exist...')
        return False

    resourceList: list = jsonDB["resourceList"]
    dict_md5_name = {item["md5"]: item["name"] for item in resourceList}
    dict_md5_type = {item["md5"]: item["type"] for item in resourceList}

    contents = Path(__inputDirectory).glob("**/*")
    filePaths = [path for path in contents if path.name in dict_md5_name]

    countTotal = len(filePaths)
    rev = str(jsonDB["revision"])

    for current, path in enumerate(filePaths):
        md5 = path.name
        name = dict_md5_name[md5]
        _type = dict_md5_type[md5]

        exportFolder = Path(__outputPath).joinpath(rev).joinpath(_type)
        exportFolder.mkdir(parents=True, exist_ok=True)
        exportFolder.joinpath(name).write_bytes(path.read_bytes())

        logger.info(f'$S({current + 1}/{countTotal}) Resource "{name}" renamed')

    logger.info("Rename finished")
    return True


def __stringToMaskBytes(maskStr: str, maskStrLen: int, bytesLen: int) -> bytes:
    maskBytes = bytearray(bytesLen)

    if maskStrLen >= 1:
        i = 0
        j = 0
        k = bytesLen - 1
        while maskStrLen != j:
            charJ = maskStr[j]
            charJ = int.from_bytes(
                charJ.encode("ascii"), byteorder="little", signed=False
            )
            j += 1
            maskBytes[i] = charJ
            i += 2
            charJ = ~charJ & 0xFF
            maskBytes[k] = charJ
            k -= 2

    if bytesLen >= 1:
        l = bytesLen
        v13 = 0x9B
        m = bytesLen
        pointer = 0
        while m:
            v16 = maskBytes[pointer]
            pointer += 1
            m -= 1
            v13 = (((v13 & 1) << 7) | (v13 >> 1)) ^ v16
        b = 0
        while l:
            l -= 1
            maskBytes[b] ^= v13
            b += 1

    return bytes(maskBytes)


def __cryptByString(
    input: bytes,
    maskString: str,
    offset: int,
    streamPos: int,
    headerLength: int,
) -> bytes:
    maskStringLength = len(maskString)
    bytesLength = maskStringLength << 1

    buffer = bytearray(input)
    maskBytes = __stringToMaskBytes(maskString, maskStringLength, bytesLength)

    i = 0
    while streamPos + i < headerLength:
        buffer[offset + i] ^= maskBytes[(streamPos + i) % bytesLength]
        i += 1

    return bytes(buffer)
