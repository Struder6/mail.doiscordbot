import discord
import imaplib
import email
import os
import time
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Берём данные дл наших авторизаций

TOKEN = 'urtoken' # Insert your discord app token
EMAIL = os.getenv('youremailongmail@gmail.com') # Insert your gmail here
PASSWORD = os.getenv('Your PaSsWoRd') # Insrt your password here
IMAP_SERVER = os.getenv('imap.gamil.com')  # imap server there is. touch it should you not
CHANNEL_ID = str(os.getenv(''))  # Target channel ID

Client = discord.Client(intents = discord.Intents.default() )

async def send_email_to_discord(subject, body):
    channel = Client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"**Subject:** {subject}n**Body:** {body}")

def check_email():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    while True:
        result, data = mail.search(None, 'UNSEEN')  # Ищем непрочитанные письма
        if result == 'OK':
            for num in data[0].split():
                result, msg_data = mail.fetch(num, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                
                subject = msg['subject']
                body = ""
                
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True).decode()
                else:
                    body = msg.get_payload(decode=True).decode()

                # Отправляем письмо в Discord
                asyncio.run(send_email_to_discord(subject, body))
                
                # Помечаем письмо как прочитанное
                mail.store(num, '+FLAGS', '\Seen')

        time.sleep(60)  # Проверяем почту каждую минуту

@Client.event
async def on_ready():
    print(f'Logged in as {Client.user}')
    check_email()

Client.run(TOKEN)
