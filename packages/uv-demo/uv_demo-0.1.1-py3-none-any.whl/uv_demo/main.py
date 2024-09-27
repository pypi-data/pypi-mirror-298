"""Example file."""

import time

import torch
from loguru import logger as log
from rich.progress import Progress


def main() -> None:
    """Main function."""

    log.info(f"PyTorch version: {torch.__version__}")
    if torch.cuda.is_available():
        log.info(f"GPU: {torch.cuda.get_device_name(0)}")
    else:
        log.info("No GPU available.")

    log.info("Hello UV!")
    with Progress() as progress:
        total: int = 20
        download_task = progress.add_task("[red]Downloading...", total=total)
        for step in range(total):
            time.sleep(0.1)
            if step == total // 2:
                progress.console.print("Halfway there!")
            progress.update(download_task, advance=1)


if __name__ == "__main__":
    main()
