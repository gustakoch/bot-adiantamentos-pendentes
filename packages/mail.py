import smtplib
import locale
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from packages.utils import greeting

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def send(provider, title, email, balance, dt_expedition):
    balance_formated = locale.currency(balance, grouping=True)

    server = smtplib.SMTP(
        os.environ.get('EMAIL_SMTP_HOST'),
        int(os.environ.get('EMAIL_SMTP_PORT'))
    )
    server.ehlo()
    server.starttls()
    server.login(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASSWORD'))

    message_html = f'''
        <html>
            <head></head>
            <body>
                <p>{greeting()},<br><br>
                O adiantamento solicitado ao fornecedor {provider}, data {dt_expedition}, no valor de {balance_formated} está com prazo vencido.<br>
                Favor informar nova previsão para lançamento da nota fiscal.<br><br>
                Att,<br>
                Djefeline Rambo<br>
                Contas a pagar
                </p>
            </body>
        </html>
    '''
    email_msg = MIMEMultipart()
    email_msg['From'] = user
    email_msg['To'] = email
    email_msg['Subject'] = 'Adiantamento pendente'
    email_msg.attach(MIMEText(message_html, 'html'))

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    server.quit()

    return f'Email do fornecedor {provider}, título {title}, enviado para {email}'
