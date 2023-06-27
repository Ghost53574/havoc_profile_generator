from . import util
from . import enum

from faker import Factory
import random
import ipaddress
import os

Faker = Factory.create
fake = Faker()

Arch = enum.Arch
AllocEnum = enum.AllocEnum
ExecuteEnum = enum.ExecuteEnum

search_path = os.environ['PATH']
windows_dir_root = "C:\\\\Windows"
windows_dir_sysnative = "\\System32"
windows_dir_syswow64 = "\\SysWow64"

# Default profile settings
all_interfaces = "0.0.0.0"
localhost = "127.0.0.1"
default_port = 40056
default_user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
default_response = [ "Content-type: text/plain; charset=utf-8", "Connection: keep-alive", "Cache-control: non-cache" ]
default_headers = [ "Content-type: text/plain; charset=utf-8", "Accept-Language: en-US" ]
default_urls = [ "/images/dog.jpg", "/images/cat.jpg", "/images/dolphin.jpg" ]

# Default files needed
default_compiler_x64 = "x86_64-w64-mingw32-gcc"
default_compiler_x86 = "i686-w64-mingw32-gcc"
default_assembler = "nasm"

# Default OPSEC safer programs to spawn to
default_spawnto_opsec = {
    "gpupdate": "gpupdate.exe /Target:User /Sync /Force",
    "werfault": "Werfault.exe",
    "svchost": "svchost.exe -k netsvcs",
    "dashost": "dasHost.exe ",
    "dllhost": "dllhost.exe /PROCESSID:",
    "conhost": "conhost.exe 0x4",
    "taskhostw": "taskhostw.exe"
}

default_spawnto_only_sysnative = [
    "dashost",
    "taskhostw",
    "conhost"
]

default_spawnto_all = [
    "gpupdate",
    "werfault",
    "svchost",
    "dashost",
    "dllhost",
    "conhost",
    "taskhostw"
]

default_pipenames = [
    "winsock",
    "mojo",
    "crashpad",
    "chromesync",
    "gecko",
    "guid",
    "chrome",
    "discord",
    "shellex",
    "pshost",
    "tcppipe",
    "ntsvcs",
    "trkwks"
]

class Base:
    def Find(self, 
             name: str,
            _search_path: str = None):
        if _search_path:
            paths = _search_path
        else:
            paths = search_path.split(":")
        for path in paths: 
            for root, _, files in os.walk(path):
                if name in files:
                    return os.path.join(root, name)
                
    def Get(self) -> object:
        return self
    
class Build(Base):
    def __init__(self, 
                 compiler_64: str = None, 
                 compiler_86: str = None, 
                 compiler_nasm: str = None) -> None:
        self.compiler_64 = None
        self.compiler_86 = None
        self.compiler_nasm = None

        if compiler_64:
            self.compiler_64 = compiler_64
        else:
            self.compiler_64 = self.Find(default_compiler_x64)
            if not self.compiler_64:
                util.print_fail(f"Cannot find {default_compiler_x64}")
        if compiler_86:
            self.compiler_86 = compiler_86
        else:
            self.compiler_86 = self.Find(default_compiler_x86)
            if not self.compiler_86:
                util.print_fail(f"Cannot find {default_compiler_x86}")
        if compiler_nasm:
            self.compiler_nasm = compiler_nasm
        else:
            self.compiler_nasm = self.Find(default_assembler)
            if not self.compiler_nasm:
                util.print_fail(f"Cannot find {default_assembler}")
            
    def Print(self) -> dict:
        template = {}
        if self.compiler_64:
            path = self.Find(self.compiler_64)
            if path:
                template["Compiler64"] = path
        if self.compiler_86:
            path = self.Find(self.compiler_86)
            if path:
                template["Compiler86"] = path
        if self.compiler_nasm:
            path = self.Find(self.compiler_nasm)
            if path:
                template["Nasm"] = path
        return template

class Teamserver(Base):
    def __init__(self, 
                 host: str, 
                 port: int, 
                 build: Build = None) -> None:
        self.host = host
        self.port = port
        self.build = None

        if not host or not port:
            self.host = all_interfaces
            self.port = default_port

        if build:
            self.build = build

    def Print(self) -> dict:
        template = {}
        if self.host and ipaddress.ip_address(self.host):
            template["Host"] = self.host
        if self.port and (self.port > 1 and self.port < 65535):
            template["Port"] = self.port
        if self.build:
            template["Build"] = self.build.Print()
        return template

class Operators(Base):
    def __init__(self) -> None:
        self.users = {}
    
    def Add_User(self, username, password, hashed = None) -> None:
        if username and password and not hashed:
            self.users[username] = password
        if username and password and hashed:
            self.users[username] = {password, hashed}
    
    def Print(self) -> dict:
        template = {}
        values = {}
        if self.users:
            for user in self.users:
                username = f"{user}"
                password = self.users[user]
                values["Password"] = password
                template[username] = values
        else:
            util.print_fail("No users in Operator block")
        return template
    
class Cert(Base):
    def __init__(self, 
                 cert_path, 
                 key_path) -> None:
        if os.path.isfile(cert_path):
            self.cert_path = cert_path
        else:
            util.print_fail("Certificate path does not exist")
        
        if os.path.isfile(key_path):
            self.key_path = key_path
        else:
            util.print_fail("Key path does not exist")
        
    def Print(self) -> dict:
        template = {}
        template["Cert"] = self.cert_path
        template["Key"] = self.key_path
        return template
    
class Proxy(Base):
    def __init__(self, 
                 host: str, 
                 port: int, 
                 username = None, 
                 password = None) -> None:
        self.host = host
        self.port = port
        self.username = None
        self.password = None
        if username and password:
            self.username = username
            self.password = password

    def Print(self) -> dict:
        template = {}
        template["Host"] = self.host
        template["Port"] = self.port
        if self.username and self.password:
            template["Username"] = self.username
            template["Password"] = self.password
        return template

class Response(Base):
    def __init__(self, headers) -> None:
        if headers:
            self.headers = headers

    def Print(self) -> dict:
        template = {}
        headers = []
        for header in self.headers:
            headers.append(header)
        template["Headers"] = headers
        return template
    
class Http_Listener(Cert, Base):
    host_rotation_types = [ "random", "round-robin" ]
    def __init__(self, 
                 name: str, 
                 hosts: list, 
                 port: int, 
                 host_bind: str,
                 killswitch: str = None,
                 workinghours: str = None,
                 secure: str = None,
                 host_rotation: str = None, 
                 user_agent: str = None, 
                 headers: list = None, 
                 urls: list = None, 
                 cert: Cert = None, 
                 proxy: Proxy = None, 
                 response: Response = None) -> None:
        self.name = name
        self.hosts = hosts
        self.port = port
        self.host_bind = host_bind
        self.killswitch = None
        self.workinghours = None
        self.host_rotation = None
        self.secure = None
        self.user_agent = None
        self.headers = None
        self.urls = None
        self.cert = None
        self.proxy = None
        self.reponse = None

        if host_rotation in self.host_rotation_types:
            self.host_rotation = host_rotation
        else:
            self.host_rotation = "round-robin"
        if user_agent:
            self.user_agent = user_agent
        else:
            self.user_agent = default_user_agent
        if headers:
            self.headers = headers
        else:
            self.headers = [ "Content-type: */*" ]
        if urls:
            self.urls = urls
        else:
            self.urls = [ "/" ]
        if not secure:
            self.secure = secure
        else:
            self.secure = "false"
        if not killswitch:
            self.killswitch = util.generate_killdate()
        else:
            self.killswitch = killswitch
        if not workinghours:
            self.workinghours = util.generate_workinghours()
        else:
            self.workinghours = workinghours
        if cert:
            self.cert = cert
        if proxy:
            self.proxy = proxy
        if response:
            self.response = response
        else:
            self.response = Response(default_headers)

    def Print(self) -> dict:
        template = {}
        template["Name"] = self.name
        template["PortBind"] = self.port
        template["Hosts"] = self.hosts
        template["HostBind"] = self.host_bind
        template["KillDate"] = self.killswitch
        template["WorkingHours"] = self.workinghours
        if self.host_rotation:
            template["HostRotation"] = self.host_rotation
        else:
            template["HostRotation"] = "round-robin"
        if self.secure:
            template["Secure"] = self.secure
        else:
            template["Secure"] = "false"
        template["UserAgent"] = self.user_agent
        template["Urls"] = self.urls
        template["Headers"] = self.headers
        if self.cert:
            template["Cert"] = self.cert.Print()
        if self.proxy:
            template["Proxy"] = self.proxy.Print()
        if self.response:
            if type(self.response) is not Response:
                self.response = Response(self.response)
            template["Response"] = self.response.Print()
        return template

class Smb_Listener(Cert, Base):
    host_rotation_types = [ "random", "round-robin" ]
    def __init__(self, 
                 name: str = None, 
                 pipename: str = None,
                 killdate: str = None,
                 workinghours: str = None) -> None:
        self.name = None
        self.pipename = None
        self.killdate = None
        self.workinghours = None

        if name:
            self.name = name
        else:
            self.name = str(fake.name()).split(" ")[1]

        if pipename:
            self.pipename = pipename
        else:
            temp = ""
            while not temp:
                temp = util.generate_pipename(None, None, random.choice(default_pipenames))
            if temp:
                self.pipename = temp
            else:
                util.print_fail("Failed to generate pipename")
        
        if killdate:
            self.killdate = killdate

        if workinghours:
            self.workinghours = workinghours

    def Print(self) -> dict:
        template = {}
        template["Name"] = self.name
        template["Pipename"] = self.pipename
        if self.killdate:
            template["KillDate"] = self.killdate
        if self.workinghours:
            template["WorkingHours"] = self.workinghours
        return template

class External_Listener(Cert, Base):
    def __init__(self, 
                 name: str, 
                 endpoint: str) -> None:
        self.name = name
        self.endpoint = endpoint

    def Print(self) -> dict:
        template = {}
        template["Name"] = self.name
        template["Endpoint"] = self.endpoint
        return template

class Listeners(Http_Listener, Smb_Listener):
    def __init__(self) -> None:
        self.http_listeners = []
        self.smb_listeners = []
        self.ext_listeners = []
    
    def Add_Http_Listener(self, 
                          listener: Http_Listener
                          ) -> None:
        self.http_listeners.append(listener.Print())

    def Add_Smb_Listener(self, 
                         listener: Smb_Listener
                         ) -> None:
        self.smb_listeners.append(listener.Print())

    def Add_External_Listener(self, 
                             listener: External_Listener
                             ) -> None:
        self.ext_listeners.append(listener.Print())

    def Print(self):
        listeners = []
        for listener in self.http_listeners:
            listener_dict = {}
            listener_dict["Http"] = listener
            listeners.append(listener_dict)
        for listener in self.smb_listeners:
            listener_dict = {}
            listener_dict["Smb"] = listener
            listeners.append(listener_dict)
        for listener in self.ext_listeners:
            listener_dict = {}
            listener_dict["External"] = listener
            listeners.append(listener_dict)
        return listeners

    def Get(self) -> object:
        return self
    
class Header(Base):
    def __init__(self, 
                 MagicMzX64: str = None, 
                 MagicMzX86: str = None,
                ) -> None:
        self.magicmzx64 = None
        self.magicmzx86 = None

        if MagicMzX64:
            self.magicmzx64 = MagicMzX64
        if MagicMzX86:
            self.magicmzx86 = MagicMzX86

    def Print(self) -> str:
        template = {}
        if self.magicmzx64:
            template["MagicMzX64"] = self.magicmzx64
        if self.magicmzx86:
            template["MagicMzX86"] = self.magicmzx86
        return template
    
class Binary(Base):
    def __init__(self,
                 header: Header = None,
                 replace_strx64: str = None,
                 replace_strx86: str = None
                 ) -> None:
        self.header = None
        self.replace_strx64 = None

        if header:
            self.header = header
        if replace_strx64:
            self.replace_strx64 = replace_strx64
        if replace_strx86:
            self.replace_strx86 = replace_strx86

    def Print(self) -> str:
        template = {}
        if self.header:
            template["Header"] = self.header.Print()
        if self.replace_strx64:
            template["ReplaceStringX64"] = self.replace_strx64
        if self.replace_strx86:
            template["ReplaceStringX86"] = self.replace_strx86
        return template

class Implant(Base):
    def __init__(self, 
                 sleep_mask: str = None, 
                 sleep_teq: str = None
                 ) -> None:
        self.sleep_mask = None
        self.sleep_teq = None
        if sleep_mask:
            self.sleep_mask = sleep_mask
        if sleep_teq:
            if sleep_teq in [ "WaitForSingleObject", "Foliage", "Ekko"]:
                self.sleep_teq = sleep_teq
            else:   
                self.sleep_teq = "WaitForSingleObject"

    def Print(self) -> str:
        template = {}
        if self.sleep_mask:
            template["SleepMask"] = self.sleep_mask
        if self.sleep_teq:
            template["SleepMaskTechnique"] = self.sleep_teq
        return template

class Injection(Base):
    ARCH_X86 = "x86"
    ARCH_X64 = "x64"
    ARCH_SYSWOW = "x86_64"

    def __init__(self, 
                 spawn_x64: str = None, 
                 spawn_x86: str = None,
                 alloc: AllocEnum = None,
                 execute: ExecuteEnum = None,
                 arch: Arch = Arch.X64,
                 sysnative: bool = False
                 ) -> None:
        self.sysnative_binary = None
        self.syswow_binary = None
        self.alloc = None
        self.execute = None

        if arch == Arch.X86_64:
            self.syswow_binary = self.Random(Arch.X86_64)
            self.sysnative_binary = self.Random(Arch.X64)
        elif arch == Arch.X64:
            self.sysnative_binary = self.Random(Arch.X64)
        elif arch == Arch.X86:
            self.sysnative_binary = self.Random(Arch.X86)
        else:
            self.sysnative_binary = self.Random(Arch.X86)

        if spawn_x64:
            self.spawn_x64 = spawn_x64
        else:
            if not sysnative and arch == Arch.X86_64:
                self.spawn_x64 = self.syswow_binary
            elif not sysnative and arch == Arch.X64:
                self.spawn_x64 = self.sysnative_binary
            else:
                self.spawn_x64 = self.sysnative_binary

        if spawn_x86:
            self.spawn_x86 = spawn_x86
        else:
            if not sysnative and arch == Arch.X86_64:
                self.spawn_x86 = self.syswow_binary
            elif not sysnative and arch == Arch.X86:
                self.spawn_x86 = self.sysnative_binary
            else:
                self.spawn_x86 = self.sysnative_binary

        if alloc:
            if alloc in AllocEnum:
                if alloc is AllocEnum.Win32:
                    alloc = "Win32"
                elif alloc is AllocEnum.Syscall:
                    alloc = "Native/Syscall"
            else:
                self.alloc = "None"
        
        if execute:
            if execute in ExecuteEnum:
                if execute is ExecuteEnum.Win32:
                    execute = "Win32"
                elif execute is ExecuteEnum.Syscall:
                    execute = "Native/Syscall"
            else:
                self.execute = "None"

    def Random(self, 
               arch: Arch
               ) -> str:
        if arch == Arch.X64 or arch == Arch.X86:
            windows_dir = f"{windows_dir_root}\\{windows_dir_sysnative}\\\\"
        elif arch == Arch.X86_64:
            windows_dir = f"{windows_dir_root}\\{windows_dir_syswow64}\\\\"
        else:
            return None

        prog = None
        
        if arch == Arch.X86_64:
            prog = random.choice(default_spawnto_all)
        else:
            prog = random.choice(default_spawnto_only_sysnative)

        spawn_to = f"{windows_dir}\\{default_spawnto_opsec[prog]}"

        if prog == "dashost":
            spawn_to = f"{spawn_to}{util.generate_dashost_pid()}"
        elif prog == "dllhost":
            spawn_to = f"{spawn_to}{util.generate_dllhost_uuid()}"
        
        return spawn_to

    def Print(self) -> dict:
        template = {}
        template["Spawn64"] = self.spawn_x64
        template["Spawn86"] = self.spawn_x86
        if self.alloc:
            template["Alloc"] = self.alloc
        if self.execute:
            template["Execute"] = self.execute
        return template

class Demon(Base):
    def __init__(self,
                 sleep: int,
                 jitter: int,
                 xforwardedfor: str = None,
                 implant: Implant = None,
                 binary: Binary = None,
                 injection: Injection = None
                 ) -> None:
        self.sleep = None
        self.injection = None
        self.jitter = None
        self.xforwardedfor = None
        self.implant = None
        self.binary = None

        if sleep:
            self.sleep = sleep
        else:
            self.sleep = 10
        if jitter:
            self.jitter = jitter
        else:
            self.jitter = 15
        if xforwardedfor:
            self.xforwardedfor = xforwardedfor
        if implant:
            self.implant = implant
        if binary:
            self.binary = binary
        if injection:
            self.injection = injection
        else:
            self.injection = Injection(None, None)

    def Print(self) -> dict:
        template = {}
        template["Sleep"] = self.sleep
        template["Jitter"] = self.jitter
        if self.xforwardedfor:
            template["TrustXForwardedFor"] = self.xforwardedfor
        if self.implant:
            template["Implant"] = self.implant.Print()
        if self.binary:
            template["Binary"] = self.binary.Print()
        if self.injection:
            template["Injection"] = self.injection.Print()
        return template

class Service(Base):
    def __init__(self, 
                 endpoint: str, 
                 password: str
                 ) -> None:
        if endpoint and password:
            self.endpoint = endpoint
            self.password = password
    
    def Print(self) -> dict:
        template = {}
        template["Endpoint"] = self.endpoint
        template["Password"] = self.password
        return template