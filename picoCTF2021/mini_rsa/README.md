# Mini RSA

### Mini RSA

70 points

Tags: `Category: Cryptography`

Author: Sara

## Description

What happens if you have a small exponent? There is a twist though, we 
padded the plaintext so that (M ** e) is just barely larger than N. 
Let's decrypt this: [ciphertext](https://mercury.picoctf.net/static/71f49c1459c00de5335d5dddc86c8841/ciphertext)

## Solution

Download the linked file and open it in a text editor:

```
N: 1615765684321463054078226051959887884233678317734892901740763321135213636796075462401950274602405095138589898087428337758445013281488966866073355710771864671726991918706558071231266976427184673800225254531695928541272546385146495736420261815693810544589811104967829354461491178200126099661909654163542661541699404839644035177445092988952614918424317082380174383819025585076206641993479326576180793544321194357018916215113009742654408597083724508169216182008449693917227497813165444372201517541788989925461711067825681947947471001390843774746442699739386923285801022685451221261010798837646928092277556198145662924691803032880040492762442561497760689933601781401617086600593482127465655390841361154025890679757514060456103104199255917164678161972735858939464790960448345988941481499050248673128656508055285037090026439683847266536283160142071643015434813473463469733112182328678706702116054036618277506997666534567846763938692335069955755244438415377933440029498378955355877502743215305768814857864433151287
e: 3

ciphertext (c): 1220012318588871886132524757898884422174534558055593713309088304910273991073554732659977133980685370899257850121970812405700793710546674062154237544840177616746805668666317481140872605653768484867292138139949076102907399831998827567645230986345455915692863094364797526497302082734955903755050638155202890599808146919581675891411119628108546342758721287307471723093546788074479139848242227243523617899178070097350912870635303707113283010669418774091018728233471491573736725568575532635111164176010070788796616348740261987121152288917179932230769893513971774137615028741237163693178359120276497700812698199245070488892892209716639870702721110338285426338729911942926177029934906215716407021792856449586278849142522957603215285531263079546937443583905937777298337318454706096366106704204777777913076793265584075700215822263709126228246232640662350759018119501368721990988895700497330256765579153834824063344973587990533626156498797388821484630786016515988383280196865544019939739447062641481267899176504155482
```

The description says that `M ^ e` is only slightly larger than `N`. We know that to get the ciphertext `c` the result of `M ^ e` is taken modulo `N`. If it is really only slightly bigger, that means `M ^ e` is equal to `N + c`. 

Because `e` is `3`, let's try to simply compute the cube root of `N + c`, assuming that `N < c < 2N`, to find the value M (our original message that was encrypted via `M ^ e (mod N)`). This is not a mathematically hard computation.

For a big `c`, python can't just compute `c ** (1/3)` (the cube root) because `OverflowError: int too large to convert to float`; it converts `c` to a float to raise it to the power of a float.

Also see the code in the `main.py` file in this folder.

Instead, we can use a binary search to search for an `M` that satisfies `M ^ 3 = N + c`. From [this stackoverflow post](https://stackoverflow.com/questions/23621833/is-cube-root-integer), we take the following python code (licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)):

```python
def find_cube_root(n):
    lo = 0
    hi = 1 << ((n.bit_length() + 2) // 3)
    while lo < hi:
        mid = (lo+hi)//2
        if mid**3 < n:
            lo = mid+1
        else:
            hi = mid
    return lo
def is_perfect_cube(n):
    return find_cube_root(n)**3 == n
```

But `N + e` doesn't seem to have a perfect cube root.

Let's define `N + e` to be `real_c`.

```python
real_c = N + e
bla = find_cube_root(real_c)
bla ** 3 == real_c # is False :(
bla ** 3 > real_c # True

blub = find_cube_root(real_c) - 1
blub ** 3 == real_c # is False :(
blub ** 3 < real_c # True
```

We can see that `N + e` does not have a perfect cube root and it isn't some off-by-one error either. The value `bla` is too small to be the cube root and the next bigger integer `blub` is too large to be the cube root.

Maybe `M ^ c` is not just a bit larger than `N` but still only a few times larger than `N`, so let's test the same with it being a bit larger than `2*N`, `3*N`, etc. with a little brute force script.

```python
i = 0
while True:
    print("trying", i)
    potential_cube_root = find_cube_root((i * n) + c)
    is_perfect_cube_root = (potential_cube_root ** 3) == ((i * n) + c)
    if is_perfect_cube_root:
        print(i)
        break

    i += 1
```

We can see that in round 3533, it breaks and prints out `3533`. So the result is indeed a perfect cube root:

```python
cube_root = find_cube_root(3533 * n + c)
print(cube_root ** 3 == 3533 * n + c) # prints True
print(f"{cube_root = }")
# prints:
# 1787330808968142828287809319332701517353332911736848279839502759158602467824780424488141955644417387373185756944952906538004355347478978500948630620749868180414755933760446136287315896825929319145984883756667607031853695069891380871892213007874933611243319812691520078269033745367443951846845107464675742664639073699907476681022428557437
```

How do we get the text of the flag?

RSA operates on numbers, so a typical way is to convert each character to its unicode codepoint (same as the ASCII value for a lot of basic characters) and express this number as a hex string ("A" -> codepoint 65 -> hex string (0x)41). Then, we concatenate the hex strings for each individual character (without the `0x`) and treat the resulting hex string as one combined huge hex number and convert it to a decimal number or rather just use that signle number in the RSA algorithm.

So to reverse this, we need to print out our number as a hex string or convert our decimal number to a hex string and then treat each pair of characters in the hex string as its own number and convert that unicode codepoint back to the real character it represents.

```python
hex_string_no_0x_prefix = f"{cube_root:02x}"
# every 2 hex characters in the hex string are treated as one hex number,
# this number is one byte big and stored as bytes (a list of bytes)
text_bytes = binascii.unhexlify(hex_string_no_0x_prefix)
# treat bytes as utf-8 (superset of ascii) and convert to text
text = text_bytes.decode("utf-8")
print(f"{text=}")
# prints (look at the end of the next line!):
# text = '                                                                                                        picoCTF{e_sh0u1d_b3_lArg3r_60ef2420}'
```

The whitespace at the start is called a padding but in this case, the original padded value raised to the power of a small exponent made the resulting number still too small and thus easily brute-forceable. The power of RSA comes from the fact that finding the root modulo `N` is very hard, but only if the original number was very big and it is therefore hard to reconstruct or guess this number by only looking at `c`. In this case, the original `M` and `e` were both not very big, leading to an `M ^ e` that was too small and too easy to guess from knowing `c`.

So there we have our flag!

`picoCTF{e_sh0u1d_b3_lArg3r_60ef2420}`
