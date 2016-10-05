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

def make_email(from_addr, to, role, target=None):
    assert role in ROLES

    msg = MIMEMultipart()
    msg['From'] = from_addr
    if type(to) == str:
        msg['To'] = to
    else:
        msg['To'] = ', '.join(to)
    msg['Subject'] = 'Are you an assassin?'
    msg.add_header('Reply-to', REPLY_ADDR)

    # Compose the real body of the message.
    body = '{}; you are {} {}.'.format(ROLES[role]['answer'], ROLES[role]['article'], role)
    if role == 'assassin':
        body += '  Your target is {}.'.format(target)

    # Make up a few lines of random glop so the real message doesn't show
    # up in someone's gmail inbox overview which might be seen by someone glancing
    # at her monitor.
    def fluff_lines(num_lines):
        return '\n'.join('=*+-#' * 10 for x in range(num_lines))

    # Put it together to generate the final message body.
    body = fluff_lines(3) + '\n\n' + body + '\n\n' + fluff_lines(1)

    msg.attach(MIMEText(body, 'plain'))

    return msg

def make_slack_msg(target_list, player_list):
    msg = '\n'.join(["This week's assassins and targets are assigned, and emails have been sent.",
                     'The roster is:',
                     '*Targets*: "{}"',
                     '*Players*: "{}"',
                     '*GAME ON*'])
    return msg.format(', '.join(targets), ', '.join(players))

def commastring_to_list(string, capitalize=False):
    if capitalize:
        return [item.strip().capitalize() for item in string.split(',')]
    else:
        return [item.strip() for item in string.split(',')]

def get_cred(username):
    password = getpass.getpass('Please enter password for {}: '.format(username))
    return (username, password)

def email_login(cred):
    print 'Logging in to smtp.gmail.com as {}.'.format(cred[0])
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(*cred)
    return server

def email_send(server, to, msg, dry_run=True):
    if dry_run:
        print 'Will send this email to {}:'.format(to)
        print '====='
        print msg.as_string()
        print '====='
        print
    else:
        server.sendmail(msg['From'], to, msg.as_string())

def email_logout(server):
    print 'Logging out of smtp.gmail.com.'
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
        msg = make_email(EMAIL_ACCOUNT, to, 'target')
        email_list.append((to, msg))

        to = EMAILS[assassin]
        msg = make_email(EMAIL_ACCOUNT, to, 'assassin', target)
        email_list.append((to, msg))

    for guard in guards:
        to = EMAILS[guard]
        msg = make_email(EMAIL_ACCOUNT, to, 'guard')
        email_list.append((to, msg))

    email_server = email_login(cred)
    for to, msg in email_list:
        email_send(email_server, to, msg, dry_run)
    email_logout(email_server)

def choose_assassins(targets, players):
    """function which assigns assassins for each target."""

    ta_list = []
    guards = players[:]
    for t in targets:
        # Choose an assassin for each target.
        a = random.choice(guards)
        guards.remove(a)
        ta_list.append((t, a))
    return ta_list, guards

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
    ta_list, guards = choose_assassins(targets, players)

    # Send out the results.
    send_results(ta_list, guards, dry_run=args.dry_run)

    # Print a nice message to be posted in slack.
    print make_slack_msg(targets, players)
