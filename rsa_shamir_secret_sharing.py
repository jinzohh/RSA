import math
import random
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
import time

def generate_shares(secret, field, shares, threshold):
    # Initialize variables.
    q = threshold
    m = shares
    a0 = secret
    mod_val = field
    a_val = []
    share_val = []

    # Get random integers for the required a values besides a0(secret).
    for i in range(q-1):
        a_val.append(random.randint(1, a0 * 2))

    # Perform operation using the formula: [a(q-1)x^(q-1)+..+ a1x + a0] mod m.
    # Get each share values (fragments of the function).
    # Return the fragment secrets as a set of points (x, y).
    for i in range(1, m+1):
        w = q - 1
        t = 0
        
        for j in a_val:
            t += j * (i ** w)
            w -= 1
        
        t += a0
        t = t % mod_val
        share_val.append((i, t))

    return share_val

def reconstruct_secret(points, field):
    # Initialize variables.
    q = points
    q_len = len(q)
    mod_val = field
    matrix_1 = []

    # Make a 2D matrix comprising the coefficients of the system of equations.
    # formula: [a(q-1)x^(q-1)+..+ a1x + a0] mod m, which  means the coefficients would be the x^2, x, and so on.
    for i in q:
        sub_mat = []
        
        for j in range(q_len-1, -1, -1):
            sub_mat.append(i[0] ** j)
        
        sub_mat.append(i[1])
        matrix_1.append(sub_mat)

    # Run a loop on matrix_1 to calculate via Gaussian Elimination process until we are left with 2 values which can calculate the secret a0.
    loop = True
    while loop == True:
        matrix_2 = []
        #print(matrix_1)
        for i in range(1, len(matrix_1)):
            sub_mat = []
            
            for j in range(len(matrix_1[0])):
                c = (matrix_1[0][j] * matrix_1[i][0]) - (matrix_1[i][j] * matrix_1[0][0])
                
                if c != 0:
                    sub_mat.append(c)
                else:
                    continue

            matrix_2.append(sub_mat)

        matrix_1 = matrix_2

        # Once we are down to the last 2 values, stop the loop.
        if len(matrix_1) < 2:
            loop = False
            #print(matrix_1)
        else:
            pass

    # Get the modular inverse of the coefficient of a0, then calculate the secret a0 via modular mathematics.
    mod_inv = pow(matrix_1[0][0], -1, mod_val)
    result = (matrix_1[0][1] * mod_inv) % mod_val

    return result

def euc(a, b):
    # This function calculates the GCD using recursion method.
    try:
        # Find the modulus of a and b.
        r = a % b
        
        # If remainder does not equal 0, call the euc() function again. If remainder equals 0, return b which is the GCD.
        if r != 0:
            result = euc(b, r)
        else:
            result = b

    except RecursionError:
        result = None

    return result

def main():
    # This is the main function.
    print("\nHello, I encrypt/decrypt your messages using RSA and Shamir Secret Sharing.")

    # Initialization.
    share_values = []

    # Getting 1024 bit prime numbers.
    P = getPrime(1024)
    Q = getPrime(1024)

    # Getting the modulus.
    N = P * Q

    # Encryption key and Decryption key.
    phi_N = (P - 1) * (Q - 1)
    E = 0x10001     # Standard encryption exponent 65537
    D = pow(E, -1, phi_N)

    start = True
    while start:
        time.sleep(1)
        usr_input = input(
'''
\nPlease choose from the options:\n
1. Generate secret shares
2. Decrypt secret
3. Exit\n
Please choose 1, 2, or 3:
'''
        )

        if usr_input == '1':
            # Inputfield to enter original message to encrypt.
            message = input("Enter the message you'd like to encrypt:\n")
            
            # Converting message to an integer.
            message = message.encode()
            message = bytes_to_long(message)

            check = message < N
            gcd = euc(message, N)

            if check and gcd == 1:
                secret = pow(message, E, N)

                try:
                    # Inputfield to enter number of shares and quorum.
                    shares = int(input("Enter the number of shares you want to generate (must be an integer): "))
                    quorum = int(input("Enter the quorum (must be an integer): "))

                    # Generating Shamir Secret shares.
                    share_values = generate_shares(secret, N, shares, quorum)
                    
                    # Printing in a reader-friendly format.
                    print("\nShare values are:")
                    time.sleep(1)
                    for shares in share_values:
                        print(shares)

                    time.sleep(1)
                    print("\nDecryption key:", D)

                except ValueError:
                    print("\nInvalid input. Restarting program...")

            else:
                print("\nInvalid message length. It may be too long.")
                print("Restarting program...")

        elif usr_input == '2':
            # Checking whether there is a message to decode.
            if not share_values:
                print("\nNo message to decrypt. Please encrypt message first.")
            else:
                decrypted_secret = reconstruct_secret(share_values[:quorum+1], N)
                
                decrypted_message = pow(decrypted_secret, D, N)
                decrypted_message = long_to_bytes(decrypted_message)
                time.sleep(1)

                print("The decrypted message is:", decrypted_message)

        elif usr_input == '3':
            print("\nExiting program...\n")
            start = False
        else:
            print("\nInvalid choice. Exiting program...\n")
            start = False
        
if __name__ == "__main__":
    main()