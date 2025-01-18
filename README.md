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

### SSH exfiltration using [Paramiko](https://www.paramiko.org/installing.html)
The example script shown only uses SSH via the paramiko library to exfiltrate stolen data (for now at least). Below is a snippet of its usage:


<br>

### Other Methods ([PyExfil](https://github.com/ytisf/PyExfil))
...

<br>

## Code Obfuscation Techniques
### Using [Pyarmor](https://pypi.org/project/pyarmor/)
To apply basic code obfuscation:
> pyarmor gen example.py

<br>

## Using [Pyinstaller](https://pyinstaller.org/en/stable/usage.html)
### Initial building:
> cd dist
> pyinstaller example.py

<br>

### Editing the .spec file
...


<br>

## Malware Analysis

**[PyInstaller Extractor](https://github.com/extremecoders-re/pyinstxtractor)** - A Python script to extract the contents of a PyInstaller generated Windows executable file. The contents of the pyz file (usually pyc files) present inside the executable are also extracted and automatically fixed so that a Python bytecode decompiler will recognize it.

**[uncompyle6](https://github.com/rocky/python-uncompyle6/)** - A cross-version Python bytecode decompiler. Translates Python bytecode back into equivalent Python source code.

<br>

## To-do List
- Metasploit download+exec module
- .py to .pdf
- smtp exfiltration
- ssh key integration
- encrypted ssh password from http server
- ssh over tor socket
