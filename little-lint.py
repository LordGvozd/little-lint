import sys
import os
from pathlib import Path


from colorama import Fore, init

from src.models import ViolationType
from src.rules import scanner

colors = {
    ViolationType.WARNING: Fore.YELLOW,
    ViolationType.NOT_RECOMMENDER: Fore.CYAN,
    ViolationType.ERROR: Fore.RED,
}

excluded_folders = (".idea", ".venv", "venv", "__pycache__")


def _check_file(file_path: Path) -> tuple[list[str], int]:
    file_count = 0
    if file_path.name in excluded_folders:
        return [], 0
    file_violations = []

    if os.path.isdir(file_path):

        for child_file_name in os.listdir(file_path):

            child_file_path = Path(
                str(file_path) + "/" + child_file_name
            ).resolve()
            child_violations, child_files_count = _check_file(child_file_path)

            if child_violations:
                file_violations.extend(child_violations)

                file_count += child_files_count
    else:
        if file_path.suffix == ".py":
            with open(file_path, "r") as f:
                violations = scanner.scan(f.read())

            for v in violations:
                color = colors[v.type]
                file_violations.append(
                    f"{color}File '{Fore.MAGENTA + str(file_path) + color}',"
                    f" line {Fore.MAGENTA + str(v.line) + color}\n"
                    f"{v.__class__.__name__}: {v.text}{Fore.RESET}"
                )
                file_count += 1
    return file_violations, file_count


def main() -> None:
    init()  # Init colorama
    args = sys.argv

    if len(args) == 1:
        print(Fore.RED + "Please, specify files to be checked!")
        exit(1)

    violations = []
    file_count = 0
    for file_name in sys.argv[1:]:
        file_path = Path(file_name).resolve()

        if not os.path.exists(file_path):
            print(Fore.RED + f"File '{file_name}' not exist!")
            exit(1)

        fv, file_count = _check_file(file_path)
        if fv:
            file_count += 1
            violations.extend(fv)
    for v in violations:
        print(v)

    print(
        f"\n{Fore.LIGHTRED_EX}Total {len(violations)}"
        f" violations in {file_count - 1} files"
    )


if __name__ == "__main__":
    main()
