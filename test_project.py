from project import get_files, encrypt, decrypt, gen_key
import pytest
import os
import inflect

# Get inflect and list of files in the same directory
p = inflect.engine()
test_list = [
    file
    for file in os.listdir()
    if os.path.isfile(file)
    and file != "key.key"
    and file != "project.py"
    and file != "test_project.py"
    and file != "requirements.txt"
    and file != "README.md"
]

# Get file if only 1 item
if len(test_list) > 0:
    item = [test_list[0]]

# Decrypt everything before tests
if len(test_list) > 0:
    while decrypt(test_list) != "File(s) not encrypted!":
        decrypt(test_list)


# Test get_files function
def test_files():
    assert get_files() == test_list
    assert len(get_files()) != len(os.listdir())


# Test single file encrypt/decrypt
def test_singleFile():
    if len(test_list) > 0:
        assert encrypt(item) == f"\nThe following file: {item[0]} is now encrypted!"
        assert decrypt(item) == f"\nThe following file: {item[0]} is now decrypted!"


# Test encrypt error
def test_encrypt_errors():
    with pytest.raises(FileNotFoundError):
        encrypt("xxxzzzzyyyy")
    with pytest.raises(FileNotFoundError):
        encrypt("zzzzzxxxxyyyy")


# Test multiple files encrypt/decrypt
def test_multipleFile():
    if len(test_list) > 1:
        assert (
            encrypt(test_list)
            == f"\nThe following files: {p.join(test_list)} are now encrypted!"
        )
        assert (
            decrypt(test_list)
            == f"\nThe following files: {p.join(test_list)} are now decrypted!"
        )


# Test file(s) not encrypted
def test_notEncrypted():
    if len(test_list) > 0:
        assert decrypt(item) == f"File(s) not encrypted!"
        assert decrypt(test_list) == f"File(s) not encrypted!"


# Test key generator
def test_key():
    key = gen_key()
    # Get all keys
    with open("key.key", "rb") as k:
        keys = k.readlines()
    # Try assertion on key == last key that was written
    assert key == keys[-1]
    # Remove generated key and write back all keys
    with open("key.key", "wb") as k:
        keys.remove(keys[-1])
        k.writelines(keys)
