import json
from eDiffMode import DiffMode
import octodb_pb2
import sys
import re
from rich.console import Console
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pathlib import Path
from google.protobuf.json_format import MessageToJson

# Currently known magic strings
__KEY = bytes.fromhex("9d8dfd7b1371612846f7ba44e01af160")
__IV = bytes.fromhex("1c6e6f9255c0e5412712f4010225e378")

# Input cache file and output directory strings
__inputPathString = "EncryptedCache/octocacheevai"
__outputPathString = "DecryptedCaches"

# Initialization
console = Console()


def __decryptCache(key=__KEY, iv=__IV) -> octodb_pb2.Database:
    """Decrypts a cache file (usually named 'octocacheevai') and deserializes it to a protobuf object

    Args:
        key (string): A byte-string. Currently 16 characters long and appears to be alpha-numeric.
        iv (string): A byte-string. Currently 10 characters long and appears to be base64-ish.

    Returns:
        octodb_pb2.Database: A protobuf object representing the deserialized cache.
    """

    cipher = AES.new(key, AES.MODE_CBC, iv)
    encryptCachePath = Path(__inputPathString)

    try:
        encryptedBytes = encryptCachePath.read_bytes()
    except:
        console.print(
            f"[bold red]>>> [Error][/bold red] Failed to load encrypted cache file at '{encryptCachePath}'.\n{sys.exc_info()}\n"
        )
        raise

    try:
        # For some reason there's a single extra 0x01 byte at the start of the encrypted file
        decryptedBytes = unpad(
            cipher.decrypt(encryptedBytes[1:]), block_size=16, style="pkcs7"
        )
    except:
        console.print(
            f"[bold red]>>> [Error][/bold red] Failed to decrypt cache file.\n{sys.exc_info()}\n"
        )
        raise

    # The first 16 bytes are an md5 hash of the database that follows it, which is skipped because it's useless for this purpose
    decryptedBytes = decryptedBytes[16:]
    # Read the decrypted bytes to a protobuf object
    protoDatabase = octodb_pb2.Database()
    protoDatabase.ParseFromString(decryptedBytes)
    # Revision number should probably change with every update..?
    console.print(
        f"[bold]>>> [Info][/bold] Current revision : {protoDatabase.revision}\n"
    )

    return protoDatabase


def __protoDb2Json(protoDb: octodb_pb2.Database) -> str:
    """Converts a protobuf serialized object to JSON string then return the string."""
    jsonDb = MessageToJson(protoDb)
    return jsonDb


def __diffRevision(jDict: dict) -> dict:
    p = Path(__outputPathString)
    manifestList = [
        it for it in p.iterdir() if re.match(r"^manifest_v\d+.json$", it.name)
    ]
    if manifestList.__len__() == 0:
        console.print(f"[bold]>>> [Info][/bold] No previous revision json found.\n")
        return jDict
    manifestList.sort(key=lambda it: int(it.name.split("_v")[1].split(".")[0]), reverse=True)
    previousOne = manifestList[0]
    jDictPrev = json.loads(previousOne.read_bytes())

    if jDictPrev["revision"] > jDict["revision"]:
        console.print(
            f"[bold yellow]>>> [Warning][/bold yellow] Old revision, diff operation has been stopped.\n"
        )
        return jDict

    if jDictPrev["revision"] == jDict["revision"]:
        if manifestList.__len__() == 1:
            console.print(
                f"[bold yellow]>>> [Warning][/bold yellow] Duplicate revision, diff operation has been stopped.\n"
            )
            return jDict
        console.print(f"[bold yellow]>>> [Warning][/bold yellow] Duplicate revision.\n")
        jDictPrev = json.loads(manifestList[1].read_bytes())

    if jDictPrev["revision"] >= jDict["revision"]:
        jDictPrev = json.loads(manifestList[1].read_bytes())
        console.print(
            f"[bold yellow]>>> [Warning][/bold yellow] Duplicate or old revision, diff operation has been stopped.\n"
        )
        return jDict

    assetBundlePrevDict = [it["id"] for it in jDictPrev["assetBundleList"]]
    resourcePrevDict = [it["id"] for it in jDictPrev["resourceList"]]

    diffNewDict = {
        "revision": jDict["revision"],
        "assetBundleList": [
            it1
            for it1 in jDict["assetBundleList"]
            if it1["id"] not in assetBundlePrevDict
        ],
        "resourceList": [
            it2
            for it2 in jDict["resourceList"]
            if it2["id"] not in resourcePrevDict
        ],
    }
    diffChangedDict = {
        "revision": jDict["revision"],
        "assetBundleList": [
            it1
            for it1 in jDict["assetBundleList"]
            if it1["id"] in assetBundlePrevDict
            and it1["state"] == "UPDATE"
        ],
        "resourceList": [
            it2
            for it2 in jDict["resourceList"]
            if it2["id"] in resourcePrevDict
            and it2["state"] == "UPDATE"
        ],
    }

    # diffChangeDict = {
    #     "revision": jDict["revision"],
    #     "assetBundleList": [ it1 for it1 in jDict["assetBundleList"] if it1 not in jDictPrev["assetBundleList"] ],
    #     "resourceList": [ it2 for it2 in jDict["resourceList"] if it2 not in jDictPrev["resourceList"] ]
    # }

    diffOutputString = f"{__outputPathString}/manifest_diff_new_v{jDictPrev['revision']}_{jDict['revision']}.json"
    diffOutputPath = Path(diffOutputString)
    __writeJsonFile(diffNewDict, diffOutputPath)

    diffOutputString = f"{__outputPathString}/manifest_diff_changed_v{jDictPrev['revision']}_{jDict['revision']}.json"
    diffOutputPath = Path(diffOutputString)
    __writeJsonFile(diffChangedDict, diffOutputPath)
    diffDict = {
        "revision": jDict["revision"],
        "urlFormat": jDict["urlFormat"],
        "assetBundleList": [],
        "resourceList": [],
    }
    
    diffDict["assetBundleList"] = diffNewDict["assetBundleList"] + diffChangedDict["assetBundleList"]
    diffDict["resourceList"] = diffNewDict["resourceList"] + diffChangedDict["resourceList"]

    return diffDict


def __writeJsonFile(d: dict, path: Path):
    # Write the string to a json file
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(d, sort_keys=True, indent=4))
        console.print(
            f"[bold green]>>> [Succeed][/bold green] JSON has been written into {path}.\n"
        )
    except:
        console.print(
            f"[bold red]>>> [Error][/bold red] Failed to write JSON into {path}.\n{sys.exc_info()}\n"
        )
        raise


def __appendType(d: dict) -> dict:
    for it in d["assetBundleList"]:
        m = re.match(r"(.+?)_.*$", it["name"])  # Matches first _ in name
        if m:
            typeStr = m.group(1)
        else:
            typeStr = "others"
        it["type"] = typeStr
    for it in d["resourceList"]:
        m = re.match(r"(.+?)_.*$", it["name"])  # Matches first _ in name
        if m:
            typeStr = m.group(1)
        else:
            typeStr = "others"
        it["type"] = typeStr
    return d


def doDecrypt(diffMode: DiffMode) -> dict:
    # Decrypt cache file
    protoDb = __decryptCache()
    # Convert protobuf to json string
    jsonString = __protoDb2Json(protoDb)
    # Deserialize json string to a dict
    jDict = json.loads(jsonString)
    jDict = __appendType(jDict)
    # Diff
    diffDict = __diffRevision(jDict)
    # Define the output path of json file
    outputPath = Path(f"{__outputPathString}/manifest_v{protoDb.revision}.json")
    # Write the json string into a file
    __writeJsonFile(jDict, outputPath)
    if diffMode == DiffMode.Diff:
        return diffDict
    else:
        return jDict
