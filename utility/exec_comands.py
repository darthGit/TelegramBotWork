import paramiko

class ExeComands:

    def __init__(self):
        print('Init ExeComands!')

    def run_ping(self, ip_adress : str):
        connect = paramiko.SSHClient()
        connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connect.connect(hostname='localhost', username='darthgit', password='toor')
        stdin, stdout, stderr = connect.exec_command('ping '+ ip_adress + ' -c 5')
        result = ''
        for line in stdout.readlines():
            print(line)
            result = result + line
        connect.close()
        return result

    def run_killall(self, ip_adress):
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


    
    
