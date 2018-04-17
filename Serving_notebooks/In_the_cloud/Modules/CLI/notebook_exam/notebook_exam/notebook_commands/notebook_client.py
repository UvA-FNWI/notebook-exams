import socket
import sys

import pysftp

class AuthException(Exception):
    pass
    
hub_host = 'notebookexam.fnwi.uva.nl'
    
class Client():
    hub_host = 'notebookexam.fnwi.uva.nl'
    
    def __init__(self, password):
        self.password = password
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_address = (self.hub_host, 2222)
        self.sock.connect(self.server_address)

        if not self.auth():
            raise AuthException('The password is incorrect.')
        
    def send(self, data):
        self.sock.send(data)
        
    def recv(self, to_stdout=False, wait=True):
        if wait:
            out = ''
            while True:
                d = self.sock.recv(1024)
                
                if '__end__' in d:
                    if to_stdout:
                        sys.stdout.write(d[:-len('__end__')])
                        
                        print ""
                        
                        return
                    else:
                        out += d[:-len('__end__')]
                        
                        return out
                else:
                    if to_stdout:
                        sys.stdout.write(d)
                    else:
                        out += d
        else:
            return self.sock.recv(1024)
    
    def close(self):
        self.sock.close()
        
    def auth(self):
        self.send('auth %s' % self.password)
        
        return (self.recv(wait=False).strip() == 'authenticated')
        
    def send_and_recv(self, command, to_stdout=False):
        self.send(command)
        
        return self.recv(to_stdout)
        
    def execute(self, command, to_stdout=False):
        return self.send_and_recv('exec %s' % command, to_stdout)
        
def upload_file(client, path):
    upload_pass = client.send_and_recv('request-upload')
    
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    
    with pysftp.Connection(hub_host, username='delivery', password=upload_pass, cnopts=cnopts) as sftp:
        with sftp.cd('/incoming'):
            sftp.put(path)
            
def download_file(client, path):
    upload_pass = client.send_and_recv('request-upload')
    
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    
    with pysftp.Connection(hub_host, username='delivery', password=upload_pass, cnopts=cnopts) as sftp:
        with sftp.cd('/incoming'):
            sftp.get(path)