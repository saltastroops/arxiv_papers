import pathlib
import tomllib


def main():
    config_file = pathlib.Path(__file__).parent.parent / "config.toml"
    with open(config_file, "rb") as f:
        config = tomllib.load(f)


if __name__ == "__main__":
    main()
