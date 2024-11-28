import socket, urllib.request

def helper_1():
    hostname = socket.gethostname()
    helper_1 = socket.gethostbyname(hostname)
    return helper_1

def helper_2():
    with urllib.request.urlopen('https://api.ipify.org') as response:
        return response.read().decode('utf-8')

def main():
    print("Local: " + helper_1())
    print("Public: " + helper_2())

if __name__ == "__main__":
    main()