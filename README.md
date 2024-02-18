# Cryptography Project
This python file uses three types of ciphers to encrypt and decrypt text. The file uses command-line arguments to specify encryption, key/passwords, and text. 

## Use
Download the crypto.py file and run from the terminal with non-positional command-line arguments. The argparse python module is necessary to run this program.

-h : help

-a : algorithm type, one from {substitution, railfence, playfair}

-e/-d : mode, encryption or decryption

-k/--key : key/password, quotes required, for substitution or playfair

-t/--text : text to be encrypted/decrypted, quotes required

## 1) Substitution
This method uses a substitution cipher with an alphabetic key. 

Example: crypt.py -a substitution -e -k "password" -t "hello world"

## 2) Railfence
This method uses a 2-rail railfence cipher to crypt text.

Example: crypt.py -a railfence -d -t "hlowrdel ol"

## 3) Playfair
This method uses the playfair cipher and an alphabetic key to generate a 5x5 grid. J's are replaced with I's and removes spaces from text.

Example: crypt.py -a playfair -e -k "password" -t "hello world"
