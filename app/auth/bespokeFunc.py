from email.message import EmailMessage 
import smtplib as sml,ssl, os
import random
import string

def sendEmail(rec, code):
    sender ='e.datapreneur@gmail.com'
    subject ="This is a test"
    content = f""" 
                    Congratulations! We've successfully created account.
                    Go to the page: <a href="url_for('auth.confirm_email')">{code}</a>
                    Thanks,
                    
                """

    password = os.environ['e_data_password']
    em = EmailMessage()
    em["From"] = sender
    em["To"] = rec
    em["Subject"] = subject
    em.set_content(content, 'html')
    context = ssl.create_default_context()

    with sml.SMTP_SSL('smtp.gmail.com',465, context = context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, rec, em.as_string())
        

    return "Sent"

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    
    
    return result_str


