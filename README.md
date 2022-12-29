# Easy Encrypt
## Video Demo: https://youtu.be/0ABpV1-8wFA
## Description:
        A simple to use python script for file encryption or decryption based on Cryptography Fernet library.It takes command-line arguments and is easy to use.
    If project.py is run without any arguments a help message is display into the terminal.
    
    Command-line arguments:
        I used argparse library for great functionality.All arguments are handled by cl_handler() function.
        -h, --help   Displays the same help message as simply running the script without arguments.
        -e           The argument followed by a file name in the same directory will encrypt the given file.
        -d           The argument followed by an encrypted file name will decrypt it.If file is not encrypted a message will be prompted "File(s) not encrypted!".
        -eAll        Encrypt all files in the directory.
        -dAll        Decrypts all files in directory.If files are not encrypted a message will be prompted "File(s) not encrypted".

    Encrypt:
        While reading the file(s) the encrypt function provided by Fernet is called on given file(s) and the encrypted content is written back to same file.For it to
        work on any type of file binary read/write is used.A message will be prompted into the terminal after each encrypted file and also a message which contains
        all encrypted files names will be displayed at the end.
        When using "-e" argument a single file will be encrypted and the key is stored inside "key.key" file.
        When using "-eAll" argument the script will encrypt all the files in root directory and all the keys are stored inside "key.key" file.
        A file can be encrypted multiple times, each time a new key is generated and stored inside "key.key" file.
        If invalid file name is given, a message is printed into the terminal which will display all posible choices for a file name.
        If there are no files inside root directory a message is printed.

    Decrypt:
        First the "key.key" file is read and all keys are stored inside a variable.While reading the file(s) a loop is used to try and decrypt the contents using every key
        stored earlier.On succes the decrypted contents are written back to same file and a message will be prompted into the terminal stating the file name and success
        decryption.At the end a message is prompted which contains all decrypted files names.Decrypt uses binary read and write.If the given file is not encrypted
        (no given key works) a message is prompted.
        When using "-d" argument a single file will be decrypted.
        When using "-dAll" argument all files inside root directory will be decrypted.
        After each succesfull decryption the key that was used is removed from "key.key" file.
        If invalid file name is given, a message is printed into the terminal which will display all posible choices for a file name.


    Key generator:
        It returns a key generated using Fernet function.It also writes the key inside "key.key".
    
    Get files:
        It returns only the files inside root directory.

### Tests:
    One of the first things "test_project.py" will do is run the decryption function untill there are no encrypted files inside directory.
        Test for "get_files()": 
            It will compare the files returned from the function to files given by a list generated by "os.listdir()" combined with "os.isfile()" 
        Test for single file encryption/decryption: 
            It will first run "encrypt()" on a file inside root directory and imediately after will run "decrypt()".Will compare                                    
            Will compare the printed messages.
            If there are no files inside root directory this test will not run.
        Test for multiple files encryption/decryption: 
            It will run "encrypt()" on all files inside root directory and imediately after will run "decrypt()" also on all files
            Will compare the printed messaages.
            If there are no files inside root directory this test will not run.
        Test for encryption errors:
            Will check for FileNotFoundError by providing invalid file name as argument.        
        Test for file(s) not encrypted:
            Will compare the printed messages.
            If there are no files inside root directory this test will not run.
        Test key:
            Will generate a new key and compare it to last key written inside "key.key"
            Will remove the generated key from file.

### Limitations:
    The more keys that are stored inside "key.key" the slower the script gets.Made sure to remove every key after each decryption for optimization purposes.
    Also the encryption or decryption takes more times with larger files, tested on 3.5 GB file and it takes about 1:50 minutes on decryption which is slower.
    Wanted to make it run faster but there seems to be no way to do that in python.

