# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:37:49 2019

@author: jho18 (Jason Ho)
"""

from emailing import Email_Distributor

# Example of a typical module call that could be used
# This was to make sure that module calls are possible.
e = Email_Distributor()
e.module_call('generic_email@gmail.com','my_email@gmail.com','sub','body')
print(str(e))
e.send_mail()

# Example of a typical module call that also sends a file
# Make sure that module calls are possible with files
f = Email_Distributor()
f.module_call_file('generic_email@gmail.com','my_email@gmail.com','sub','body',r'filepath')
print(str(f))
f.send_mail()


