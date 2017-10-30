import socket

def get_local_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    s.setblocking(False)
    local_ip_address = s.getsockname()[0]
    s.close()
    return local_ip_address
