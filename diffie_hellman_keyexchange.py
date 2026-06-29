def diffie_hellman():
    p = int(input("Enter prime number p: "))
    g = int(input("Enter primitive root g: "))

    a = int(input("User A, enter your private key (a number): "))
    b = int(input("User B, enter your private key (a number): "))

    pub_a = pow(g, a, p)
    pub_b = pow(g, b, p)

    print(f"\nUser A Public Key: {pub_a}")
    print(f"User B Public Key: {pub_b}")

    secret_a = pow(pub_b, a, p)
    secret_b = pow(pub_a, b, p)

    print(f"\nShared Secret computed by A: {secret_a}")
    print(f"Shared Secret computed by B: {secret_b}")

    if secret_a == secret_b:
        print("\nSuccess! Both secrets match.")
    else:
        print("\nError: Secrets do not match.")

if __name__ == "__main__":
    diffie_hellman()
