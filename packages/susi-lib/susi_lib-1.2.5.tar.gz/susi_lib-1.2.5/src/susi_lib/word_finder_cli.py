import argparse
import sys
from inspect import get_annotations
from pathlib import Path
from typing import Literal, TypedDict, cast

from susi_lib.dictionary import Dictionary, _Mapping
from susi_lib.functions import unique_letters
from susi_lib.regex import Selection, create_regex


def _validate_input(wanted_letters: list[str], length: str | None, file: str | None):
    if len(wanted_letters) < 1:
        return False, "No wanted letters"
    keys = get_annotations(_Mapping)
    if file is not None and file not in keys and not Path(file).exists():
        return False, f"File '{file}' does not exist"
    if length is None:
        length = str(len(wanted_letters))
    match (length.split("-")):
        case [wl]:
            if not wl.isdigit():
                return False, "Length should be a number"
            if len(wanted_letters) not in (1, int(wl)):
                return False, "Wanted letters has wrong format"
        case [begin, end]:
            if not begin.isdigit() or not end.isdigit():
                return False, "Begin and end should be numbers"
            if len(wanted_letters) != 1:
                return False, "Wanted letters has wrong format"
        case _:
            return False, "Length has wrong format"
    return True, ""


class _TrDictReturn(TypedDict, total=False):
    data: list[str]
    length: int | tuple[int, int]
    letters: str
    invert: bool


def _translate(
    wanted_letters: list[str], length: int | tuple[int, int], file: str | None
) -> tuple[
    list[tuple[str, Selection]],
    _TrDictReturn,
]:
    if file is None:
        f = sys.stdin
    elif file in _Mapping(PM="", PM_a="", S="", S_a="", ZT="", ZT_a="").keys():
        f = open(
            Dictionary[cast(Literal["PM", "PM_a", "S", "S_a", "ZT", "ZT_a"], file)],
            "r",
            encoding="utf-8",
        )
    else:
        f = open(file, "r", encoding="utf-8")
    data = [l.strip() for l in f]
    f.close()

    match len(wanted_letters):
        case 1:
            wl = wanted_letters[0]
            return ([], {"data": data, "length": length, "letters": wl})
        case _:
            args: list[tuple[str, Selection]] = []
            for group in wanted_letters:
                if "." in group:
                    args.append((group, Selection.ANY))
                elif group[0] == "^":
                    args.append((group[1:], Selection.INVERT))
                else:
                    args.append((group, Selection.NONE))
            return (args, {"data": data})


parser = argparse.ArgumentParser(
    description="Program for finding words using regular expressions."
)
parser.add_argument(
    "-w", "--word-length", type=str, help="search for words of this length"
)
parser.add_argument(
    "-i",
    "--input-file",
    default=None,
    help="Path to a input file, each word should be on separate line. Or a dictionary short: \
        'PM', 'PM_a', 'S', 'S_a', 'ZT', 'ZT_a'. Default: stdin",
)
parser.add_argument(
    "-u",
    "--unique",
    action="store_true",
    help="If set, it finds only words with unique letters",
)
parser.add_argument(
    "wanted_letters",
    help="type wanted letters without spaces or space separated groups of wanted \
            letters for that position",
    nargs="*",
)


def main() -> Literal[0, 1]:
    args_parsed = parser.parse_args()

    valid, message = _validate_input(
        args_parsed.wanted_letters, args_parsed.word_length, args_parsed.input_file
    )
    if not valid:
        print(f"Error: {message}")
        return 1

    word_length = cast(
        int | tuple[int, int] | tuple[int],
        (
            tuple(map(int, args_parsed.word_length.split("-")))
            if args_parsed.word_length is not None
            else len(args_parsed.wanted_letters[0])
        ),
    )
    word_length = (
        word_length[0]
        if not isinstance(word_length, int) and len(word_length) == 1
        else word_length
    )

    args, kwargs = _translate(
        args_parsed.wanted_letters, word_length, args_parsed.input_file
    )
    regex = create_regex(*args, **kwargs)
    result = regex.execute()
    if args_parsed.unique:
        result = [w for w in result if unique_letters(w)]
    print("\n".join(result))
    return 0
