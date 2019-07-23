# 								Email Automation Module

##### 																																		Written by: Jason Ho

##### 																																				Date: 07/22/2019

--------

## Project Overview

This module was specifically created since so much time was always spent on writing similar code that just sends emails. This email script is able to be used with command line arguments, as a module that can be called inside of scripts, and also as a REPL where the user just inputs the information directly into the console.



**Note**: Before the script can be used, a mail relay server needs to be provided on line 148 of the emailing.py file. Since I do not want to share out the relay server that I use, one will have to input their own before they can use the emailing part of this script. Alternatively, it is possible to modify the script to accommodate regular service accounts from g-mail quite easily, but as of right now, it only accepts mail relay.

```python
with smtplib.SMTP('name of relay server here', 'port number here') as server:
```



### Project Files

- **emailing.py** : This file contains the Email_Distributor object that does most of the work in that it   connects to the mail relay server, stores the relevant fields and is able to be used as a module from just connecting with the this email file. It also contains the main function that is able to run command line arguments.  It just connects to the Email_Distributor object, but is able to take in all arguments in the console to automatically send emails. In addition, it has a manual mode for people that are less adept at using command line arguments where it just prompts for each of the required fields: from address, to address, subject of the email, body of the email, and an optional file path argument for files that want to be sent.
  
  - Note: The module part of the emailing script is able to send both emails with and without files, but they are parts of different functions. The module_call() function handles emails without files while the module_call_file() handles emails with files.
  
- **examples.py** : This file is primarily used to demonstrate examples of how to use the module calls of the Email_Distributor object. 

- **README.md** : This is the file that contains all of the information that includes all of the documentation to make sure that everything works correctly.

  

### How to Use

##### Command Line Flags:

- There are 5 different command line flags that one can input in order to change to send an email.
  - **'-f'** or **'--fromemail'** which is used to define who the email is coming from. This can be any address.
  - **'-t'** or **'--toemail'** which is used to define who the email will be sent to. In order to send to multiple people, use the same flag multiple times
    - For example: '-e email@email.com -e otheremail@email.com'
  - **'-s'** or **'--subject'** which is used to define what the subject of the email will be. In order words, this is what is displayed without opening the email.
  - **'-b'** or **'--body'** which is used to define the body of the email address. This field is not needed since the program will check beforehand whether or not a body exists and will automatically fill one in if it does not exist.
    - Note: The user will be able to change whatever they want the message to 
  - **'-p'** or **'-filepath'** which is used to define where the file that a user wants to send is located. At this moment, it is only possible to send one attachment per email but that could be fixed later on pretty easily. 
    - Note: The entire filepath must be passed into the flag.
- Note: The command lines are made using argparse so it is possible to pass the **'-h'** or **'--help'** flag in order to get more help on how to use the program with command line flags.

##### Manual Input into Console:

- In order to reach the manual input into the console, a user will have to input the flag: **'-m'** or **'--manual'** which means that it will open up a kind of REPL that will ask for each type of input from the command prompt rather than passing everything as command line arguments. 
- The user will then just go through and input whatever they want. The email will be displayed to the user though before being sent out to make sure that everything that they have inputted is correct. If it is not correct, then they can leave the console and then run again to correct that information.

##### Module Calls:

- In order to use module calls, one will first instantiate an Email_Distributor() object. Then, they will use either the object's **module_call** function or the **module_call_file** function.
  - **module_call** takes in four variables in this order: from address, to address, subject, body of email
  - **module_call_file** takes in five variables in this order: from address, to address, subject, body of email and then the filepath all as a string.
    - Note that the filepath either has to have escape characters for the backslashes, or converted to a raw string.
      - In order to escape backslashes, put a forward slash in front of it
      - In order to convert a string to a raw string put an r in front of the string.
        - Ex: **'filepath'** converted to a raw string is just **r'filepath'** with the r in the front.
    - Otherwise, the filepath will produce a Unicode Syntax Error because the code will interpret it incorrectly and cause a problem.
- To verify that information is correct, after using these functions, the user will have to use the **send_email()** function themselves in order to make sure that their email is correct. 
  - The str(Email_Distributor Object) is modified for easy viewing for the user so that they can verify information before sending information out.
- Examples of how to use the module calls can be found in **examples.py**



### Future Implementations

In the future, I plan on updating the code to accommodate specific needs such that the email module can do more. Some future ideas are posted below:

- Rewrite the file_path to be a list such that it would be possible for a user to input multiple files instead of having to send an email per file.
- Writing a GUI for the manual console call so that the user does not have to use the command prompt. 
  - Or, just rewriting the command prompt REPL so that it is easier to read and has checks to make sure that variables are correct.



