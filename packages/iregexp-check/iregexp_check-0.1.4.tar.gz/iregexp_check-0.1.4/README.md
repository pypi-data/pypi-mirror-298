<h1 align="center">I-Regexp Check</h1>

<p align="center">
<a href="https://datatracker.ietf.org/doc/html/rfc9485">RFC 9485</a> I-Regexp: An Interoperable Regular Expression Format
</p>

<p align="center">
  <a href="https://github.com/jg-rp/rust-iregexp/blob/main/LICENSE.txt">
    <img src="https://img.shields.io/pypi/l/iregexp_check.svg?style=flat-square" alt="License">
  </a>
  <a href="https://github.com/jg-rp/rust-iregexp/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/jg-rp/rust-iregexp/tests.yml?branch=main&label=tests&style=flat-square" alt="Tests">
  </a>
  <br>
  <a href="https://pypi.org/project/iregexp_check">
    <img src="https://img.shields.io/pypi/v/iregexp_check.svg?style=flat-square" alt="PyPi - Version">
  </a>
  <a href="https://pypi.org/project/iregexp_check">
    <img src="https://img.shields.io/pypi/pyversions/iregexp_check.svg?style=flat-square" alt="Python versions">
  </a>
</p>

---

## Install

```
pip install iregexp_check
```

## Usage

```python
from iregexp_check import check

print(check(r"[ab]{3}"))  # True
print(check(r"[0-9]*?"))  # False
```
