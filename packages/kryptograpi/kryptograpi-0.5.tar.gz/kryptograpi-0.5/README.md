# Kryptograpi

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/my-library)](https://pypi.org/project/my-library/)

## Overview

Welcome to **Kryptograpi**: where encryption meets humor and mathematical randomness! This utterly groundbreaking (and intentionally insecure) library utilizes the digits of Pi to encrypt and decrypt data, proving once and for all that not all math is serious business.

Get your digits of Pi [here](https://pi2e.ch/blog/2017/03/10/pi-digits-download/), and prepare for a descend in kryptograpically verifiable absurdity!

## Why Use Kryptograpi?

- **Novelty:** Tired of boring encryption methods? So are we! Kryptograpi adds a splash of whimsy to your data protection needs.
- **Simplicity:** It's as simple as pi! If you can count to 3.14159, you’re halfway there.
- **Irrelevant:** You are not the only one struggeling with finding your place in this world! 
- **Insecure:**   Just like you in any social setting!

## Usage

```python
#Import all existing methods
from kryptograpi.functions import define_pi,encrypt,decrypt

#Define py (parse path to your Pi file if desired)
pi=define_pi()

#Encrypt 13
message=13
cipher_data=encrypt(pi,message)

#Output results
print("Cipher Data: ", cipher_data)
print("Decryption result: ", decrypt(pi,cipher_data))

#Cipher Data:  [403706, 18, {3: '9', 4: '4', 11: '8'}]
#Decryption result:  13
```
