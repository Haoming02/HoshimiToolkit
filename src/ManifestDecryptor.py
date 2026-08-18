import json
import os
import re
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from diskcache import Cache
from google.protobuf.json_format import MessageToJson

from . import ENV, octodb_pb2
from .logging import logger
from .options import DiffMode, Game, MagicStrings


def __decryptCache(key: bytes, iv: bytes, cache: str) -> octodb_pb2.ProtobufDB:
    """
    Decrypts a cache file (usually named 'octocacheevai') and deserializes it to a protobuf object
    """

    cipher = AES.new(key, AES.MODE_CBC, iv)
    encryptCachePath = Path(cache)

    try:
        encryptedBytes = encryptCachePath.read_bytes()
    except Exception:
        logger.error("Failed to read the encrypted cache...")
        return None

    try:
        # There is an extra 0x01 byte at the start of the encrypted file
        decryptedBytes = unpad(
            cipher.decrypt(encryptedBytes[1:]),
            block_size=16,
            style="pkcs7",
        )
    except Exception:
        logger.error("Failed to decrypt the encrypted cache...")
        return None

    # The first 16 bytes are an md5 hash of the database
    decryptedBytes = decryptedBytes[16:]

    # Read the decrypted bytes to a protobuf object
    protoDatabase = octodb_pb2.Database()
    protoDatabase.ParseFromString(decryptedBytes)

    logger.info(f"Current Revision: {protoDatabase.revision}")
    return protoDatabase


def __proto2json(protoDb: octodb_pb2.ProtobufDB) -> str:
    """Converts a protobuf serialized object to JSON string"""
    jsonDb = MessageToJson(protoDb)
    return jsonDb


def __loadJson(jsonString: str) -> dict:
    """Deserialize json string to a dict"""

    def _appendType(item: dict):
        m = re.match(r"(.+?)_.*$", item["name"])  # Matches the first _ in name
        typeName = m.group(1) if m else "others"
        item["type"] = typeName

    jsonDB = json.loads(jsonString)
    for it in jsonDB["assetBundleList"]:
        _appendType(it)
    for it in jsonDB["resourceList"]:
        _appendType(it)

    return jsonDB


def __diffRevision(jsonDB: dict, cache: Cache) -> dict:
    latest: int = next(cache.iterkeys(reverse=True), None)
    rev = int(jsonDB["revision"])

    if latest is None:
        cache[rev] = jsonDB
        return jsonDB

    if latest >= rev:
        logger.warning("The given Cache is duplicated / outdated...")
        status = input("Continue? [Y/n]: ")
        if status.strip() == "Y":
            return jsonDB
        else:
            logger.info("Process Terminated")
            return None

    prevDB: dict = cache[latest]
    cache[rev] = jsonDB

    prevAssetBundle: set[int] = {it["id"] for it in prevDB["assetBundleList"]}
    prevResource: set[int] = {it["id"] for it in prevDB["resourceList"]}

    addedDB = {
        "assetBundleList": [
            it1 for it1 in jsonDB["assetBundleList"] if it1["id"] not in prevAssetBundle
        ],
        "resourceList": [
            it2 for it2 in jsonDB["resourceList"] if it2["id"] not in prevResource
        ],
    }

    changedDB = {
        "assetBundleList": [
            it1
            for it1 in jsonDB["assetBundleList"]
            if it1["id"] in prevAssetBundle and it1["state"] == "UPDATE"
        ],
        "resourceList": [
            it2
            for it2 in jsonDB["resourceList"]
            if it2["id"] in prevResource and it2["state"] == "UPDATE"
        ],
    }

    diffDB = {
        "revision": jsonDB["revision"],
        "urlFormat": jsonDB["urlFormat"],
        "assetBundleList": addedDB["assetBundleList"] + changedDB["assetBundleList"],
        "resourceList": addedDB["resourceList"] + changedDB["resourceList"],
    }

    return diffDB


def Decrypt(diffMode: DiffMode, game: Game) -> tuple[dict, bool]:
    cache = os.path.join(ENV, game.name, "EncryptedCache", "octocacheevai")
    if not os.path.isfile(cache):
        logger.error(f'Cache "{cache}" does not exist...')
        return None, False

    # Decrypt cache file
    KEY, IV = MagicStrings.get(game)
    protoDB: octodb_pb2.ProtobufDB = __decryptCache(KEY, IV, cache)
    if protoDB is None:
        return None, False

    # Convert protobuf to json
    jsonString = __proto2json(protoDB)
    jsonDB = __loadJson(jsonString)

    outputPath = os.path.join(ENV, game.name, "DecryptedCaches")
    cache = Cache(
        directory=outputPath,
        eviction_policy="least-recently-stored",
        size_limit=32 * 1024 * 1024,  # 32 MB; each rev is ~5 MB
        cull_limit=2,
    )

    # Process differences
    diffDB = __diffRevision(jsonDB, cache)
    if diffDB is None:
        return None, False

    cache.close()
    return (jsonDB if diffMode == DiffMode.all else diffDB), True
