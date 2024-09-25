import paramiko
import subprocess
import socket
import struct
from elevate import elevate

from .printing import print, input


class Remote:

    def __init__(self,
                 host: str,
                 username: str,
                 password: str = None,
                 public_key: str = None,
                 port: int = 22,
                 sudo: bool = False,
                 debug: bool = False):
        self.host = host
        self.username = username
        self.public_key = public_key
        self.port = port
        self.sudo = sudo
        self.debug = debug
        self.is_local = False

        if self.is_loopback(host):
            self.is_local = True
            if self.sudo:
                elevate(graphical=False)
                self.sudo = False
            return

        with print(f'🟪[Connecting to {host} as {username}]', close='\n'):
            self.password = password or input(f'🟨Enter password for {username}@{host}: ', password=True)
            self.client = self.create_client()

    def create_client(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host,
                    username=self.username,
                    password=self.password,
                    key_filename=self.public_key,
                    allow_agent=True,
                    port=self.port)
        print('🟩Connected')
        return ssh

    def run(self, command, sudo=...):
        if sudo or self.sudo and sudo is ...:
            command = f'sudo {command}'
        if self.debug:
            print(f'🟩$ {command}')
            print.indent()

        if self.is_local:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            stdout = stdout.decode('utf-8').strip()
            stderr = stderr.decode('utf-8').strip()
        else:
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout = stdout.read().decode('utf-8').strip()
            stderr = stderr.read().decode('utf-8').strip()

        if self.debug:
            if stdout:
                with print('STDOUT', indent='  | '):
                    print(stdout)
            if stderr:
                with print('STDERR', indent='  | '):
                    print(stderr)
            print.dedent()
        return stdout, stderr

    def run_safe(self, command):
        stdout, stderr = self.run(command)
        if stderr:
            raise RuntimeError(stderr)
        return stdout

    def get(self, path) -> str:
        if self.is_local:
            with open(path) as f:
                return f.read()
        else:
            with self.client.open_sftp().file(path, 'r') as f:
                return f.read().decode('utf-8', errors='replace')

    def put(self, path, content):
        if self.is_local:
            with open(path, 'w') as f:
                f.write(content)
        else:
            with self.client.open_sftp().file(path, 'w') as f:
                f.write(content)

    def is_loopback(self, host: str) -> bool:
        loopback_checker = {
            socket.AF_INET: lambda x: struct.unpack('!I', socket.inet_aton(x))[0] >> (32-8) == 127,
            socket.AF_INET6: lambda x: x == '::1'
        }
        for family in (socket.AF_INET, socket.AF_INET6):
            try:
                r = socket.getaddrinfo(host, None, family, socket.SOCK_STREAM)
            except socket.gaierror:
                return False
            for family, _, _, _, sockaddr in r:
                if not loopback_checker[family](sockaddr[0]):
                    return False
        return True
