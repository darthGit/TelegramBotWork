import paramiko
import os

class ExeComands:
    
    def __init__(self):
        print('Init ExeComands!')

    def run_ping(self, ip_adress : str):
        if self.__is_host_up(ip_adress=ip_adress):
            return "Host is up!"
        else:
            return "Host is down!"

    def run_killall(self, ip_adress):
        if self.__is_host_up(ip_adress=ip_adress):
            connect = paramiko.SSHClient()
            connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            connect.connect(hostname=ip_adress, username='root', password='toor')
            stdin, stdout, stderr = connect.exec_command('killall xinit')
            connect.close()
            result = ''
            for line in stdout.readlines():
                print(line)
                result = result + line
            return result

    
    def run_delete_check(self, ip_adress):
        None

    def run_reboot(self, ip_adress):
        connect = paramiko.SSHClient()
        connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connect.connect(hostname=ip_adress, username='root', password='toor')
        stdin, stdout, stderr = connect.exec_command('reboot')
        connect.close()
        result = ''
        for line in stdout.readlines():
            print(line)
            result = result + line
        return result

    def get_tty(self, ip_adress):
        connect = paramiko.SSHClient()
        connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connect.connect(hostname=ip_adress, username='root', password='toor')
        stdin, stdout, stderr = connect.exec_command('dmesg | grep tty')
        connect.close()
        result = ''
        for line in stdout.readlines():
            print(line)
            result = result + line
        return result

    def swap_tty(self, ip_adress, device, tty):
        None

    def __is_host_up(self, ip_adress: str):
        response = os.system('ping -c 3 %s -i 0.2' % (ip_adress))
        if response == 0:
            return True
        else:
            return False
    
