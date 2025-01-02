import argparse

from .options import WorkMode, DiffMode, Game

parser = argparse.ArgumentParser(description="🟉 🟊 ⚝ ⛦ Hoshimi Toolkit ⛦ ⚝ 🟊 🟉")

work_mode = parser.add_mutually_exclusive_group()
work_mode.add_argument("--remote", action="store_true", help="Download from server")
work_mode.add_argument("--local", action="store_true", help="Extract local assets")

diff_mode = parser.add_mutually_exclusive_group()
diff_mode.add_argument("--diff", action="store_true", help="Only download new assets")
diff_mode.add_argument("--all", action="store_true", help="Always download everything")

game = parser.add_mutually_exclusive_group()
game.add_argument("--ipr", action="store_true", help="Idoly Pride")
game.add_argument("--kr", action="store_true", help="Idoly Pride (KR Server)")
game.add_argument("--gakumas", action="store_true", help="Gakuen Idolmaster")


def parse() -> tuple[WorkMode, DiffMode, Game]:
    args = parser.parse_args()

    work = WorkMode.local if args.local else WorkMode.remote
    diff = DiffMode.all if args.all else DiffMode.diff

    if args.kr:
        game = Game.kr
    elif args.gakumas:
        game = Game.gakumas
    else:
        game = Game.ipr

    return (work, diff, game)
