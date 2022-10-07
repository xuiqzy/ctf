# No Padding, No Problem

90 points

Tags: `Category: Cryptography`

Author: Sara

## Description

Oracles can be your best friend, they will decrypt anything, except the flag's ciphertext. How will you break it? Connect with `nc mercury.picoctf.net 28517`.

## Walkthrough

So let's start by playing around with it by connecting to it with the command line tool netcat as described:

```
> nc mercury.picoctf.net 28517
Welcome to the Padding Oracle Challenge
This oracle will take anything you give it and decrypt using RSA. It will not accept the ciphertext with the secret message... Good Luck!


n: 59866201650591105514449902904967946132952987226199253259076227417753038999368975462915212188619093237291063093744682659641681103322406526779604115019228628244221254346582055178837455954757663691089435783524670493367716346080054286951036640513287395819782025555805386581259439088331925358682133728196972745227
e: 65537
ciphertext: 8563862546151248534941136954208675466357179974895773245298191099452276976225047649870450352391705518476779351266842102767046468848473822492882700695108177437384935883764112666899396292784484429764273096879809639733940121589363071915331802691299544461712020631282264406655513083643376195045713520223268600417


Give me ciphertext to decrypt: 
```

So let's try some values:

```
Give me ciphertext to decrypt: 1
Here you go: 1
Give me ciphertext to decrypt: 2
Here you go: 31980923372401971912244510181579980084198849408655733520925907448721111959469906176335845920828429916858922264879502921029389000382750469896476998660911609611856419061725130146069676506518886048905966589293302241602314822154128337248569336518186039841019361179081449016685696254908950417281905456100689770808
Give me ciphertext to decrypt: 3
Here you go: 53718790427442807370103460179190832251387592453767616666470737400939808815656424767958319792255130001194866103618094957082239180942844610489093278565290186538971173470076212769135726408850019664280763962549504321468937199329808359630498623341990713208183983570762610727101484347602576819635103388730952830973
Give me ciphertext to decrypt: 9984654651
Here you go: 59709045694219226771711510334644133177874653557814515880698595885506340464173826746553307609966845980257631543487767600141020965855067128695611374872827767950269441033081405812169738016289608688609558074186265380068242840712227446600828277691138092750721163938331479958722973689822280199345172200498285978483
Give me ciphertext to decrypt: 8563862546151248534941136954208675466357179974895773245298191099452276976225047649870450352391705518476779351266842102767046468848473822492882700695108177437384935883764112666899396292784484429764273096879809639733940121589363071915331802691299544461712020631282264406655513083643376195045713520223268600417
Will not decrypt the ciphertext. Try Again
Give me ciphertext to decrypt: ianteruidnt
Give me ciphertext to decrypt: 
```

Note that the initial `n`, `e` and `ciphertext` change with each new connection to the server using netcat, so we need to be careful to use the values of the current connection, otherwise the oracle decrypts ciphertexts for us based on another private key `d` and another `n` and another corresponding `ciphertext`!

So we can see that it does not decrypt the ciphertext of the flag or any non-number, but decrypts everything else. This is called an oracle because it gives us information that we could not have without knowing the private key. We also already have the right ciphertext that is the encrypted flag, so this is not about brute-forcing our answer. We already have our encrypted answer.

Also note the title `No Padding, No Problem`. It indicates that the flag was encrypted without padding. Padding the ciphertext correctly before encryption is essential for RSA security, so this could be a way to attack it.

In [RSA (cryptosystem) - Wikipedia #Attacks against Plain (Unpadded) RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Attacks_against_plain_RSA), we can see explained that "RSA has the property that the product of two ciphertexts is equal to the encryption of the product of the respective plaintexts. That is $m_1^e * m_2^e \equiv (m_1 * m_2)^e \mod{n}$."

Let's say our plaintext message `m` is $m_1$.

We can now calculate a new different ciphertext $c_2$ that the oracle will decrypt for us and reveal the message $m_1$ through that. For that, we chose any plaintext $m_2$ and calculate $c_2 \equiv m_1^e * m_2^e \equiv (m_1 * m_2)^e \mod{n}$. The good thing is that because we multiply modulo `n`, we don't need to know the value $m_1^e$ but just need any value that is congruent to $m_1^e$ modulo `n` — which we do with our `ciphertext`!

```python
c_2_big = original_ciphertext_of_interest * (m_2 ** e)
c_2 = c_2_big % n
```

When we give the oracle this value $c_2$, it will most likely be different from `c` and thus, it will decrypt it for us.

If we manually make our calculations or call a script from the output of the oracle on the server and then paste our result, the connection might be closed and the values will not match with a new connection. We therefore make a script `main.py` which not only calculates $c_2$ for us but also gets the initial values from the server response, sends our value $c_2$ to the server after calculating it and finally printing the respone from the server. Take a look at it for more details and explanations. It uses the [pwntools](https://docs.pwntools.com/en/stable/intro.html) library to make connecting and parsing the output from the server a lot easier and gives us nice output meanwhile, but you could also do the same with only python built-in modules.

The value $c_2$ decrypted by the oracle will give us back $m_1 * m_2$, which we just need to divide —modulo `n` — by our known $m_2$ to get the secret plaintext $m_1$. Simple division might not work because the result must be an integer again. So it is done by multiplying with the multiplicative inverse, which in the case of division modulo `n` is the modular multiplicative inverse for $m_2$ modulo `n`.
We achieve that in Python 3.8 and later through:

```python
multiplicative_inverse_of_m_2 = pow(m_2, -1, n)
```

We need to take the result of `m_1_times_m_2 * multiplicative_inverse_of_m_2` modulo `n` in case it is larger or equal to `n`, as only those numbers are possible valid encodings of the original secret plaintext.

Then we need to decode the resulting integer into a string again. We do this by taking the hex string represantation of it, interpreting every 2 bytes (2 characters in the hex string) as one byte of data and decode that data into a string under the UTF-8 encoding.

```python
hex_string_no_0x_prefix = f"{m_1:02x}"
cleartext_bytes = unhexlify(hex_string_no_0x_prefix)
cleartext_flag = cleartext_bytes.decode("utf-8")
print(f"solution: {cleartext_flag}")
```

We finally get the flag: `picoCTF{m4yb3_Th0se_m3s54g3s_4r3_difurrent_4005534}`
