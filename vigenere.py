import secrets
import string


def main():
    # asks user for required function until valid response is given
    while True:
        function = input("Do you want to encrypt or decrypt? ").strip().lower()
        if function in ["encrypt", "decrypt"]:
            break
        print("Invalid function, please choose one of the following (encrypt/decrypt).")

    print(vigenere(function))


def vigenere(function):
    # ask if text will be provided in terminal or from file
    while True:
        choice = input("Read from (f)ile or (w)rite text here?(f/w) ").lower().strip()
        if choice not in ["f", "w"]:
            print(
                "Invalid, please write 'f' to read from file or 'w' to write text here."
            )
        else:
            break

    # get file from user
    if choice == "f":
        while True:
            try:
                filename = input("File name? ")
                inptr = open(filename, "r")
                break
            except FileNotFoundError:
                print(
                    """Couldn't find file. Make sure file is inside project folder, otherwise write the path to the file and make sure to write the file extension, ex: ###.txt"""
                )

        phrase = "".join(inptr.readlines())
        inptr.close()

    # get text from user
    elif choice == "w":
        phrase = input("Enter Text: ")

    # ask if user has key or wants an auto key
    while True:
        choice2 = (
            input(
                """If you are decrypting from a file created by this program choose 'r'. Otherwise feel free to choose.\n(P)rovide key or use (r)andom key/
                     (r)ead key from file?(p/r) """
            )
            .lower()
            .strip()
        )
        if choice2 not in ["p", "r"]:
            print(
                "Invalid, please write 'p' to provide key or 'r' to randomly generate a key / read key from a file."
            )

        elif choice2 == "r" and function == "decrypt" and choice == "w":
            print(
                "Cannot find key automatically to decrypt text written in terminal, please manually provide key."
            )

        else:
            break

    # using secret library to randomly generate a random length letter key
    if choice2 == "r":
        sysrandom = secrets.SystemRandom()
        length = sysrandom.randrange(1, 9)
        alphabet = string.ascii_letters
        key = "".join(secrets.choice(alphabet) for i in range(length))

    # getting key input from user and making sure it is valid
    elif choice2 == "p":
        while True:
            try:
                key = input("Key: ")
                for i in range(len(key)):
                    if (
                        ord(key[i]) < 32 or ord(key[i]) > 126
                    ):  # key can only contain chars within 32-126 in ascii code
                        raise ValueError
                break
            except ValueError:
                print("Invalid Key")

    # encrypting the input
    if function == "encrypt":
        encryption = encrypt(phrase, key)
        if choice == "f":
            outptr = open(
                "vig_" + filename, "w"
            )  # opens a new file to write encrypted text to
            keyptr = open(
                "key_vig_" + filename, "w"
            )  # opens a new file to write the key to
            keyptr.writelines(str(key) + "\n")
            outptr.writelines(encryption)
            outptr.close()
            keyptr.close()

        # output key if it is randomly generated
        if choice2 == "r":
            return encryption, key

        return encryption

    # decrypting the input
    elif function == "decrypt":
        # read key from file in case file is generated by program
        if choice2 == "r" and choice == "f":
            try:
                inptr = open("key_" + filename, "r")
                key = (
                    inptr.readline().strip()
                )  # clean up key and remove invalid characters
                for char in key:
                    if ord(char) not in range(32, 127):
                        key = key.replace(char, "")
            except FileNotFoundError:
                return "Cannot find file containing the key."
            inptr.close()

        decryption = decrypt(phrase, key)
        if choice == "f":
            outptr = open(
                "de_" + filename, "w"
            )  # open new file to write the decrypted text
            outptr.writelines(decryption)
            outptr.close()

        return decryption


# function to encrypt
def encrypt(plaintext, key):
    encrypted = ""
    counter = 0  # counter to help us repeat key until all text is encrypted
    for i in range(len(plaintext)):
        x = ord(plaintext[i])
        # make sure x is in values we can change before we change it
        if 126 >= x >= 32:
            x = ((x + ord(key[counter]) - 32) % 95) + 32
        encrypted += chr(x)
        counter += 1
        if counter == len(key):  # when counter reaches end of key, reset counter
            counter = 0

    return encrypted


# function to decrypt
def decrypt(ciphertext, key):
    decrypted = ""
    counter = 0  # counter to help us repeat key until all text is encrypted
    for i in range(len(ciphertext)):
        x = ord(ciphertext[i])
        # make sure x is in values we can change before we change it
        if 126 >= x >= 32:
            x = ((x - ord(key[counter]) - 32 + 95) % 95) + 32
        decrypted += chr(x)
        counter += 1
        if counter == len(key):  # when counter reaches end of key, reset counter
            counter = 0

    return decrypted


if __name__ == "__main__":
    main()
