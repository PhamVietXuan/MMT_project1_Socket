import socket
def HandleUsernameAndPassword(requesting_file):
        temp=requesting_file.split('?')[1]
        temp2=temp.split('&')
        client_username=temp2[0]
        client_password=temp2[1]
        client_username=client_username.split('=')[1]
        client_password=client_password.split('=')[1]
        print(client_username)
        print(client_password)
        if(client_username == server_username and client_password == server_password):
            myfile='profile.html'
        else:
            myfile='error.html'



server_username = 'admin'
server_password = '123456'
HOST,PORT = '127.0.0.1',8000
 
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.bind((HOST,PORT))
my_socket.listen(1)
 
print('Serving on port ',PORT)
 
while True:
    connection,address = my_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    string_list = request.split(' ')     # Split request from spaces
    print (string_list)
    if len(string_list) < 2:
        break
    method = string_list[0]
    requesting_file = string_list[1]
    
    print('Client request ',requesting_file)
    myfile = requesting_file.split('?')[0]
    myfile = myfile.lstrip('/')
    if (requesting_file.find('?')!=-1):
        myfile=HandleUsernameAndPassword(requesting_file)
    
    try:
        file = open(myfile,'rb') # open file , r => read , b => byte format
        response = file.read()
        file.close()
 
        header = 'HTTP/1.1 200 OK\n'
 
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
