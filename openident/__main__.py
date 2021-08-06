"""Entrypoint for OpenIdent"""
import argparse

from openident.core import run


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenIdent")
    return parser.parse_args()


def main() -> None:
    run()


if __name__ == "__main__":
    main()
