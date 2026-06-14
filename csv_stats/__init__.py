"""
CSV Statistics CLI Tool

A simple Python CLI tool that reads a CSV file and outputs summary statistics
including row count, column means, and min/max values.
"""

__version__ = "1.0.0"
__author__ = "CSV Stats Team"

from csv_stats.stats import calculate_statistics, format_statistics

__all__ = ["calculate_statistics", "format_statistics"]
