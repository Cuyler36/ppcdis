"""
Batch rips assets from a binary using a supplied YAML file
"""

from argparse import ArgumentParser
import yaml

from ppcdis import load_binary_yml, rip_asset

if __name__ == "__main__":
    hex_int = lambda s: int(s, 16)
    parser = ArgumentParser(description="Rip assets from a binary")
    parser.add_argument("binary_path", type=str, help="Binary input yml path")
    parser.add_argument("asset_yml_path", type=str, help="Asset input yml path")
    args = parser.parse_args()

    # Load binary
    binary = load_binary_yml(args.binary_path)
    data = None

    # Read asset YAML file
    with open(args.asset_yml_path, "r") as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.CSafeLoader)

    # Process each asset
    for file_path, addresses in data.items():
        start_address, end_address = addresses
        dat = rip_asset(binary, start_address, end_address)

        # Output
        with open(file_path, "wb") as f:
            f.write(dat)
