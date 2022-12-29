import os
import argparse
import cryptography
import inflect
from cryptography.fernet import Fernet
from sys import argv, exit


def main():
    # Initialize parser and get args
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files")
    args = cl_handler(parser)

    # Call de/en function based on args
    if args["e"] is not None:
        print(encrypt(args["e"]))
    elif args["d"] is not None:
        print(decrypt(args["d"]))
    elif args["eAll"] is True:
        print(encrypt(get_files()))
    elif args["dAll"] is True:
        print(decrypt(get_files()))


# Handle command-line arguments
def cl_handler(parser: object):
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-eAll", help="Encrypt all files inside root directory", action="store_true"
    )
    group.add_argument(
        "-dAll", help="Decrypt all files inside root directory", action="store_true"
    )
    group.add_argument(
        "-e", type=str, help="One file encrypt", choices=get_files(), nargs=1
    )
    group.add_argument(
        "-d", type=str, help="One file decrypt", choices=get_files(), nargs=1
    )
    args = parser.parse_args()

    # Check for existing argv
    if len(argv) < 2:
        parser.print_help()
    return vars(args)


# Get all files inside root directory
def get_files():
    files = []
    for file in os.listdir():
        if (
            file == "project.py"
            or file == "test_project.py"
            or file == "key.key"
            or file == "requirements.txt"
            or file == "README.md"
        ):
            continue
        if os.path.isfile(file):
            files.append(file)
    return files


# Encrypt function
def encrypt(files: list):
    # Initialize inflect
    p = inflect.engine()

    # Encrypt files
    for file in files:
        with open(file, "rb") as reader:
            container = reader.read()
            with open(file, "wb") as writer:
                writer.write(Fernet(gen_key()).encrypt(container))
                print(f"--> {file} encrypted")

    # Format returning string
    if len(files) == 1:
        completed = f"file: {files[0]} is"
    elif len(files) == 0:
        return "No files to encrypt"
    else:
        completed = f"files: {p.join(files)} are"
    return f"\nThe following {completed} now encrypted!"


# Decrypt function
def decrypt(files: list):
    # Initialize inflect
    p = inflect.engine()

    # Open key file and split into multiple keys
    try:
        with open("key.key", "rb") as key:
            keys = key.readlines()
    except FileNotFoundError:
        exit("No encrypted files found!")

    # Trigger for no encrypted files and empty list for printing decrypted file names
    trigger = False
    decripted_files = []
    # Decrypt every file in given list
    for file in files:
        with open(file, "rb") as reader:
            container = reader.read()
            # Try every key for decryption
            for key in keys:
                try:
                    decrypted_line = Fernet(key).decrypt(container)
                    # Write back decrypted content
                    with open(file, "wb") as writer:
                        writer.write(decrypted_line)
                        # Trigger not encrypted
                        trigger = True
                        # Append to list of decrypted files
                        decripted_files.append(file)
                        # Remove used key
                        with open("key.key", "wb") as k:
                            keys.remove(key)
                            k.writelines(keys)
                            # Print decrypted file
                            print(f"--> {file} decrypted")
                except (cryptography.fernet.InvalidToken, ValueError):
                    pass

    # Format returning string
    if len(decripted_files) == 1:
        completed = f"file: {decripted_files[0]} is"
    else:
        completed = f"files: {p.join(decripted_files)} are"
    reader.close()
    # No files to be decrypted
    if trigger == False:
        return f"File(s) not encrypted!"
    # Return completed string
    return f"\nThe following {completed} now decrypted!"


def gen_key():
    key = Fernet.generate_key() + bytes("\n", "utf-8")
    # Append key to file
    with open("key.key", "ab") as k:
        k.write(key)
    return key


if __name__ == "__main__":
    main()
