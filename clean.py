'''
This program helps backing up data to dropbox easier and automated. It first uploads your files to dropbox and then 
deletes them from the local storage. It uses input for the path to 'delete files from' and the dropbox path to upload the 
file to. It also sends an email from the specified email address to your specified email address as a confirmation 
using a secure ssl server . The program also creates and appends to a log file, which stores the time of the instances 
the backups were done.

PLEASE ENTER THE REQUIRED FIELDS WHERE THERE IS A COMMENT TO ENTER THEM
'''
# import the modules required
import os
import dropbox
import smtplib
import ssl
from time import time, ctime

#constructing a clean function that will delete all the files from the directory specified
def clean(path):
    if os.path.exists(path):
        files = os.listdir(path)
        for i in files:
            i = os.path.join(path, i)
            os.remove(i)
    else:
        print("are u sure this directory exists -_-")

#constructing a upload_files function that will upload files to the destination parameter from the source parameter
def upload_files(source, destination):

    db = dropbox.Dropbox(
        'dropbox_authenticaton_code')         #please type in your dropbox authentication code here
    # checking if the directory inputed exists
    if os.path.exists(source):
        for root, dirs, files in os.walk(source):

            for filename in files:
                # constructing a local path of the file using the local directory and the file's name
                local_path = os.path.join(root, filename)
                # constructing a relative path using the local_path variable and the local directory
                rel_path = os.path.relpath(local_path, source)
                # constructing the dropbox path using the destination specified and the rel_path
                db_path = os.path.join(destination, rel_path)

                # upload the file
                with open(local_path, 'rb') as f:
                    db.files_upload(f.read(), db_path,
                                    mode=dropbox.files.WriteMode.overwrite)
    else:
        print("are you sure the folder's path  exists? -_-")
        print("------------------------------------------------")

#constructing an email function to send the user a confirmation email about the backup from the specified email
def email():
    port = 465
    password = "password"                                        #please type in the password of the email address you want to send an email from
    sender_email = "sender_gmail"                         #please type in the email address you want to send an email from

    context = ssl.create_default_context()
    receiver_email = "receiver_gmail"                      #please type in the email address on which you want to receive an email
    message = "the files have been backed up "

# staring a smt-ssl server
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server: 
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

#constructing a log function to save the data which stores the time of the instances the backups were done.
def log():
    f = open("log.txt", 'a+')
    current_DateTime = time()
    f.write("Backup done at: "+ctime(current_DateTime) +
            "\n ------------------------------------"+"\n")
    f.close()        
#constructing a log_display function to display the log in the cli
def log_display():
    f = open("log.txt","r+")            
    f_read = f.read()
    print(f_read)

# constructing a main function that will run if the user wants to backup
# it will run if the user presses l
def main():
    path = input("enter the path of the folder you want to clean: ")
    print("------------------------------------------------")
    d = input(
        'enter the folder you want to store the files (for example /Music) in: ')
    print("------------------------------------------------")
    upload_files(path, d)
    print('all the files have been uploaded ;)')
    print("---------------------------------")
    clean(path)
    print("the folder is cleaned :)")
    email()
    print("the backup is complete :)")
    log()


# using an if condition to display log or backup the data
m= str(input("to backup press b and enter\n------------------------------------------------\nto display the log press l and enter: "))
if(m=="b"):
    main()
elif(m=="l"):    
    log_display()
else:
    print("wrong input -_- ")    