import hashlib
import os
import shutil
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


def atomic_move(
    source_path: Path | str,
    target_path: Path | str,
    *,
    verify_hash: bool = False,
    hash_algorithm: str = "sha256",
) -> None:
    """
    Move a file safely, including when source and target use different filesystems.

    The file is copied to a temporary file in the target directory and atomically
    replaced into place. The source is removed only after the copy succeeds.

    When ``verify_hash`` is true, the source and target digests are compared before
    the source is removed.
    """
    source = Path(source_path)
    target = Path(target_path)
    if verify_hash:
        hashlib.new(hash_algorithm)

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "wb", dir=target.parent, delete=False
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            with source.open("rb") as source_file:
                shutil.copyfileobj(source_file, temporary_file)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        temporary_path.replace(target)

        if verify_hash:
            source_digest = _file_digest(source, hash_algorithm)
            target_digest = _file_digest(target, hash_algorithm)
            if source_digest != target_digest:
                raise ValueError("source and target hashes do not match")

        source.unlink()
    except Exception:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()
        raise


def _file_digest(path: Path, algorithm: str) -> bytes:
    digest = hashlib.new(algorithm)
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.digest()
