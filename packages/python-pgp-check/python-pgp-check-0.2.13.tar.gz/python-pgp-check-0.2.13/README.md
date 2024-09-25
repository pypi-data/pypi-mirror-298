# Python PGP Check

A quick python CLI tool to verify file PGP hashes


### Installation and usage

Install it with python pip using 

``` bash
    pip install python-pgp-check
```

### Usage
Calculate Hash

to calculate the hash of a file:
```bash
    python-pgp-check <file_path>
``` 

Verify Hash

To verify a file against an expected hash:
```bash
    python-pgp-check <file_path> <expected_hash>
```

Specifying Hash Algorithm

By default, SHA-256 is used. To use a different algorithm:

```bash
    python-pgp-check <file_path> [<expected_hash>] --algorithm <algorithm>
```

Supported algorithms: md5, sha1, sha256, sha512

### Examples

Calculate SHA-256 hash:
```bash
    python-pgp-check /path/to/file
```
Verify file with SHA-256 hash:
```bash
python-pgp-check /path/to/file 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

Calculate MD5 hash:
```bash
python-pgp-check /path/to/file --algorithm md5
```
Verify file with SHA-512 hash:
```bash
python-pgp-check /path/to/file 3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2 --algorithm sha512
```