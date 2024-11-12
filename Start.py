import subprocess, os, platform, psutil

def is_script_running(script_name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'cmd.exe' in proc.info['name'] and script_name in cmdline:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def main():
    script_path = os.path.join(os.path.dirname(__file__), 'Main.py')
    if not is_script_running('Main.py'):
        if platform.system() == "Windows":
            command = f'start cmd /k "python {script_path}"'
            subprocess.Popen(command, shell=True)
        else:
            command = f'python {script_path}'
            subprocess.Popen(['x-terminal-emulator', '-e', command])

if __name__ == "__main__":
    main()