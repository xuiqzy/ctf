# Mod 26

Tags: `Category:Cryptography`

Author: Pandu

## Description

Cryptography can be easy, do you know what ROT13 is? `cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_jdJBFOXJ}`

## Hints

Look up what the ROT13 algorithm does.

## Solution

ROT13 ([ROT13 - Wikipedia](https://en.wikipedia.org/wiki/ROT13)) is an algorithm that replaces each letter in a word with the letter thirteen letters after it in the alphabet. It is a special case of the [Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher) where the number by which the letters are rotated equals 13.

If you reach `Z` , you just wrap around to `A` as the next letter. If you assign each letter from `A` to `Z` a number from 0 to 26, this wrapping around can be expressed by `current_letter_as_number + 13) mod 26`, where `a mod b` is the remainder of `a` divided b `b`.  This explains the name `MOD 26` of the challenge.

Note that the [mathematical definition of the modulo operation](https://en.wikipedia.org/wiki/Modular_arithmetic) is different from [the one used in programming](https://en.wikipedia.org/wiki/Modulo_operation) (often expressed by `%` or `mod`); the mathematical one is clearly defined for negative numbers and results in an equivalence class instead of a number as a result. The programming definition for positive numbers is just that of the remainder when dividing two numbers; the behaviour for negative numbers is not consistent between all programming languages.

Because the basic latin alphabet has 26 characters, applying ROT13 to the encrypted ciphertxt results in the original plaintext again (called a reciprocal cipher). The operations for encrypting and decrypting something are the same.

There are ROT13 converters online or you can use e.g. the `codecs` module in python or implement the algorithm yourself as it is fairly easy.

In the rot13 algorithm in the code (in the `solution.py` file in this folder) implemented by our own function instead of the `codecs` module, we use the [ascii value](https://en.wikipedia.org/wiki/ASCII#Printable_characters) of the character to get a number. But since the `a` or `A` are not converted to `0` or `1` but `97` and `65` respectively, we have to subtract that number to get the position in the alphabet for each letter.

We use `0` instead of `1` as the value for `a` and `A` to make calculations with the `%` (modulo) operator possible, which otherwise would result in e.g. `26 % 26 == 0`. That would make it impossible to have a `z` as a result.

If you find this too complicated and don't want to have to do anything with character encodings such as ascii just to implement rot13, you can just create a map (python dictionary) with each character as the key and assign it an int from `0` to `25`. Then you can directly convert each letter (just use all lowercase or all uppercase to make it easier) to a number, do the rotation by 13, and convert it back. No ascii needed :)

There are also some special characters that are not latin alphabet letters included in the encrypted text. They cannot be decrypted by this method since they cannot be mapped to a number between `0` and `25`. We will just add them to the plaintext as is for the resulting flag to make sense.

ROT13 as an encryption is considered trivially easy to crack, as it is a commonly known algorithm with no secret key involved. Thus, it is more appropriately named an encoding than an encryption because it is a fixed transformation without a secret.

Also, patterns in the original text stay there in the ciphertext since each letter is always encrypted to the same ciphertext letter (deterministic transformation). This uneven distribution of ciphertext characters can give away some information about the algorithm used and so trying to hide what algorithm is used would not work, in addition to the usual problems that things such as what algorithm is used nearly always leak into the knowledge of attackers in other ways (see [Security through obscurity - Wikipedia](https://en.wikipedia.org/wiki/Security_through_obscurity)).

Even without knowing the ROT13 algorithm, the patterns in the ciphertext also give away information about the message itself such as the frequency of every letter. With this frequency information, the original plaintext can easily be reconstructed by matching the most frequent ciphertext letter to the original letter that is most frequent in normal text (e.g. the letter `e` in English) and so on for the other letters.

Better choose a secure, tried and tested, encryption algorithm implemented by a well known library which has a secret key and concentrate your efforts on keeping that key private.
