# philiprehberger-hash-utils

[![Tests](https://github.com/philiprehberger/py-hash-utils/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-hash-utils/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-hash-utils.svg)](https://pypi.org/project/philiprehberger-hash-utils/)
[![License](https://img.shields.io/github/license/philiprehberger/py-hash-utils)](LICENSE)

Simplified hashing helpers for strings, files, and checksums.

## Installation

```bash
pip install philiprehberger-hash-utils
```

## Usage

### Hash Strings and Bytes

```python
from philiprehberger_hash_utils import hash_string, hash_bytes

hash_string("hello world")                # SHA-256 hex digest
hash_string("hello world", "md5")         # MD5 hex digest
hash_bytes(b"\x00\x01\x02", "sha512")    # SHA-512 hex digest
```

### Hash Files

```python
from philiprehberger_hash_utils import hash_file

digest = hash_file("large_file.bin")  # Streams in chunks
digest = hash_file("data.csv", algorithm="blake2b")
```

### Hash Dictionaries

```python
from philiprehberger_hash_utils import hash_dict

# Deterministic — key order doesn't matter
hash_dict({"b": 2, "a": 1}) == hash_dict({"a": 1, "b": 2})  # True
```

### Verify Checksums

```python
from philiprehberger_hash_utils import verify_checksum

# Timing-safe comparison
is_valid = verify_checksum("download.zip", expected_sha256)
```

### Supported Algorithms

`md5`, `sha1`, `sha256` (default), `sha512`, `blake2b`

## API

| Function / Class | Description |
|------------------|-------------|
| `hash_string(s, algorithm="sha256")` | Hash a string |
| `hash_bytes(data, algorithm="sha256")` | Hash raw bytes |
| `hash_file(path, algorithm="sha256", chunk_size=8192)` | Hash a file (streaming) |
| `hash_dict(d, algorithm="sha256")` | Deterministic dict hash |
| `verify_checksum(path, expected, algorithm="sha256")` | Timing-safe file verification |


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
