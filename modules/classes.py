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
                 proxy_type: str,
                 host: str, 
                 port: int, 
                 username = None, 
                 password = None) -> None:
        self.proxy_type = proxy_type
        self.host = host
        self.port = port
        self.username = None
        self.password = None
        if username and password:
            self.username = username
            self.password = password

    def Print(self) -> dict:
        template = {}
        if self.proxy_type in [ "http", "https" ]:
            template["Type"] = self.proxy_type
        else:
            template["Type"] = "http"
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
                 host_bind: str,
                 port_bind: int, 
                 port_conn: int = None,
                 methode: str = None,
                 killswitch: str = None,
                 workinghours: str = None,
                 secure: str = None,
                 host_rotation: str = None, 
                 user_agent: str = None, 
                 headers: list = None, 
                 host_header: str = None,
                 urls: list = None, 
                 cert: Cert = None, 
                 proxy: Proxy = None, 
                 response: Response = None) -> None:
        self.name = name
        self.hosts = hosts
        self.port_bind = port_bind
        self.host_bind = host_bind
        self.port_conn = None
        self.methode = None
        self.killswitch = None
        self.workinghours = None
        self.host_rotation = None
        self.secure = None
        self.user_agent = None
        self.headers = None
        self.host_header = None
        self.urls = None
        self.cert = None
        self.proxy = None
        self.reponse = None

        if port_conn:
            self.port_conn = port_conn
        if methode:
            self.methode = methode
        else:
            self.methode = "post"
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
        if host_header:
            self.host_header = host_header
        if urls:
            self.urls = urls
        else:
            self.urls = [ "/" ]
        if secure:
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
        template["PortBind"] = self.port_bind
        template["Hosts"] = self.hosts
        template["HostBind"] = self.host_bind
        if self.port_conn:
            template["PortConn"] = self.port_conn
        if self.methode:
            template["Methode"] = self.methode
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
        if self.host_header:
            template["HostHeader"] = self.host_header
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
                 CompileTime: str = None,
                 ImageSizeX64: int = None,
                 ImageSizeX86: int = None
                ) -> None:
        self.magicmzx64 = None
        self.magicmzx86 = None
        self.compiletime = None
        self.imagesizex64 = None
        self.imagesizex86 = None

        if MagicMzX64:
            self.magicmzx64 = MagicMzX64
        if MagicMzX86:
            self.magicmzx86 = MagicMzX86
        if CompileTime:
            self.compiletime = CompileTime
        if ImageSizeX64:
            self.imagesizex64 = ImageSizeX64
        if ImageSizeX86:
            self.imagesizex86 = ImageSizeX86

    def Print(self) -> str:
        template = {}
        if self.magicmzx64:
            template["MagicMzX64"] = self.magicmzx64
        if self.magicmzx86:
            template["MagicMzX86"] = self.magicmzx86
        if self.compiletime:
            template["CompileTime"] = self.compiletime
        if self.imagesizex64:
            template["ImageSizeX64"] = self.imagesizex64
        if self.imagesizex86:
            template["ImageSizeX86"] = self.imagesizex86
        return template
    
class Binary(Base):
    def __init__(self,
                 header: Header = None,
                 replace_strx64: dict = None,
                 replace_strx86: dict = None
                 ) -> None:
        self.header = None
        self.replace_strx64 = None
        self.replace_strx86 = None

        if header:
            self.header = header
        if replace_strx64:
            self.replace_strx64 = replace_strx64
        if replace_strx86:
            self.replace_strx86 = replace_strx86
            
    def ParseReplaceStrings(
        replacement_strings: dict
        ) -> str:
        ""

    def Print(self) -> str:
        template = {}
        if self.header:
            template["Header"] = self.header.Print()
        if self.replace_strx64:
            template["ReplaceStringX64"] = self.ParseReplaceStrings(self.replace_strx64)
        if self.replace_strx86:
            template["ReplaceStringX86"] = self.ParseReplaceStrings(self.replace_strx86)
        return template

class Injection(Base):
    ARCH_X86 = "x86"
    ARCH_X64 = "x64"
    ARCH_SYSWOW = "x86_64"

    def __init__(self, 
                 spawn_x64: str = None, 
                 spawn_x86: str = None,
                 sysnative: bool = False
                 ) -> None:
        self.sysnative_binary = None
        self.syswow_binary = None
        
        if spawn_x64:
            if sysnative:
                self.spawn_x64 = self.Random(Arch.X64)
            else:
                self.spawn_x64 = self.Random(Arch.X86_64)
        if spawn_x86:
            if sysnative:
                self.spawn_x86 = self.Random(Arch.X86)
            else:
                self.spawn_x86 = self.Random(Arch.X86)

    def Random(self, 
               arch: Arch
               ) -> str:
        if arch == Arch.X64 or arch == Arch.X86:
            windows_dir = f"{windows_dir_root}\\{windows_dir_sysnative}\\"
        elif arch == Arch.X86_64:
            windows_dir = f"{windows_dir_root}\\{windows_dir_syswow64}\\"
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
        if self.spawn_x64:
            template["Spawn64"] = self.spawn_x64
        if self.spawn_x86:
            template["Spawn86"] = self.spawn_x86
        return template
# implant: Implant = None,
class Demon(Base):
    def __init__(self,
                 sleep: int,
                 jitter: int,
                 indirectsyscall: bool = False,
                 stackduplication: bool = False,
                 sleepteq: str = None,
                 proxyloading: str = None,
                 amsietwpatching: str = None,
                 injection: Injection = None,
                 dotnetpipe: str = None,
                 binary: Binary = None,
                 xforwardedfor: str = None
                 ) -> None:
        self.sleep = None
        self.jitter = None
        self.indirectsyscall = None
        self.stackduplication = None
        self.sleepteq = None
        self.proxyloading = None
        self.amsietwpatching = None
        self.injection = None
        self.dotnetpipe = None
        self.xforwardedfor = None
        self.binary = None

        if sleep:
            self.sleep = sleep
        else:
            self.sleep = 10
        if jitter:
            self.jitter = jitter
        else:
            self.jitter = 15
        if indirectsyscall:
            self.indirectsyscall = indirectsyscall
        if stackduplication:
            self.stackduplication = stackduplication
        if sleepteq:
            if sleepteq in [ "WaitForSingleObject", "Foliage", "Ekko", "Zilean" ]:
                self.sleepteq = sleepteq
            else:   
                self.sleepteq = "WaitForSingleObject"
        if proxyloading:
            if proxyloading in [ "RtlRegisterWait", "RtlCreateTimer", "RtlQueueWorkItem" ]:
                self.proxyloading = proxyloading
            else:
                self.proxyloading = None
        if amsietwpatching in [ "HWBP" ]:
            if amsietwpatching is "HWBP":
                self.amsietwpatching = "Hardware breakpoints"
        if injection:
            self.injection = injection
        if dotnetpipe:
            self.dotnetpipe = dotnetpipe
        if binary:
            self.binary = binary
        if xforwardedfor:
            self.xforwardedfor = xforwardedfor

    def Print(self) -> dict:
        template = {}
        template["Sleep"] = self.sleep
        template["Jitter"] = self.jitter
        if self.indirectsyscall:
            template["IndirectSyscall"] = self.indirectsyscall
        if self.stackduplication:
            template["StackDuplication"] = self.stackduplication
        if self.sleepteq:
            template["SleepTechnique"] = self.sleepteq
        if self.proxyloading:
            template["ProxyLoading"] = self.proxyloading
        if self.amsietwpatching:
            template["AmsiEtwPatching"] = self.amsietwpatching
        if self.injection:
            template["Injection"] = self.injection.Print()
        if self.dotnetpipe:
            template["DotNetNamePipe"] = self.dotnetpipe
        if self.binary:
            template["Binary"] = self.binary.Print()
        if self.xforwardedfor:
            template["TrustXForwardedFor"] = self.xforwardedfor

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
