#! /usr/bin/env python

"""Choose assassin(s) and maybe targets for a nerf-assassin game.

Arguments:
    targets: Comma-separated list of targets.  If empty, targets will be
             chosen at random.
    -p players: list of players.
    -d, --dry-run: don't actually send emails; just run the chooser.
"""


# vim: set ai sw=4 et:

# import os
# import sys
import random
import argparse
import getpass
import smtplib
# I have no idea why pylint wants to complain about these imports.
# pylint: disable=import-error,no-name-in-module
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
# pylint: enable=import-error,no-name-in-module

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

def make_email(from_addr, recip, role, target_name=None):
    """Compose a message to a nerf assassin player.

    from_addr: The email address the message will be from.
    recip: The email address of the recipient.
    role: The player's role in the current game.
    target_name: If a player is the assassin, this is the target.
    """

    assert role in ROLES

    msg = MIMEMultipart()
    msg['From'] = from_addr
    if isinstance(recip, str):
        msg['To'] = recip
    else:
        msg['To'] = ', '.join(recip)
    msg['Subject'] = 'Are you an assassin?'
    msg.add_header('Reply-to', REPLY_ADDR)

    # Compose the real body of the message.
    body = '{}; you are {} {}.'.format(ROLES[role]['answer'], ROLES[role]['article'], role)
    if role == 'assassin':
        body += '  Your target is {}.'.format(target_name)

    def fluff_lines(num_lines):
        """Make up lines of random glop.

        Intended to be used for obscuration so the real message doesn't show
        up in someone's gmail inbox overview which might be seen by someone
        glancing at her monitor.
        """
        return '\n'.join('=*+-#' * 10 for x in range(num_lines))

    # Put it together to generate the final message body.
    body = fluff_lines(3) + '\n\n' + body + '\n\n' + fluff_lines(1)

    msg.attach(MIMEText(body, 'plain'))

    return msg

def make_slack_msg(target_list, player_list):
    """Emit a message suitable for posting to the assassing slack channel."""
    msg = '\n'.join(["This week's assassins and targets are assigned, and emails have been sent.",
                     'The roster is:',
                     '*Targets*: "{}"',
                     '*Players*: "{}"',
                     '*GAME ON*'])
    return msg.format(', '.join(target_list), ', '.join(player_list))

def commastring_to_list(string, capitalize=False):
    """Turn a comma separated list in a string to a python list."""
    if capitalize:
        return [item.strip().capitalize() for item in string.split(',')]
    return [item.strip() for item in string.split(',')]

def get_cred(username):
    """Get credentials (password) for a given username."""
    password = getpass.getpass('Please enter password for {}: '.format(username))
    return (username, password)

def email_login(cred):
    """Log into the gmail smtp server with the given credentials."""
    print 'Logging in to smtp.gmail.com as {}.'.format(cred[0])
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(*cred)
    print 'Login complete.'
    return server

def email_send(server, recip, msg, dry_run=True):
    """Send an email message.

    If dry_run is true, just print the message which would have been sent.
    """
    if dry_run:
        print 'Will send this email to {}:'.format(recip)
        print '====='
        print msg.as_string()
        print '====='
        print
    else:
        server.sendmail(msg['From'], recip, msg.as_string())

def email_logout(server):
    """Log out of an email session."""
    print 'Logging out of smtp.gmail.com.'
    server.quit()

def send_results(ta_list, guard_list, dry_run=True):
    """Once we've chosen roles for all players, send out the emails."""
    for target_name, assassin_name in ta_list:
        print '{} is {}\'s target.'.format(target_name, assassin_name)
    for guard_name in guard_list:
        print '{} is a guard.'.format(guard_name)

    cred = get_cred(EMAIL_ACCOUNT)

    # Okay; we've got our players and their roles.
    # Let's compose email messages, and send them.
    email_list = []

    for target_name, assassin_name in ta_list:
        recip = EMAILS[target_name]
        msg = make_email(EMAIL_ACCOUNT, recip, 'target')
        email_list.append((recip, msg))

        recip = EMAILS[assassin_name]
        msg = make_email(EMAIL_ACCOUNT, recip, 'assassin', target_name)
        email_list.append((recip, msg))

    for guard_name in guard_list:
        recip = EMAILS[guard_name]
        msg = make_email(EMAIL_ACCOUNT, recip, 'guard')
        email_list.append((recip, msg))

    email_server = email_login(cred)
    for recip, msg in email_list:
        email_send(email_server, recip, msg, dry_run)
    email_logout(email_server)

def choose_assassins(target_list, player_list):
    """function which assigns assassins for each target."""

    ta_list = []
    guard_list = player_list[:]
    for target_name in target_list:
        # Choose an assassin for each target.
        assassin_name = random.choice(guard_list)
        guard_list.remove(assassin_name)
        ta_list.append((target_name, assassin_name))
    return ta_list, guard_list

if __name__ == '__main__':
    # Stupid pylint wants a bunch of variables (including parser!) to be
    #  named as constants.  That would be worse, not better.
    # pylint: disable=invalid-name
    parser = argparse.ArgumentParser()
    parser.add_argument('targets', nargs='?')
    parser.add_argument('-p', '--players', default=PLAYERS)
    parser.add_argument('-d', '--dry_run', action='store_true')

    args = parser.parse_args()

    # print args
    # sys.exit(0)

    # We need to know the email address of every player.
    players = commastring_to_list(args.players, capitalize=True)
    for p in players:
        assert p in EMAILS, '{} is an invalid player.'.format(p)

    # The targets might or might not be in the list of players, but
    # either way, we must know their email addresses
    if args.targets is None:
        targets = (random.choice(players),)
        print "targets are: {}".format(targets)
    else:
        targets = commastring_to_list(args.targets, capitalize=True)

    for target in targets:
        assert target in EMAILS, '{} is an invalid target.'.format(target)
        try:
            players.remove(target)
        except ValueError:
            pass

    # Choose an assassin for each target.
    ta_pairs, guards = choose_assassins(targets, players)

    # Send out the results.
    send_results(ta_pairs, guards, dry_run=args.dry_run)

    # Print a nice message to be posted in slack.
    print make_slack_msg(targets, players)
