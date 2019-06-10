import hashlib
import tempfile
from pathlib import Path

import pytest
from philiprehberger_hash_utils import (
    hash_string,
    hash_bytes,
    hash_file,
    hash_dict,
    verify_checksum,
    SUPPORTED_ALGORITHMS,
)


def test_hash_string_sha256():
    result = hash_string("hello")
    expected = hashlib.sha256(b"hello").hexdigest()
    assert result == expected


def test_hash_string_md5():
    result = hash_string("hello", "md5")
    expected = hashlib.md5(b"hello").hexdigest()
    assert result == expected


def test_hash_bytes():
    data = b"\x00\x01\x02"
    result = hash_bytes(data)
    expected = hashlib.sha256(data).hexdigest()
    assert result == expected


def test_hash_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        f.write(b"file content")
        path = f.name
    result = hash_file(path)
    expected = hashlib.sha256(b"file content").hexdigest()
    assert result == expected
    Path(path).unlink()


def test_hash_dict_deterministic():
    d1 = {"b": 2, "a": 1}
    d2 = {"a": 1, "b": 2}
    assert hash_dict(d1) == hash_dict(d2)


def test_hash_dict_different():
    assert hash_dict({"a": 1}) != hash_dict({"a": 2})


def test_verify_checksum():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        f.write(b"verify me")
        path = f.name
    expected = hashlib.sha256(b"verify me").hexdigest()
    assert verify_checksum(path, expected) is True
    assert verify_checksum(path, "wrong") is False
    Path(path).unlink()


def test_all_algorithms():
    for algo in SUPPORTED_ALGORITHMS:
        result = hash_string("test", algo)
        assert isinstance(result, str)
        assert len(result) > 0


def test_unsupported_algorithm():
    with pytest.raises(ValueError, match="Unsupported"):
        hash_string("test", "sha999")


def test_verify_checksum_case_insensitive():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        f.write(b"case test")
        path = f.name
    expected = hashlib.sha256(b"case test").hexdigest().upper()
    assert verify_checksum(path, expected) is True
    Path(path).unlink()
