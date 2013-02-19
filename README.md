WebMo
========

*Version 0.24*

WebMo is a Python script that monitors the website notify you via email when any difference is found.

Setup
-----

1. Add your Gmail account information in settings.cfg

2. Run the program with full website URL path and monitor frequency in seconds

Notice
------

* This program is tested on Python 2.7.2
* You need BeautifulSoup installed in your Python environment
* This program will use your Gmail account to send email so your computer doesn't need to be setup to send email.
* This program simply compares the length of old and new content so this does not work for websites that return different length of content every time (e.g. http://google.com/).
