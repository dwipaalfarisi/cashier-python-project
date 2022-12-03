# to create staging file
from database import ReadAndWrite


def main():
    stage = ReadAndWrite()
    # create staging file
    stage.write_header()


if __name__ == "__main__":
    main()
