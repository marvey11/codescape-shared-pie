from pathlib import Path
from unittest.mock import patch

import pytest

from codescape.util.fileutils import atomic_write_bytes


def test_atomic_write_bytes_creates_file_and_content(tmp_path: Path) -> None:
    target_file = tmp_path / "output.txt"
    data = b"hello world"

    atomic_write_bytes(target_file, data)

    assert target_file.exists()
    assert target_file.read_bytes() == data


def test_atomic_write_bytes_creates_parent_directories(tmp_path: Path) -> None:
    target_file = tmp_path / "nested" / "deeply" / "output.bin"
    data = b"\x00\x01\x02\x03"

    atomic_write_bytes(target_file, data)

    assert target_file.exists()
    assert target_file.read_bytes() == data


def test_atomic_write_bytes_accepts_string_path(tmp_path: Path) -> None:
    target_file = tmp_path / "string_path.txt"
    data = b"string path test"

    atomic_write_bytes(str(target_file), data)

    assert target_file.exists()
    assert target_file.read_bytes() == data


def test_atomic_write_bytes_overwrites_existing_file(tmp_path: Path) -> None:
    target_file = tmp_path / "existing.txt"
    target_file.write_bytes(b"initial data")

    new_data = b"updated data"
    atomic_write_bytes(target_file, new_data)

    assert target_file.read_bytes() == new_data


def test_atomic_write_bytes_cleans_up_tmp_file_on_write_failure(tmp_path: Path) -> None:
    target_file = tmp_path / "failed_write.txt"
    data = b"some data"

    # Simulate an I/O error during the write operation
    with patch("tempfile.NamedTemporaryFile") as mock_tmp:
        mock_file = mock_tmp.return_value.__enter__.return_value
        mock_file.name = str(tmp_path / "temp_file_to_cleanup")
        mock_file.write.side_effect = OSError("Disk write error")

        # Create the temporary file manually so tmp_path.exists() can check it
        temp_path = Path(mock_file.name)
        temp_path.touch()

        with pytest.raises(IOError, match="Disk write error"):
            atomic_write_bytes(target_file, data)

        # Verify the temporary file was cleaned up and target was not created
        assert not temp_path.exists()
        assert not target_file.exists()


def test_atomic_write_bytes_cleans_up_tmp_file_on_fsync_failure(tmp_path: Path) -> None:
    target_file = tmp_path / "fsync_failure.txt"
    data = b"some data"

    with patch("os.fsync", side_effect=OSError("Sync failed")):
        with pytest.raises(OSError, match="Sync failed"):
            atomic_write_bytes(target_file, data)

        assert not target_file.exists()
        # Verify no orphan temporary files remain in the target directory
        remaining_files = list(tmp_path.glob("*"))
        assert len(remaining_files) == 0
