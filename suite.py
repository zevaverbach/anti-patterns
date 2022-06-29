"""
A benchmark suite for Performance Anti-Patterns
"""
import timeit
import pathlib
import sys
from statistics import fmean
from rich.console import Console
from rich.table import Table
from rich.text import Text

REPEAT = 5
TIMES = 5


def format_delta(result: float, comparator: float, delta: float) -> Text:
    """
    Color the column a shade of green if the result was faster than the comparator,
    red if it was slower, and format the string appropriately with %, minus symbol, etc.
    """
    minus = ""
    if abs(delta) > 100:
        formatter = "{0:.5f} ({1}{2:.1f}%)"
    else:
        formatter = "{0:.7f} ({1}{2:.1f}%)"
    if result < comparator:
        if delta < 10:
            col = "medium_spring_green"
        elif 10 <= delta < 20:
            col = "spring_green1"
        elif 20 <= delta < 40:
            col = "spring_green2"
        else:
            col = "green1"
        return Text(formatter.format(result, minus, delta), style=col)
    else:
        minus = "-"
        return Text(formatter.format(result, minus, delta), style="red")


if __name__ == "__main__":
    table = Table(
        title=f"Anti-Pattern Benchmark Suite, repeat={REPEAT}, number={TIMES}"
    )

    table.add_column("Benchmark", justify="right", style="cyan", no_wrap=True)
    table.add_column("Min", width=10)
    table.add_column("Max", width=10)
    table.add_column("Mean", width=10)
    table.add_column("Min (+)", style="blue", width=21)
    table.add_column("Max (+)", style="blue", width=21)
    table.add_column("Mean (+)", style="blue", width=21)

    profiles_out = pathlib.Path(__file__).parent / "profiles"
    if not profiles_out.exists():
        profiles_out.mkdir()
    n = 0

    for f in pathlib.Path(__file__).parent.glob("bench_*.py"):
        if len(sys.argv) > 1 and f.stem != f"bench_{sys.argv[1]}":
            continue
        i = __import__(
            f.stem,
            globals(),
            locals(),
        )
        if hasattr(i, "__benchmarks__"):
            for benchmark in i.__benchmarks__:
                n += 1
                func1, func2, desc = benchmark
                comparator_result = timeit.repeat(func1, repeat=REPEAT, number=TIMES)
                result = timeit.repeat(func2, repeat=REPEAT, number=TIMES)

                delta_mean = (
                    abs(fmean(result) - fmean(comparator_result))
                    / fmean(comparator_result)
                ) * 100.0
                delta_min = (
                    abs(min(result) - min(comparator_result)) / min(comparator_result)
                ) * 100.0
                delta_max = (
                    abs(max(result) - max(comparator_result)) / max(comparator_result)
                ) * 100.0

                fdelta_min = format_delta(
                    min(result), min(comparator_result), delta_min
                )
                fdelta_max = format_delta(
                    max(result), max(comparator_result), delta_max
                )
                fdelta_mean = format_delta(
                    fmean(result), fmean(comparator_result), delta_mean
                )

                table.add_row(
                    desc,
                    "{:.7f}".format(min(comparator_result)),
                    "{:.7f}".format(max(comparator_result)),
                    "{:.7f}".format(fmean(comparator_result)),
                    fdelta_min,
                    fdelta_max,
                    fdelta_mean,
                )

    console = Console(width=150)
    console.print(table)
