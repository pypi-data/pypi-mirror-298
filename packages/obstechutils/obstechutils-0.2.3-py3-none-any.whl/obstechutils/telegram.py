from __future__ import annotations

import requests
from .db import DataBase
from .credentials import Credentials
from typing import Union,Dict
from .dataclasses import strictdataclass 
import json
from abc import ABC, abstractmethod
from email.message import EmailMessage
import smtplib


@strictdataclass
class Notificator():
    database: str
    recipients_table: str
    recipients_id_column: str 
    recipients_active_column:str
    recipients_authorized_column:str = 'Authorized'
    recipients_name_column: str = 'Name'
    telescopes_table:str = 'Telescopes'
    telescopes_users_column:str = 'Users'
    telescopes_roof_column:str = 'RoofIndex'
    sql_user:str = 'generic_obstech'

    
        
    def select_users(self, user_criteria: Dict[str, object] = {}) -> Dict[str, object]:
        query = f"""
            SELECT  {self.recipients_name_column}, {self.recipients_id_column}
            FROM `{self.recipients_table}`
        """
        criteria = [f"{k} {repr(v)}" for k, v in user_criteria.items()]
        criteria.append(self.recipients_id_column)
        criteria = "\nAND ".join(criteria)
        query += f"    WHERE {criteria}"
        print(query)
        db = DataBase.from_credentials(database=self.database, user=self.sql_user)
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            res = cursor.fetchall()

        return dict(res)

    def select_root_users(self):
        res = self.select_users(user_criteria={"isRoot = ":1})
        return res

    def select_roof_users(self,roof_index):
        query = f"""
            SELECT  {self.telescopes_users_column}
            FROM `{self.telescopes_table}`
            WHERE {self.telescopes_roof_column} = {roof_index}
        """
        db = DataBase.from_credentials(database=self.database, user=self.sql_user)
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            res = cursor.fetchall()
        users = sum([json.loads(item[0])['users'] for item in res],[])
        users = list(dict.fromkeys(users))
        criteria = {f"{self.recipients_name_column} REGEXP ":"|".join(users)}
        
        return self.select_users(user_criteria=criteria)

    def broadcast(
        self, 
        message: str, 
        /, *,
        user_criteria: Dict[str,object] = {},
        error_id: str = 260757924, # perhaps caller should state it instead
    ) -> None:
   
        users = self.select_users(user_criteria)
        for id, name in users:
            self.send_message(message, id, name, error_id=error_id) 

@strictdataclass
class TelegramBroadcastBot(Notificator):

    token: str
    user: str = 'generic_obstech'
    

    @classmethod
    def from_credentials(
            cls, 
            user: str = 'generic_obstech'
    ) -> TelegramBroadcastBot:

        creds = Credentials.load('telegram',user=user) 
        token = creds['token']
        del creds['token']

        return cls(token=token, **creds)
   
    
    def send_message(
        self, 
        message: str, 
        ids: list[str], 
        /, *,
        name: str = 'user',
        error_id: str = '', 
    ):
        for id in ids:
            req_url = (
                f"https://api.telegram.org/bot{self.token}/"
                f"sendMessage?parse_mode=Markdown&chat_id={id}&text={message}"
            )
            res = requests.get(req_url)
        
            # report error to another user if error_id is provided 
            if not res.json()['ok']:
                error_message = f"Error sending message to {name} ID={id}: {res}"
                print(error_message)
                if error_id:
                    self.send_message(error_message, id=error_id)
        


@strictdataclass
class EmailNotificator(Notificator):

    user: str 
    password: str
    smtp_server='smtp.gmail.com:587'

    @classmethod
    def from_credentials(
            cls, 
            user: str = 'generic_obstech'
    ) -> EmailNotificator:

        creds = Credentials.load('email',user=user) 
        
        return cls( **creds)
   
    
    def send_message(
        self, 
        message: str, 
        id_list: list[str], 
        /, *,
        name: str = 'user',
        error_id: str = '', 
        subject:str
    ):
        

        msg = EmailMessage()
        msg.set_content(message)

        msg["From"] = f"{name}<{self.user}>"
        msg["To"] = self.user
        msg["Ccc"] = '%s' % ','.join(id_list)
        msg["Subject"] = subject

        server = smtplib.SMTP(self.smtp_server)
        server.starttls()
        server.login(self.user, self.password)
        _problems = server.send_message(msg)
        server.quit()
