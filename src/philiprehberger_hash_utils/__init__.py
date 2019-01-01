"""Simplified hashing helpers for strings, files, and checksums."""

from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path


__all__ = [
    "hash_string",
    "hash_bytes",
    "hash_file",
    "hash_dict",
    "verify_checksum",
    "SUPPORTED_ALGORITHMS",
]

SUPPORTED_ALGORITHMS: list[str] = ["md5", "sha1", "sha256", "sha512", "blake2b"]


def _get_hasher(algorithm: str) -> "hashlib._Hash":
    if algorithm not in SUPPORTED_ALGORITHMS:
        msg = (
            f"Unsupported algorithm: '{algorithm}'. "
            f"Supported: {', '.join(SUPPORTED_ALGORITHMS)}"
        )
        raise ValueError(msg)
    return hashlib.new(algorithm)


def hash_string(s: str, algorithm: str = "sha256") -> str:
    """Return the hex digest of a string.

    Args:
        s: The string to hash.
        algorithm: Hash algorithm name. Defaults to ``"sha256"``.

    Returns:
        Hex-encoded hash digest.
    """
    h = _get_hasher(algorithm)
    h.update(s.encode("utf-8"))
    return h.hexdigest()


def hash_bytes(data: bytes, algorithm: str = "sha256") -> str:
    """Return the hex digest of raw bytes.

    Args:
        data: The bytes to hash.
        algorithm: Hash algorithm name. Defaults to ``"sha256"``.

    Returns:
        Hex-encoded hash digest.
    """
    h = _get_hasher(algorithm)
    h.update(data)
    return h.hexdigest()


def hash_file(
    path: str | Path,
    algorithm: str = "sha256",
    chunk_size: int = 8192,
) -> str:
    """Return the hex digest of a file's contents.

    Streams the file in chunks for memory efficiency with large files.

    Args:
        path: Path to the file.
        algorithm: Hash algorithm name. Defaults to ``"sha256"``.
        chunk_size: Read buffer size in bytes.

    Returns:
        Hex-encoded hash digest.
    """
    h = _get_hasher(algorithm)
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def hash_dict(d: dict, algorithm: str = "sha256") -> str:  # noqa: ANN401
    """Return a deterministic hex digest of a dictionary.

    Keys are sorted recursively to ensure consistent hashing
    regardless of insertion order.

    Args:
        d: The dictionary to hash.
        algorithm: Hash algorithm name. Defaults to ``"sha256"``.

    Returns:
        Hex-encoded hash digest.
    """
    serialized = json.dumps(d, sort_keys=True, separators=(",", ":"), default=str)
    return hash_string(serialized, algorithm)


def verify_checksum(
    path: str | Path,
    expected: str,
    algorithm: str = "sha256",
) -> bool:
    """Verify that a file's hash matches an expected checksum.

    Uses timing-safe comparison to prevent timing attacks.

    Args:
        path: Path to the file.
        expected: Expected hex-encoded hash digest.
        algorithm: Hash algorithm name. Defaults to ``"sha256"``.

    Returns:
        True if the file's hash matches the expected value.
    """
    actual = hash_file(path, algorithm)
    return hmac.compare_digest(actual.lower(), expected.lower())
