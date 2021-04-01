'''
Created on Mar 30, 2021

@author: daily
'''

import socket
import pandas as pd
import matplotlib.pyplot as plt
import io
import urllib, base64
from http.server import HTTPServer, BaseHTTPRequestHandler

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

def getData():
    data = pd.read_csv('network_log.txt', sep='\t', header=None)
    output = ''
    for r in range(len(data)):
        output += '&#9;'
        output += data.at[(len(data)-r-1), 0]
        output += '&#9;'
        output += data.at[(len(data)-r-1), 1]
        output += '&#9;'
        output += data.at[(len(data)-r-1), 2]
        output += '&#9;&#9;'
        output += data.at[(len(data)-r-1), 3]
        output += '</br>'
    return output

def getGraph():
    data = pd.read_csv('network_log.txt', sep='\t', header=None, names=['Date', 'Time', 'IP', 'Status', 'Bit'])
    data['Timestamp'] = data['Date'] + ' ' + data['Time']
    data.index = pd.to_datetime(data['Timestamp'], dayfirst=True)
    plt.plot('Bit', data=data)
    plt.xticks(size=7, rotation=90)
    fig = plt.gcf()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    html = '<img src = "%s"/>' % uri
    return html

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        
        output = ''
        output += '<html><body><pre>'
        output += '<h1>Network Status Log</h1>'
        output += getGraph()
        output += '</br>'
        output += '</br>'
        output += '&#9;<b>Date</b>&#9;&#9;<b>Time</b>&#9;&#9;<b>IP</b>&#9;&#9;<b>Status</b>'
        output += '</br>'
        output += getData()
        output += '</br>'
        output += '</pre></body></html>'
        
        self.wfile.write(output.encode())
        
def main():
    PORT = 420
    server_address = ('0.0.0.0', PORT)
    server = HTTPServer(server_address, requestHandler)
    print('Server running on ' + ip_address + ':' + str(PORT))
    server.serve_forever()

if __name__ == '__main__':
    main()