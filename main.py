import pandas as pd
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from pandas._libs.tslibs import Timestamp

from packages.mail import send
from packages.scrollbar import fill_list_scrollbar

class Window():
    def __init__(self):
        self.root = Tk()
        self.root.geometry('800x400')
        self.root.title('Scripts de automação')
        self.root.resizable(0, 0)

        Label(self.root, text='Envio de adiantamentos vencidos').place(x=16, y=16)
        Button(self.root, text='Enviar e-mails', command=self.send_emails, bg='green', fg='white', highlightbackground='green').place(x=16, y=42)
        Button(self.root, text='Sair', command=self.root.destroy, bg='red', fg='white', highlightbackground='red').place(x=730, y=350)

        self.root.mainloop()

    def send_emails(self):
        is_send_emails_accepted = messagebox.askquestion(
            title='Envio de adiantamentos vencidos', 
            message='Iniciar o envio?'
        )

        if is_send_emails_accepted == 'yes':
            messages_sent = self.data_science()

            fill_list_scrollbar(messages_sent)

            messagebox.showinfo(
                title='Envio de adiantamentos vencidos', 
                message='Os e-mails foram enviados com êxito! Pressione Ok para fechar'
            )

    def data_science(self):
        actual_datetime = datetime.today()
        advances_spreadsheet = pd.read_excel('adiantamentos_pendentes.xlsx')
        advances_spreadsheet_filtered = advances_spreadsheet[['NOME', 'TÍTULO', 'E-MAIL', 'EMISSÃO', 'VALOR SALDO', 'DATA FINAL']]
        advances_spreadsheet_filtered.rename(columns={
            'NOME': 'provider',
            'TÍTULO': 'title',
            'E-MAIL': 'email', 
            'EMISSÃO': 'dt_expedition', 
            'VALOR SALDO': 'balance',
            'DATA FINAL': 'dt_final'
        }, inplace = True)

        all_messages_sent = []

        for i in advances_spreadsheet_filtered.index:
            dt_final = advances_spreadsheet_filtered.loc[i, 'dt_final']
            email = advances_spreadsheet_filtered.loc[i, 'email']

            if type(dt_final) == Timestamp and type(email) == str:
                if dt_final < actual_datetime:
                    provider = advances_spreadsheet_filtered.loc[i, 'provider']
                    title = advances_spreadsheet_filtered.loc[i, 'title']
                    balance = float(advances_spreadsheet_filtered.loc[i, 'balance'])
                    dt_expedition = datetime.strftime(advances_spreadsheet_filtered.loc[i, 'dt_expedition'], "%d/%m/%Y")

                    message_sent = send(provider, title, email, balance, dt_expedition)
                    all_messages_sent.append(message_sent)
        
        return all_messages_sent

app = Window()
