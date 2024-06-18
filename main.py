##Written by Caleb Schwalb to detect if Maya went down##
## if down, send email, else detect##
## June 14 2022

##edited by caleb schwalb 9/25/2023
import psutil
import time
import smtplib


def checkIfProcessRunning(processName):
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True # we found it
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def parseGet(sFilename):
    file = open(sFilename, "r")
    toreturn = file.readline()
    file.close()
    return toreturn

def mail():
    body = 'Subject:  Maya is down!'
    try:
        smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
    except Exception as e:
        print(e)
        smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
    smtpObj.ehlo()
    smtpObj.starttls()
    usn = parseGet("username.txt")
    pw = parseGet("password.txt")
    smtpObj.login(usn, pw)
    smtpObj.sendmail('maya_is_down@outlook.com', 'calebschwalb@gmail.com', body)


if __name__ == '__main__':
    while(True):
         if checkIfProcessRunning("maya"):##maya is the process name for maya.exe
             print("[+]Maya is running!  Do nothing!")
             time.sleep(60)
         else:
            print("[+]No Maya")
            mail()
            print("[+]Email Sent!")
            break## one minutes interval to not be too heavy on cpu
