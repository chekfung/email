# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:46:30 2019

@author: jho18 (Jason Ho)
"""

# Imports
import sys
import re
import argparse
import textwrap

# Imports for email infrastructure
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import COMMASPACE

class Email_Distributor():
    '''
    Email_Distributor is the object that is responsible for all of the emails
    that will be sent from the collector script. It contains all of the info
    needed in order to check whether or not the downed or recovered collectors
    have already had emails sent out. It is also able to get rid of the fixed
    collectors such that if the collectors go down again, the correct email
    will be sent out.
    
    Most of the methods are private because there should not be any calls to
    them other than through the public method: run. Essentially, to utilize
    this object, just create the object with the necessary variables and then
    call run and everything else should be done.
    '''
    # Default body message
    default_body = 'This is an automated message using email scripts'
    
    def __init__(self):
        self.sub = None
        self.to_add = None
        self.from_add = None
        self.file_path = 'No file path added.'
        self.file_name = None
        self.body = None
        
    def __str__(self):
        st = ('----------------------- Email Overview -------------------------\n'
        + 'From Address: ' + self.from_add + '\n'
        + 'To Address: ' + str(self.to_add) + '\n'
        + 'Subject: ' + self.sub + '\n'
        + 'Body: ' + self.body + '\n'
        + 'file_path: ' + self.file_path)
        return st
    
    def module_call_file(self, from_add, to_add, s, b, fp): 
        '''
        Method that allows for module call so that can be used in scripts
        
        Note: The entire file path is required for the script to work correctly
        In addition, in order to override a unicode error, put a r in front
        of the filepath so that it is converted to a raw string
        
        Parameters
        ----------
        from_add : str
            Represents the sender email in the email in the object
            
        to_add : str
            Represents the address(s) to send the email to in the object
        
        s : str
            Represents the subject of the email
            
        b : str
            Represents the body of the email
        
        fp : str
            Represents the file path that will be attached to the email
        '''
        self.sub = s
        self.to_add = to_add
        self.from_add = from_add
        self.file_path = fp
        self.body = b
        
    def module_call(self, from_add, to_add, s, b):
        '''
        Method that allows for module call so that can be used in scripts
        
        Note: The entire file path is required for the script to work correctly
        In addition, in order to override a unicode error, put a r in front
        of the filepath so that it is converted to a raw string
        
        Parameters
        ----------
        from_add : str
            Represents the sender email in the email in the object
            
        to_add : str
            Represents the address(s) to send the email to in the object
        
        s : str
            Represents the subject of the email
            
        b : str
            Represents the body of the email
        '''
        self.sub = s
        self.to_add = to_add
        self.from_add = from_add
        self.body = b

    def is_body_empty(self):
        '''
        is_body_empty is a method that checks whether or not there is a
        body in the email and if there is not, it automatically inputs a
        body stating that this script is an automated message.
        
        A user can change this field to whatever they want to.
        
        Returns
        ---------
        body empty? : bool
            Represents whether or not the body was found to be empty or not
        '''
        if self.body == None:
            self.body = self.default_body
            return True
        else:
            return False
    
    def send_mail(self):
        '''
        send_mail is a method that actually sends out the emails using the
        brown relay server to send the contents of everything that is done by
        the other methods. 
        
        Parameters
        ----------
        state : string
            Represents if collectors in email are down or recovered
            
        os : string
            Represents if the collectors are windows or linux based
            
        lst : list of dictionaries
            Represents the list of downed or recovered collectors that will
            be passed into the other methods later on.
            
        email : list
            Represents the receiver emails that will be sent out depending on
            the team that the collector comes from.
        '''
        # Login to SMTP server and send email
        with smtplib.SMTP('mail relay server name', 'port') as server:

            # Setting up initial MIME Email object
            message = MIMEMultipart('alternative')
            message['Subject'] = self.sub
            message['From'] = self.from_add
            message['To'] = self.to_add

            # MIME Object
            body = MIMEText(self.body, "plain")
            message.attach(body)
            
            # Check if file exists
            if (self.file_path != 'No file path added.'):
                try:
                    p = MIMEBase('application', 'octet-stream')
                    attach = open(self.file_path, "rb")
                    p.set_payload((attach).read())
                    
                    # Find the filename so can name file
                    match = re.search('[ \w-]+?(?=\.)', self.file_path)
                    filename = match.group(0)
                    
                    # Encode and attach to the message
                    encoders.encode_base64(p)
                    p.add_header('Content-Disposition', 'attachment', 
                                 filename= str(filename))
                    message.attach(p)
                    
                except (FileNotFoundError):
                    print('The file that was inputted was not found.')
                except (AssertionError):
                    print('Fatal assertion error found. Exiting')
                    sys.exit(1)
                    
            # Sending Actual Mail
            server.sendmail(self.from_add, self.to_add , message.as_string())
            print('Email has been sent!')
            
def main():
   '''
   main provides the argparse part of the the entire collector script which is
   quite nice to have as it explains everything, how to operate the script,
   etc. 
   
   It uses flags in order to indicate what should be done. This is especially
   useful when the script is called outside of a python IDE, which allows for 
   everything to function from the command line.
   '''
   # What is displayed when help is called
   parser = argparse.ArgumentParser( 
       epilog = 'Written by Jason Ho; jason_ho@brown.edu',
       formatter_class = argparse.RawDescriptionHelpFormatter,
       description = textwrap.dedent('''\
                                     Email Sender
            --------------------------------------------------------------
            This script can be used as both a command line argument script
            or used as an individual module that is needed for different
            scripts. Since it is used so much, it was a good idea to 
            just port this into a script of its own.
            
            The email object either is instantialized and called with its
            methods to send emails while editing the contents of the 
            email using other methods in the class.
            
            The email object can also be called as a command line 
            argument using the correct flags to automatically input what
            the user wants to do.
            
            Note: Everything can be done as command line arguments, manually
            in the console using the --manual flag (-m) or just by doing a
            module call.
            '''))
           
   parser.add_argument('-p', '--filepath', type = str,
                   help= 'Attachment filepath for email. Full filepath needed.')
   parser.add_argument('-f', '--fromemail', type = str, 
                   help= 'Attachment filename for email. Full filepath needed.')
   parser.add_argument('-t', '--toemail', action = 'append', 
                   help= 'Add as many emails to notify. Each email added'
                   + 'from command line must be preceded by -e')
   parser.add_argument('-s', '--subject', type = str, 
                   help= 'Subject of the email to be sent out')
   parser.add_argument('-b', '--body', type = str,
                   help= 'Body of the message that will be sent in email.')
   parser.add_argument('-m', '--manual', action= 'store_true',
                   help= 'Takes input rather than using command line arguments')

   # parses out the arguments from the command line call
   args = parser.parse_args()
   e = Email_Distributor()
   
   if args.manual != True:
       # Checking if file path exists
       if args.filepath != None:  
           e.file_path = args.filepath
    
       # Checking if from email exists
       if args.fromemail != None:
           e.from_add = args.fromemail
       else:
           print('Missing a from email. This is required to work correctly.')
           print('\n Here is how to use the program correctly.')
           parser.print_help()
           
       # Checking if to email exists
       if args.toemail != None:
           e.to_add = COMMASPACE.join(args.toemail)
           print(type(e.to_add))
       else:
           print('Missing a to email. This is required to work correctly.')
           print('\n Here is how to use the program correctly.')
           parser.print_help()
           
       # Checking if subject exists
       if args.subject != None:
           e.sub = args.subject
       else:
           print('Missing a subject. This is required to work correctly.')
           print('Here is how to use the program correctly.\n')
           parser.print_help()
           
       # Checking if body exists
       if args.body != None:
           e.body = args.body
       else:
           e.is_body_empty()
           print('Since no body was added, one was automatically generated.')
       
       if (e.to_add != None and e.from_add != None and e.sub != None):
           print(str(e))
           e.send_mail()
         
   # If lazy flag was passed
   else:
       print('\nYou have entered the manual input mode for the email sender.')
       print('The script will prompt for the following information: from address'
             + ', to address, subject, body, and optional filepath.')
       # Asking for inputs for from email, to email, subject, body and optional
       # filepath
       e.from_add = input('Please input a from address: ')
       
       # To Address
       to_email = []
       loop_variable = True
       
       while loop_variable:
           em = input('Please input a to address: ')
           to_email.append(em)
           
           # Check if want to add another email
           add = input('Add another email address to send to? (yes/no): ')
           
           if add == 'no':
               loop_variable = False
       e.to_add = COMMASPACE.join(to_email)   
       
       # Subject
       e.sub = input('Please input the subject for email: ')
       
       # Body
       e.body = input('Please input the body for the email: ')
       
       # Filepath
       i = input('Add a file path to send? (yes/no): ')
       
       if i == 'yes':
           e.file_path = input('Input full file path here: ')
       
       print(str(e))
       c = input('Is this information correct? (yes/no): ')
       print('\n')
       
       if c != 'yes':
           sys.exit(0)
       else:
           e.send_mail()
       
# ========================================================================== #
    
# Used specifically if the user wants to run in command line
if __name__ == '__main__':
    main()     


