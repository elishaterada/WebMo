#!/usr/bin/env python

"""
Webmo

Enter full URL and monitor frequency in seconds to get started
"""

import sys
import urllib2
from datetime import datetime
import time
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from ConfigParser import SafeConfigParser


# Get current time in pretty format
def pretty_time():
    now = datetime.now()
    pretty_time_format = now.strftime("%Y-%m-%d %H:%M:%S")
    return pretty_time_format


# Query the content from given URL
def website_content_query(website_url):
    try:
        soup = BeautifulSoup(urllib2.urlopen(website_url))
        website_content = str(soup)
    except urllib2.HTTPError or urllib2.URLError:
        print "There is an error with the request"
        return

    return website_content


# Send email notification
def send_notification(result):

    # Load and parse config file
    parser = SafeConfigParser()
    parser.read('settings.cfg')
    recipient_email = parser.get('email', 'recipient')
    gmail_user = parser.get('email', 'gmail_user')
    gmail_pwd = parser.get('email', 'gmail_pwd')

    # Create minimal message
    msg = MIMEText(result)
    msg['From'] = gmail_user
    msg['To'] = recipient_email
    msg['Subject'] = "Notification"

    # Send message
    mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(gmail_user, gmail_pwd)
    mail_server.sendmail(gmail_user, recipient_email, msg.as_string())
    mail_server.close()
    return


def main(argv=None):
    if argv is None:
        argv = sys.argv

    #0 Check and parse user input
    if len(argv) < 3:
        print "Please enter website URL and query frequency"
        exit()

    website_url = argv[1]
    monitor_frequency = argv[2]

    #1 Initial query for the website content to compare against new query
    old_content = website_content_query(website_url)

    while True:

        #2 Compare length of old and new content and process the result
        temp_new_content = website_content_query(website_url)

        # If there is an error with query result, skip this round of check
        if temp_new_content is None:
            time.sleep(int(monitor_frequency))
            continue
        else:
            new_content = temp_new_content

        # Send notification if there is any difference
        if len(new_content) != len(old_content):

            current_time = pretty_time()
            result = current_time + " - Updated - " + website_url + "\n"

            # Send email notification
            send_notification(result)

            # The updated content becomes old content for successive query
            old_content = new_content

        # Record unchanged if there is no difference
        else:
            current_time = pretty_time()
            result = current_time + " - Unchanged - " + website_url + "\n"

        #3 Log result
        with open('./report.log', 'a') as f:
            f.write(result)

        #4 Wait for specified time period
        time.sleep(int(monitor_frequency))

if __name__ == "__main__":
    sys.exit(main())
