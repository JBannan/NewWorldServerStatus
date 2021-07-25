# New World Server Status Detector

This is a simple Discord bot that scrapes the New World Server Status page available here: https://www.newworld.com/en-us/support/server-status

This works on a simple get request to the web page using the python "request" package. The response is then parsed using BeautifulSoup.
The method used currently only works for US East servers. Without user input, the page defaults to the first set of servers (US East).
