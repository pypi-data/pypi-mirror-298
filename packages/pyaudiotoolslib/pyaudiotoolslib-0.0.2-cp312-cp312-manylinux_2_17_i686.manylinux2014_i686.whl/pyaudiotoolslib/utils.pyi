from os import PathLike
from pathlib import Path
from typing import TypeAlias

PathType: TypeAlias = str | bytes | PathLike | Path

def normalize_from_file(
    input_file: PathType,
    output_file: PathType,
    peak_level: float = -1.0,
    remove_dc: bool = True,
) -> None: ...
def remove_clicks_from_file(
    input_file: PathType,
    output_file: PathType,
    threshold_level: int = 200,
    click_width: int = 20,
) -> None: ...
def measure_rms_linear_from_file(input_file: PathType) -> float: ...
def measure_rms_db_from_file(input_file: PathType) -> float: ...
# def omp_get_max_threads() -> int: ...
# def omp_set_num_threads(threads: int) -> None: ...
