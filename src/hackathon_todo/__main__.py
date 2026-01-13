"""
Entry point for the Hackathon Todo application.

This module serves as the main entry point for the CLI application
when executed as a module.
"""

from __future__ import annotations

from .cli.app import main


def run() -> None:
    """
    Run the main application.

    This function serves as the entry point for the application.
    It handles any top-level exceptions and ensures proper exit codes.
    """
    try:
        main()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nOperation cancelled by user.")
        exit(1)
    except Exception as e:
        # Handle unexpected errors
        print(f"An unexpected error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    run()