#!/usr/bin/env python

"""
Webmo

Version 0.3
Enter full URL and monitor frequency in seconds to get started
"""

import sys
import urllib2
import re
from datetime import datetime
import time
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from ConfigParser import SafeConfigParser

# Get current time in pretty format
def pretty_time():
	now = datetime.now()
	pretty_time_format = str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)
	return pretty_time_format
	
# Query the content from given URL
def website_content_query(website_url):
	try:
		soup = BeautifulSoup(urllib2.urlopen(website_url))
		website_content = str(soup)
	except urllib2.HTTPError:
		print "There is an error with website"
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
	
	old_content = ""
	
	while True:

		#1 Query for the website content
		new_content = website_content_query(website_url)

		#2 Compare length of old and new content and process the result
		current_time = pretty_time()

		if old_content is "":
			old_content = new_content
			continue
		elif len(new_content) != len(old_content):
			result = current_time + " - Updated - " + website_url + "\n"

			# Send email notification
			send_notification(result)

			# The updated content becomes old content for successive query
			old_content = new_content			
		else:
			result = current_time + " - Unchanged - " + website_url + "\n"

		#3 Log result
		with open('./report.log', 'a') as f:
			f.write(result)

		#4 Wait for specified time period
		# print "Waiting for next process in", int(monitor_frequency), "seconds"
		time.sleep(int(monitor_frequency))

if __name__ == "__main__":
	sys.exit(main())
