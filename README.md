# RSA
This program generates an RSA encrypted message which is further broken down into Shamir Secret shares. It also decrypts the encrypted message back to its original form.

Running this program requires pycryptodome library.
```
pip install pycryptodome
```
## RSA Principles
The basic idea of how RSA encryption/decryption works is the difficulty of factoring a very, very large number in a timely manner.
The formula to encrypt is: $C$ = $m^e$ mod $N$, where C = ciphertext, m = message, e = public key, and $N$ = $p * q$ where p and q are very, very large prime numbers.
The formula to decrypt is: $D$ = $C^d$ mod $N$, where D = decrypted message (or m) and d = private key.
How e and d are set is through the formula: e * d = 1 (mod phi_N), where phi_N = (p - 1) * (q - 1). From the formula, we can see that e and d are multiplicative inverses of each other, and through applying this inverse relatioinship, we are able to encrypt and decrypt the original message.

### Why is phi_N equal to (p - 1) * (q - 1)?
The foundation of this relationship is what is known as the Euler's Totient function. Euler's Totient function states that phi_N is the count of integers mod N relatively prime to N, which is simply (p - 1) * (q - 1). For example, if N = 15 where p = 3 and q = 5, then the integers mod N relatively prime to N would be {1, 2, 4, 7, 8, 11, 13, 14}. The length of this set is 8, which is the same as (3 - 1) * (5 - 1) = 8. Therefore, phi_N = 8.

### Shamir Secret Sharing Principles
The idea of Shamir Secret Sharing is to release the message, m, only if a cerntain number of users are present called the quorum. The secret message can be divided up into however many fragments, but as long as the quorum is met, then the secret can be released. The fragments are formed through system of linear equations taking the form: f(x) = $a_{q-1}x^{q-1}$ + ... + $a_ix$ + $a_0$ (mod N), where $a_0$ is the secret message, m.

For example, it can be divided among 5 people with $q = 3$ (quorum) in this manner:
1. f(1) = $a_2 + a_1 + a_0$ (mod N)
2. f(2) = $4a_2 + 2a_1 + a_0$ (mod N)
3. f(3) = $9a_2 + 3a_1 + a_0$ (mod N)
4. f(4) = $16a_2 + 4a_1 + a_0$ (mod N)
5. f(5) = $25a_2 + 5a_1 + a_0$ (mod N)

One user holds one quation, and any 3 equations out of the 5 can be used to solve for $a_0$ (secret message, m). So, as long as 3 users are present, the secret can be unlocked.
