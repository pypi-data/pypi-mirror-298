# pdf2index

[![PyPI - Version](https://img.shields.io/pypi/v/pdf2index.svg)](https://pypi.org/project/pdf2index)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pdf2index.svg)](https://pypi.org/project/pdf2index)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install pdf2index
```

Consider installing in a `venv` or using `pipx`

Warning: This package has large dependencies. You will be downloading ~2 GB.

Warning: Currently this package is optimised for amd gpus with ROCm.

## Usage

```console
pdf2index book1.pdf book2.pdf book3.pdf --password $(<password_file.txt) --out index.txt
```

Note: The order of the pdfs matters as the books will be referenced in that order.

## Dev

```console
# Enter env
hatch shell
time HSA_OVERRIDE_GFX_VERSION=11.0.0 pdf2index data/Book* -p $(<data/passwd/passwd.txt)
```

Monitor gpu usage with `amdgpu_top`.

### Check ROCm availability

- install `rocminfo`
- run python script `helpers/rocm_test.py`

## License

`pdf2index` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
