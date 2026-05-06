"""Dataset path helpers for raw and processed energy arbitrage data."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DatasetPaths:
    raw: Path
    processed: Path
    external: Path


def default_dataset_paths(project_root: Path) -> DatasetPaths:
    data_root = project_root / "data"
    return DatasetPaths(
        raw=data_root / "raw",
        processed=data_root / "processed",
        external=data_root / "external",
    )
