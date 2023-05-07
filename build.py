#!/usr/bin/env python
import os
import shutil
import subprocess as spc
from pathlib import Path

PWD = Path(".")
BUILD_DIR = Path("build")

IGNORE_DIRS = [
    ".idea",
    "build",
    "venv",
]

# If a file extension is here and the key value is True, it will get processed.
# If it is here and the key value is False, it will get copied.
TO_PROCESS = {
    "html": True,
    "css": False,
    "ico": False,
    "js": False,
    "png": False,
    "svg": False,
    "webmanifest": False,
    "xml": False,
}


def ext_of(file: Path) -> str:
    """Returns the extension of the given file."""
    return file.name.split(".")[-1]


def should_process(file: Path) -> bool:
    """Returns whether if the file should be processed."""
    return should_copy(file) and TO_PROCESS.get(ext_of(file), False)


def should_copy(file: Path, /) -> bool:
    """Returns whether if the file should be copied (i.e. included in the build/ dir)."""
    return ext_of(file) in TO_PROCESS and not file.name.startswith("_")


def process_file(in_: Path, out: Path, /) -> None:
    """
    Processes the give file with the C preprocessor.
    Writes the output to the given file.
    Filters lines that start with `#`.
    """
    process = spc.Popen(
        f"cc -E - < {in_}", stderr=spc.DEVNULL, stdout=spc.PIPE, shell=True
    )

    with out.open("wb") as out_file:
        for line in process.stdout:
            if line.startswith(b"#"):
                continue

            out_file.write(line)


def build(directory: Path, /) -> None:
    for path in directory.iterdir():
        if any(
            part in IGNORE_DIRS
            for part in (path.parts[:-1] if path.is_file() else path.parts)
        ):
            continue

        if path.is_dir():
            build(path)
            continue

        if not should_copy(path):
            continue

        path_build_path = BUILD_DIR / path.relative_to(PWD)
        path_build_path.parent.mkdir(parents=True, exist_ok=True)

        if should_process(path):
            print("Building", end="")
            process_file(path, path_build_path)
        else:
            print("Copying ", end="")
            shutil.copyfile(path, path_build_path)

        print(f" {path}...")


if __name__ == "__main__":
    shutil.rmtree("build", ignore_errors=True)
    os.makedirs("build")

    build(PWD)
    print()
    print("Building finished!")
