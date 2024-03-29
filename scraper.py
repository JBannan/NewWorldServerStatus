import requests

from bs4 import BeautifulSoup

url='https://www.newworld.com/en-us/support/server-status'
#url = "https://old.reddit.com/top/"

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
def scrapeServerStatus (SERVER_NAME='Atlantis'):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    list = soup.find("div", attrs={'class':'ags-ServerStatus-content-responses-response ags-ServerStatus-content-responses-response--centered ags-js-serverResponse is-active', })
    servers = list.find_all("div", class_="ags-ServerStatus-content-responses-response-server")

    for server in servers:
        for string in server.strings:
            if SERVER_NAME in string:
                statUp = server.find("div", attrs={'class':'ags-ServerStatus-content-responses-response-server-status--up'})
                statDown = server.find("div", attrs={'class':'ags-ServerStatus-content-responses-response-server-status--down'})
                serverStatus = 'Server not found'
                if (statDown != None):
                    print('Server Down - ', SERVER_NAME)
                    serverStatus = 'The server is down'
                elif (statUp != None):
                    print('Server Up - ', SERVER_NAME)
                    serverStatus = 'The server is up'
                return serverStatus
    return 'Server not found'

def scrapeEast():
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    list = soup.find("div", attrs={'class':'ags-ServerStatus-content-responses-response ags-ServerStatus-content-responses-response--centered ags-js-serverResponse is-active', })
    servers = list.find_all("div", class_="ags-ServerStatus-content-responses-response-server")
    
    status_dict = {}

    for server in servers:
        serverName = 'default'
        for string in server.strings:
            if len(string.strip()) != 0:
                serverName = string.strip()
        statUp = server.find("div", attrs={'class':'ags-ServerStatus-content-responses-response-server-status--up'})
        statDown = server.find("div", attrs={'class':'ags-ServerStatus-content-responses-response-server-status--down'})
        serverStatus = 'Server not found'
        if (statDown != None):
            serverStatus = 'The server is down'
        elif (statUp != None):
            serverStatus = 'The server is up'
        else:
            print('no server found')
        status_dict[serverName] = serverStatus
    return status_dict

# Server status
''' <div class="ags-ServerStatus-content-responses-response ags-ServerStatus-content-responses-response--centered ags-js-serverResponse is-active" data-index="0">
        <div class="ags-ServerStatus-content-responses-response-server">
            <div class="ags-ServerStatus-content-responses-response-server-status ags-ServerStatus-content-responses-response-server-status--up"></div>
            <div class="ags-ServerStatus-content-responses-response-server-name">
                Atlantis
            </div>  
        </div>
    </div>'''   

