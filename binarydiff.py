"""
Diffs the sections and relocations (where possible) of a dol/rel file
"""

from argparse import ArgumentParser
import colorama as col

from ppcdis import diff_secs, diff_relocs, load_binary_yml, load_from_yaml, RelReader

if __name__ == "__main__":
    hex_int = lambda s: int(s, 16)
    parser = ArgumentParser(
        description="Diff the sections and relocations of dol/rel files"
    )
    parser.add_argument("good", type=str, help="Path to good binary yml")
    parser.add_argument("test", type=str, help="Path to test binary")
    parser.add_argument(
        "-n",
        "--max-reloc-diffs",
        type=int,
        default=-1,
        help="Maximum number of rel relocation diffs to print",
    )
    parser.add_argument("-m", "--map", type=str, help="Optional symbols YAML file")
    args = parser.parse_args()

    # Init colorama
    col.init()

    # Load binaries
    good = load_binary_yml(args.good)
    test = good.load_other(args.test)
    symbols = None
    if args.map:
        symbols = load_from_yaml(args.map)

    # Do diff
    ret = diff_secs(good, test)
    if not ret and isinstance(good, RelReader):
        diff_relocs(good, test, args.max_reloc_diffs, symbols)
