from binascii import unhexlify
from typing import Iterable

import pwn

HOST = "mercury.picoctf.net"
PORT = 28517

# used for attack, can be anything greater than 1
M_2: int = 2

connection = pwn.remote(HOST, PORT)
received_bytes = connection.recvuntil(b"Give me ciphertext to decrypt: ")
received_text: str = received_bytes.decode("utf-8")


all_lines = received_text.splitlines()

print()
print("==== initial response ====")
print("\n".join(all_lines))
print("==== initial response end ====")
print()


def get_number_from_answer_by_line_prefix(response_all_lines: Iterable[str], line_prefix: str) -> int:
    result = ""

    for line in response_all_lines:
        if not line.startswith(line_prefix):
            continue

        result = line.removeprefix(line_prefix)

    assert result != ""

    result_number = int(result)

    return result_number


e = get_number_from_answer_by_line_prefix(all_lines, "e: ")
print(f"{e=}")
n = get_number_from_answer_by_line_prefix(all_lines, "n: ")
print(f"{n=}")
ciphertext = get_number_from_answer_by_line_prefix(all_lines, "ciphertext: ")
print(f"{ciphertext=}")


def calculate_ciphertext_for_padding_oracle_attack(original_ciphertext_of_interest: int, e: int, n: int, m_2: int) -> int:
    c_2_big = original_ciphertext_of_interest * (m_2**e)
    c_2 = c_2_big % n

    return c_2


c_2 = calculate_ciphertext_for_padding_oracle_attack(ciphertext, e, n, M_2)

print()
print(f"{c_2=}")
print()


def get_decrypted_ciphertext(connection: pwn.tubes.tube, ciphertext: int) -> int:
    connection.sendline(str(ciphertext).encode("utf-8"))

    received_bytes = connection.recvuntil(b"Give me ciphertext to decrypt: ")
    received_text: str = received_bytes.decode("utf-8")
    all_lines = received_text.splitlines()

    print()
    print("==== response ====")
    print("\n".join(all_lines))
    print("==== response end ====")
    print()

    decrypted_result = get_number_from_answer_by_line_prefix(all_lines, "Here you go: ")

    return decrypted_result


decrypted_c_2 = get_decrypted_ciphertext(connection, c_2)

m_1_times_m_2 = decrypted_c_2
print(f"{m_1_times_m_2=}")


def calculate_secret_plaintext_from_decrypted_padding_oracle_attack_plaintext_answer(m_1_times_m_2: int, m_2: int) -> int:

    multiplicative_inverse_of_m_2 = pow(m_2, -1, n)
    print(f"{multiplicative_inverse_of_m_2=}")
    assert multiplicative_inverse_of_m_2 < n

    m_1_big = m_1_times_m_2 * multiplicative_inverse_of_m_2

    assert int(m_1_big) == m_1_big

    m_1 = m_1_big % n

    return m_1


m_1 = calculate_secret_plaintext_from_decrypted_padding_oracle_attack_plaintext_answer(m_1_times_m_2, M_2)

print(f"{m_1=}")


def get_utf_8_string_from_binary_data_integer(binary_data_as_number: int) -> str:
    hex_string_no_0x_prefix = f"{binary_data_as_number:02x}"
    cleartext_bytes = unhexlify(hex_string_no_0x_prefix)
    cleartext_string = cleartext_bytes.decode("utf-8")

    return cleartext_string


cleartext_flag = get_utf_8_string_from_binary_data_integer(m_1)
print()
print(f"Solution: {cleartext_flag}")
