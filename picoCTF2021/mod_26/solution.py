#!/usr/bin/python3 -u
import codecs


def get_rot13_applied(ciphertext: str):
    plaintext = ""
    for ciphertext_letter in ciphertext:
        ciphertext_letter_is_in_latin_alphabet = ciphertext_letter.isalpha() and ciphertext_letter.isascii()
        if not ciphertext_letter_is_in_latin_alphabet:
            plaintext += ciphertext_letter
            continue

        if ciphertext_letter.islower():
            ascii_value_to_position_in_alphabet_shift = ord("a")
        else:
            ascii_value_to_position_in_alphabet_shift = ord("A")

        ascii_value = ord(ciphertext_letter)
        encrypted_position_in_alphabet_starting_with_0 = ascii_value - ascii_value_to_position_in_alphabet_shift
        decrypted_position_in_alphabet = (encrypted_position_in_alphabet_starting_with_0 + 13) % 26

        plaintext_letter = chr(decrypted_position_in_alphabet + ascii_value_to_position_in_alphabet_shift)

        plaintext += plaintext_letter

    return plaintext


ENCRYPTED_FLAG = "cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_jdJBFOXJ}"
print(f"Encrypted flag: {ENCRYPTED_FLAG}")

# either us the codecs python module or write an own rot13 function, see above
# flag_only_letters = codecs.encode(encrypted_flag_only_letters, "rot13")
decrypted_flag = get_rot13_applied(ENCRYPTED_FLAG)


print(f"Decrypted flag: {decrypted_flag}")
