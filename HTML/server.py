import socket
from msvcrt import getch

server_username = 'admin'
server_password = '123456'
HOST,PORT = '127.0.0.1',8000


def HandleUserAndPass(data):
    UserAndPass=data.split('\n')[2]
    temp=UserAndPass.split('&')
    client_username=temp[0]
    client_password=temp[1]
    client_username=client_username.split('=')[1]
    client_password=client_password.split('=')[1]
    if(client_username == server_username and client_password == server_password):
         myfile='profile.html'
    else:
          myfile='error.html'
    return myfile

def HandleReadFile(file_name):
    getData=open(file_name,'rb')
    data=getData.read()
    return data

my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.bind((HOST,PORT))
my_socket.listen(1)

print('Serving on port ',PORT)
 
while True:
    connection,address = my_socket.accept()

    request = connection.recv(1024).decode('utf-8')
    string_list = request.split(' ')     # Split request from spaces
    if len(string_list) < 2:
        break
    method = string_list[0]
    requesting_file = string_list[1]
    
    if len(string_list) < 2:  
        continue

    requesting_file = string_list[1]
    print('Client request ',requesting_file)
    myfile = requesting_file.split('?')[0]
    myfile = myfile.lstrip('/')
    temp=string_list[len(string_list)-1]
    if(myfile=='profile.html'):
        myfile=HandleUserAndPass(string_list[len(string_list)-1])
    
    try:
        response=HandleReadFile(myfile)
 
        header = 'HTTP/1.1 200 OK\n'
        if(myfile=='error.html'):
            header='HTTP/1.1 404 Not Found\n'
 
        if(myfile.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif(myfile.endswith(".css")):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'
 
        header += 'Content-Type: '+str(mimetype)+'\n\n'
 
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
 
    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()

