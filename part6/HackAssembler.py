import sys

from hack_assembler import HackAssembler


def main():
    """
    Main flow - expect sys.argv[1] to be the path of the .asm file.
    """
    path = sys.argv[1]
    hack_assembler = HackAssembler.create(path)
    hack_assembler.first_pass()

    output = path.split(".")[0] + ".hack"

    with open(output, "w") as f:
        hack_assembler.second_pass(f)


if __name__ == "__main__":
    main()
