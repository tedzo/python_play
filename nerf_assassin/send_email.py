#! /usr/bin/env python

# vim: set ai sw=4 et sm:

import sys
import os
import getpass
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# Need a local module which defines the following symbols
from emails import EMAILS, EMAIL_ACCOUNT, REPLY_ADDR

ROLES = {'target': {'answer': 'No', 'article':'the'},
         'assassin': {'answer': 'Yes', 'article':'the'},
         'guard': {'answer': 'No', 'article':'a'}}

def sendit_simple(cred, fromaddr, toaddrs, msg):
    """Command to send a messsage.
    Note: for this to work in gmail, the account being used must have
    enabled "less secure apps"."""

    user, pwd = cred

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(*cred)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def sendit(cred, to, msg):
    """Command to send a messsage.
    Msg must contain 'From' and 'To" fields.
    Note: for this to work in gmail, the account being used must have
    enabled "less secure apps"."""

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(*cred)
    server.sendmail(msg['From'], to, msg.as_string())
    server.quit()

def make_msg(cred, to, role):
    user, pwd = cred
    assert role in ROLES

    msg = MIMEMultipart()
    msg['From'] = user
    if type(to) == str:
        msg['To'] = to
    else:
        msg['To'] = ', '.join(to)
    msg.add_header('Reply-to', REPLY_ADDR)
    msg['Subject'] = 'Are you the assassin?'

    body = '{}; you are {} {}.'.format(ROLES[role]['answer'], ROLES[role]['article'], role)
    msg.attach(MIMEText(body, 'plain'))

    return msg

def get_cred():
    username = EMAIL_ACCOUNT
    password = getpass.getpass('Please enter password for {}: '.format(username))
    return (username, password)

if __name__ == '__main__':
    cred = get_cred()
    to = [EMAILS['Ted'], EMAILS['Tedzo']]

