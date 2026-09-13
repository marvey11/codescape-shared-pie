import os
import tempfile
from pathlib import Path


def atomic_write_bytes(path: Path | str, data: bytes) -> None:
    """Atomically write bytes to a file destination.

    Creates a temporary file in the target directory, writes data,
    flushes and syncs to disk, and replaces the target atomically.
    """
    target_path = Path(path)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "wb", dir=target_path.parent, delete=False
        ) as tmp_file:
            tmp_path = Path(tmp_file.name)
            tmp_file.write(data)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())

        tmp_path.replace(target_path)
    except Exception:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()
        raise
