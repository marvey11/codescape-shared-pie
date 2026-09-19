from pathlib import Path
from unittest.mock import patch

import pytest

from codescape.util.fileutils import atomic_move, atomic_write_bytes


def test_atomic_move_copies_target_and_removes_source(tmp_path: Path) -> None:
    source_file = tmp_path / "source.txt"
    target_file = tmp_path / "nested" / "target.txt"
    source_file.write_bytes(b"move me")

    atomic_move(source_file, target_file)

    assert target_file.read_bytes() == b"move me"
    assert not source_file.exists()


def test_atomic_move_verifies_matching_hash_before_removing_source(
    tmp_path: Path,
) -> None:
    source_file = tmp_path / "source.txt"
    target_file = tmp_path / "target.txt"
    source_file.write_bytes(b"verified content")

    atomic_move(source_file, target_file, verify_hash=True)

    assert target_file.read_bytes() == b"verified content"
    assert not source_file.exists()


def test_atomic_move_keeps_source_when_hashes_do_not_match(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_file = tmp_path / "source.txt"
    target_file = tmp_path / "target.txt"
    source_file.write_bytes(b"source content")
    digest_results = iter((b"source", b"target"))

    def fake_file_digest(path: Path, algorithm: str) -> bytes:
        return next(digest_results)

    monkeypatch.setattr("codescape.util.fileutils._file_digest", fake_file_digest)

    with pytest.raises(ValueError, match="hashes do not match"):
        atomic_move(source_file, target_file, verify_hash=True)

    assert source_file.exists()


def test_atomic_move_accepts_hash_algorithm(tmp_path: Path) -> None:
    source_file = tmp_path / "source.txt"
    target_file = tmp_path / "target.txt"
    source_file.write_bytes(b"algorithm selection")

    atomic_move(
        source_file,
        target_file,
        verify_hash=True,
        hash_algorithm="sha512",
    )

    assert not source_file.exists()


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
