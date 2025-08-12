import socket

comm_config = {
    "socket_family" : socket.AF_INET, 
    "socket_type" : socket.SOCK_STREAM,
    "host" : "192.168.0.62",
    "port" : 8080,
    "baudrate" : 1024,
    "charset" : "utf8",
}

db_config = {
    "host" : "localhost",
    "port" : 3306,
    "user" : "root",
    "password" : "0000",
    "charset" : "utf8",
}