import smtplib
import tempfile
import subprocess
from elevate import elevate
from winotify import Notification

elevate(show_console=False)

def send_mail(mail):
    email_server = smtplib.SMTP("smtp.gmail.com",587)
    email_server.starttls()
    email_server.login("from_addr","password")
    email_server.sendmail("from_addr", "to_addrs", mail)
    email_server.quit()

def get_eventlog():
    tmp = tempfile.TemporaryFile()

    subprocess.run(["powershell", "Get-EventLog -LogName Security -InstanceID 4624"], stdout=tmp, stderr=subprocess.DEVNULL)
    tmp_size = tmp.tell()
    if tmp.tell() != 0:
        tmp.seek(0)
        send_mail(tmp.read())
        subprocess.run(["powershell", "Clear-EventLog -LogName Security"])
        notification = Notification(
            app_id="Login Control App",
            title="Login!",
            msg="An account was successfully logged on...",
            icon=r"C:\relative\path\icons\login.ico")
        notification.show()

    subprocess.run(["powershell", "Get-EventLog -LogName Security -InstanceID 4625"], stdout=tmp, stderr=subprocess.DEVNULL)
    if tmp.tell() != tmp_size:
        tmp.seek(0)
        send_mail(tmp.read())
        subprocess.run(["powershell", "Clear-EventLog -LogName Security"])
        notification = Notification(
            app_id="Login Control App",
            title="Warning!",
            msg="An account failed to log on...",
            icon=r"C:\relative\path\icons\failed.ico")
        notification.show()

if __name__ == '__main__':
    try:
        while True:
            get_eventlog()
            
    except KeyboardInterrupt:
        exit()