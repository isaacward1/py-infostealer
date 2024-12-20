# PyGlutton
A guide on the build process, obfuscation techniques, and analysis of simple python-based infostealer malware.<p>
<b>** Disclaimer ** This tutorial is intended for educational purposes only. I do not condone the malicious use of this material.</b>


<br>

## Prerequisites
- Windows 10
- Python 3.1X
> pip install -U -R requirements.txt

<br>

## Building Malware

### Code Obfuscation w/ [Pyarmor](https://pypi.org/project/pyarmor/)
To apply basic code obfuscation:
> pyarmor gen example.py

<br>

### Using [Pyinstaller](https://pyinstaller.org/en/stable/usage.html)
Initial building:
> cd dist
> pyinstaller example.py
<br>
Editing .spec file

[finish later]


<br>

### Other Obfuscation Techniques
[finish later]

<br>

### Ideas
[finish later]

<br>

## Malware Analysis

[PyInstaller Extractor](https://github.com/extremecoders-re/pyinstxtractor) - A Python script to extract the contents of a PyInstaller generated Windows 
executable file. The contents of the pyz file (usually pyc files) present inside the 
executable are also extracted and automatically fixed so that a Python bytecode decompiler will recognize it.

[uncompyle6](https://github.com/rocky/python-uncompyle6/) - A cross-version Python bytecode decompiler. Translates Python bytecode back into equivalent Python source code.
