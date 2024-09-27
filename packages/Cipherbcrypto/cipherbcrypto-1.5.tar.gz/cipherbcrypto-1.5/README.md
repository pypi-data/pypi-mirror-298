# Cipherbcrypto
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)

Encode string data by zlib, base64 invert, how its work ?

## Installation
Python requires [Python.org](https://www.python.org/) v3,7+ to run.
Install the dependencies and devDependencies and start the server.
```sh
python -m pip install pip
python -m pip install --upgrade pip
pip install Cipherbcrypto
```
## Using

```Python
from Cipherbcrypto import algorithmb
b = algorithmb()
secret = "PRIVATEDATA" # | =wKCQiGADsSzPNNzM30zRzyyM/c1J9kzzBvzsg09TzJe
encode_string = b.encd(secret)
print(encode_string)

decode_string = b.decd(encode_string)
print(decode_string)
```

## License
MIT
**Encode Cipherbcrypt group**