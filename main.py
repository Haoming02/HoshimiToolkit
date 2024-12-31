from src.options import DiffMode, Game, WorkMode
from src.parser import parse


def main(work: WorkMode, diff: DiffMode, game: Game):
    from src.ManifestDecryptor import Decrypt

    jsonDB, status = Decrypt(diff, game)
    if status is False:
        return

    if work == WorkMode.remote:
        from src.AssetsDownloader import DownloadAll

        DownloadAll(jsonDB, game)

    from src.MaskedHeaderStream import RenameAll, Unobfuscate

    if not Unobfuscate(jsonDB, game):
        return

    if not RenameAll(jsonDB, game):
        return

    from src.logging import logger

    logger.info("$SAll operations are done!")


if __name__ == "__main__":
    work, diff, game = parse()
    main(work, diff, game)
