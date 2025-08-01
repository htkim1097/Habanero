import socket

comm_config = {
    "socket_family" : socket.AF_INET, 
    "socket_type" : socket.SOCK_STREAM,
    "address" : "localhost",
    "port" : 8080,
    "baudrate" : 1024,
}

db_config = {
    "host" : "localhost",
    "port" : 3306,
    "user" : "root",
    "password" : "0000",
    "charset" : "utf8",
}

