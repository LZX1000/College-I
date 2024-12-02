import os, socket, urllib.request, time

def get_current_time():
    return time.strftime("%H:%M:%S", time.localtime())

def helper_1():
    hostname = socket.gethostname()
    helper_1 = socket.gethostbyname(hostname)
    return helper_1

def helper_2():
    with urllib.request.urlopen('https://api.ipify.org') as response:
        return response.read().decode('utf-8')

def helper_3():
    return {
        "current_time": get_current_time(),
        "local": helper_1(),
        "public": helper_2(),
        "platform": os.name,
        "hostname": socket.gethostname()
    }

def main():
    stats = helper_3()

    try:
        with open("interesting_stats.txt", "a") as file:
            file.write(", ".join([f"{key}: {value}" for key, value in stats])  + "\n\n")
    except FileNotFoundError:
        with open("interesting_stats.txt", "w") as file:
            file.write(", ".join([f"{key}: {value}" for key, value in stats]) + "\n\n")

if __name__ == "__main__":
    main()