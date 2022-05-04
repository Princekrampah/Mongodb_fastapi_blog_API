import os
from fastapi import BackgroundTasks

# pip install fastapi-mail python-dotenv python-multipart
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

# do not specify the '.env'
load_dotenv()
 

class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="api/templates"
)


# https://sabuhish.github.io/fastapi-mail/example/#using-jinja2-html-templates
async def send_registration_mail(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html',
    )
    
    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


async def password_reset(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html',
    )
    
    fm = FastMail(conf)
    await fm.send_message(message, template_name='password_reset.html')


