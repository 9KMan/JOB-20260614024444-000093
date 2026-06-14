#!/usr/bin/env python3
"""
CSV Statistics CLI Tool

A command-line tool that reads a CSV file and outputs summary statistics
including row count, column means, and min/max values.
"""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from csv_stats.analyzer import CSVAnalyzer
from csv_stats.formatters import format_summary, format_error


console = Console()


@click.command()
@click.argument(
    "file_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="CSV delimiter character (default: comma)",
)
@click.option(
    "--quotechar",
    "-q",
    default='"',
    help="CSV quote character (default: double quote)",
)
@click.option(
    "--encoding",
    "-e",
    default="utf-8",
    help="File encoding (default: utf-8)",
)
@click.option(
    "--no-header",
    is_flag=True,
    help="Treat first row as data, not header",
)
@click.option(
    "--decimal-places",
    "-p",
    default=2,
    type=int,
    help="Number of decimal places for numeric values (default: 2)",
)
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json", "text"]),
    default="table",
    help="Output format (default: table)",
)
@click.version_option(version="1.0.0", prog_name="csv-stats")
def main(
    file_path: Path,
    delimiter: str,
    quotechar: str,
    encoding: str,
    no_header: bool,
    decimal_places: int,
    output: str,
) -> None:
    """
    Read a CSV file and display summary statistics.

    Shows row count, column means, and min/max values for each numeric column.

    Example:\n
        csv-stats data.csv\n
        csv-stats sales.csv --delimiter ";" --decimal-places 4
    """
    try:
        analyzer = CSVAnalyzer(
            delimiter=delimiter,
            quotechar=quotechar,
            encoding=encoding,
            has_header=not no_header,
            decimal_places=decimal_places,
        )

        summary = analyzer.analyze(file_path)

        if output == "json":
            from csv_stats.formatters import format_json
            console.print(format_json(summary))
        elif output == "text":
            console.print(format_summary(summary))
        else:
            table = Table(title=f"CSV Statistics: {file_path.name}", show_header=True)
            table.add_column("Statistic", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")

            # Row count
            table.add_row("Total Rows", str(summary["row_count"]))
            table.add_row("Total Columns", str(summary["column_count"]))
            table.add_row("File Path", str(summary["file_path"]))

            console.print(table)
            console.print()

            if summary["statistics"]:
                stats_table = Table(
                    title="Column Statistics",
                    show_header=True,
                    header_style="bold green",
                )
                stats_table.add_column("Column", style="cyan")
                stats_table.add_column("Mean", style="yellow", justify="right")
                stats_table.add_column("Min", style="red", justify="right")
                stats_table.add_column("Max", style="green", justify="right")
                stats_table.add_column("Non-Null", style="blue", justify="right")

                for col_name, stats in summary["statistics"].items():
                    stats_table.add_row(
                        col_name,
                        str(stats.get("mean", "N/A")),
                        str(stats.get("min", "N/A")),
                        str(stats.get("max", "N/A")),
                        str(stats.get("non_null_count", "N/A")),
                    )

                console.print(stats_table)

    except Exception as e:
        console.print(format_error(str(e)), style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    main()
