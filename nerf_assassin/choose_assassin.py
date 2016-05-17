#! /usr/bin/env python

# vim: set ai sw=4 et:

import os
import sys
import random
import argparse
import getpass
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# Need a local module which defines the following symbols
from emails import EMAILS, EMAIL_ACCOUNT, REPLY_ADDR

# There are 2 critical pieces of information for each role:
# 1: The answer to the question: "Are you the assassin?"
# 2: The article to use when telling someone he or she has a particluar
#    role.  Formerly, since there were only 1 target and 1 assassin, they got
#    a definite article ("the") while, guards got an indefinite article ("a").
#    Now, since we support multiple target/assassin pairs, they also get
#    indefinite articles.
ROLES = {'target': {'answer': 'No', 'article':'a'},
         'assassin': {'answer': 'Yes', 'article':'an'},
         'guard': {'answer': 'No', 'article':'a'}}

PLAYERS = 'Doug, Pat, Paul, Brandon, Bin, Huong, Matt, Fred, Alex, Ashish, Scott, Bryan'

def make_msg(from_addr, to, role, target=None):
    assert role in ROLES

    msg = MIMEMultipart()
    msg['From'] = from_addr
    if type(to) == str:
        msg['To'] = to
    else:
        msg['To'] = ', '.join(to)
    msg['Subject'] = 'Are you an assassin?'
    msg.add_header('Reply-to', REPLY_ADDR)

    body = '{}; you are {} {}.'.format(ROLES[role]['answer'], ROLES[role]['article'], role)
    if role == 'assassin':
        body += '  Your target is {}.'.format(target)

    msg.attach(MIMEText(body, 'plain'))

    return msg

def commastring_to_list(string, capitalize=False):
    if capitalize:
        return [item.strip().capitalize() for item in string.split(',')]
    else:
        return [item.strip() for item in string.split(',')]

def get_cred(username):
    password = getpass.getpass('Please enter password for {}: '.format(username))
    return (username, password)

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

def send_results(ta_list, guards, dry_run=True):
    for t, a in ta_list:
        print '{} is {}\'s target.'.format(t, a)
    for guard in guards:
        print '{} is a guard.'.format(guard)

    cred = get_cred(EMAIL_ACCOUNT)

    # Okay; we've got our players and their roles.
    # Let's compose email messages, and send them.
    email_list = []

    for target, assassin in ta_list:
        to = EMAILS[target]
        msg = make_msg(EMAIL_ACCOUNT, to, 'target')
        email_list.append((to, msg))

        to = EMAILS[assassin]
        msg = make_msg(EMAIL_ACCOUNT, to, 'assassin', target)
        email_list.append((to, msg))

    for guard in guards:
        to = EMAILS[guard]
        msg = make_msg(EMAIL_ACCOUNT, to, 'guard')
        email_list.append((to, msg))

    for to, msg in email_list:
        if dry_run:
            print 'Will send this email to {}:'.format(to)
            print '====='
            print msg.as_string()
            print '====='
            print
        else:
            sendit(cred, to, msg)

def choose_assassins(targets, players):
    """function which assigns assassins for each target.
    Note: the input list "players" will have the chosen assassins
    removed."""

    ta_list = []
    for t in targets:
        # Choose an assassin for each target.
        a = random.choice(players)
        players.remove(a)
        ta_list.append((t, a))
    return ta_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('targets')
    parser.add_argument('-p', '--players', default=PLAYERS)
    parser.add_argument('-d', '--dry_run', action='store_true')

    args = parser.parse_args()

    # We need to know the email address of every player.
    players = commastring_to_list(args.players, capitalize=True)
    for p in players:
        assert p in EMAILS, '{} is an invalid player.'.format(p)

    # The targets might or might not be in the list of players, but
    # either way, we must know their email addresses
    targets = commastring_to_list(args.targets, capitalize=True)
    for t in targets:
        assert t in EMAILS, '{} is an invalid target.'.format(t)
        try:
            players.remove(t)
        except ValueError:
            pass

    # Choose an assassin for each target.
    ta_list = choose_assassins(targets, players)

    # All the remaining players are guards.
    send_results(ta_list, players, dry_run=args.dry_run)
