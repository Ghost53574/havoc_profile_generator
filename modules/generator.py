from . import classes
from . import util
from . import enum

from faker import Factory
import random
import json

Faker = Factory.create
fake = Faker()

Teamserver = classes.Teamserver
Build      = classes.Build
Operators  = classes.Operators
Listeners  = classes.Listeners
Http_Listener = classes.Http_Listener
Smb_Listener = classes.Smb_Listener
External_Listener = classes.External_Listener
Cert       = classes.Cert
Proxy      = classes.Proxy
Response   = classes.Response
Demon      = classes.Demon
Injection  = classes.Injection
Implant    = classes.Implant
Binary     = classes.Binary
Header     = classes.Header
Service    = classes.Service

Arch = enum.Arch
AllocEnum = enum.AllocEnum
ExecuteEnum = enum.ExecuteEnum

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

class Generator(Teamserver, Operators, Listeners, Demon, Service):
    def __init__(self, 
                 teamserver: Teamserver, 
                 operators: Operators, 
                 listeners: Listeners, 
                 demon: Demon, 
                 service: Service = None
                 ) -> None:
        self.service = None

        if teamserver:
            self.teamserver = teamserver
        else:
            util.print_fail("Need a teamserver config")
        if operators:
            self.operators = operators
        else:
            util.print_fail("Need at least one operator config")
        if listeners:
            self.listeners = listeners
        else:
            util.print_fail("Need a listener config")
        if Service:
            self.service = service
        if demon:
            self.demon = demon
        else:
            util.print_fail("Need a demon config")

    def Print(self) -> dict:
        template = {}
        if self.teamserver:
            template["Teamserver"] = self.teamserver.Print()
        else:
            util.print_fail("Need a Teamserver config")
        if self.operators:
            template["Operators"] = self.operators.Print()
        else:
            util.print_fail("Need at least one Operator config")
        if self.listeners:
            template["Listeners"] = self.listeners.Print()
        else:
            util.print_fail("Need a Listeners block in config")
        if self.service:
            template["Service"] = self.service.Print()
        if self.demon:
            template["Demon"] = self.demon.Print()
        else:
            util.print_fail("Need a Demon block in config")
        return template

    def Get(self) -> object:
        return self
    
class Profile():
    def __init__(self,
                 quiet: bool,
                 profile_names: list, 
                 profiles: list,
                 profile: str = None, 
                 config: str = None,
                 sysnative: bool = False,
                 evasion: bool = False,
                 min_port: str = None,
                 max_port: str = None,
                 host: str = None, 
                 port: int = None, 
                 hosts: list = None, 
                 arch: Arch = None,
                 extra_listeners: list = None
                 ) -> object:
        self.profile = None
        self.config = None

        operator_block = None
        listeners_block = None
        service_block = None
        demon_block = None

        if not quiet:
            util.print_good("Generating profile")

        if profile:
            self.profile = profile
        else:
            self.profile = random.choice(profile_names)

        if config:
            self.config = json.loads("".join(config))
            teamserver_host = self.config.get("ts_host")
            teamserver_port = self.config.get("ts_port")
            build_compiler_x64 = self.config.get("compiler_x64")
            build_compiler_x86 = self.config.get("compiler_x86")
            build_assembler = self.config.get("assembler")

            operator_block = self.config.get("users")
            listeners_block = self.config.get("listeners")
            service_block = self.config.get("service")
            demon_block = self.config.get("demon")
        else:
            teamserver_host = localhost
            teamserver_port = util.get_random_port(
                min_port=int(min_port), 
                max_port=int(max_port))
            build_compiler_x64 = default_compiler_x64
            build_compiler_x86 = default_compiler_x86
            build_assembler = default_assembler

        if not teamserver_host and not teamserver_port:
            teamserver_host = localhost
            teamserver_port = default_port
        elif not teamserver_host:
            teamserver_host = localhost
        elif not teamserver_port:
            teamserver_port = default_port
        if not build_compiler_x64 and not build_compiler_x86:
            build_compiler_x64 = default_compiler_x64
            build_compiler_x86 = default_compiler_x86
        elif build_compiler_x86 and not build_compiler_x64:
            build_compiler_x64 = default_compiler_x64
        elif build_compiler_x64 and not build_compiler_x86:
            build_compiler_x86 = default_compiler_x86

        if not build_assembler:
            build_assembler = default_assembler

        build = Build(build_compiler_x64, build_compiler_x86, build_assembler)
        teamserver = Teamserver(teamserver_host, teamserver_port, build)
        if not quiet:
            util.print_good("Teamserver built")

        if not operator_block:
            operators = Operators()
            random_uesrname = fake.user_name()
            random_password = fake.password()
            operators.Add_User(random_uesrname, random_password)
        else:
            operators = Operators()
            for op in operator_block:
                operator_user = dict(op).keys()
                for key in operator_user:
                    username = key
                    password = dict(op)[key]
                    operators.Add_User(username, password)
        if not quiet:
            util.print_good("Generated Operators")

        if not profile or profile == "any":
            selected_profile = random.choice(profile_names)
        elif profile == "none":
            selected_profile = None
            profile_data = None
        else:
            selected_profile = profile

        if selected_profile:
            profile_data = profiles[selected_profile]
        else:
            util.print_warn("No profile selected, using config data")

        profile_user_agent = None
        profile_request = None
        profile_response = None
        profile_headers = None
        profile_sleep = None
        profile_jitter = None
        profile_spawnx64 = None
        profile_spawnx86 = None
        profile_alloc = None
        profile_execute = None
        profile_sleep_teq = None
        profile_pipename = None
        profile_xforwardedfor = None

        if profile_data:
            profile_user_agent = profile_data.get("User Agent")
            profile_request = profile_data.get("Request")
            profile_response = profile_data.get("Response")
            profile_headers = profile_data.get("Headers")
            profile_sleep = profile_data.get("Sleep")
            profile_jitter = profile_data.get("Jitter")
            profile_xforwardedfor = profile_data.get("TrustXForwardedFor")
            profile_spawnx64 = profile_data.get("Spawnx64")
            profile_spawnx86 = profile_data.get("Spawnx86")
            profile_sleep_teq = profile_data.get("SleepTechnique")
            profile_alloc = profile_data.get("Alloc")
            profile_execute = profile_data.get("Execute")
            profile_pipename = profile_data.get("Pipename")

        listeners = Listeners()

        if not listeners_block:
            if not quiet:
                util.print_good("Loading random listeners")
            if not hosts:
                temp = []
                number_hosts = random.choice(range(1, 20))
                for i in range(number_hosts):
                    temp.append(fake.ipv4())
                hosts = temp
            else:
                temp = []
                try:
                    number_hosts = len(hosts.split(","))
                except:
                    number_hosts = 1
                if number_hosts > 1:
                    for host in hosts.split(","):
                        temp.append(host)
                else:
                    temp = [ hosts ]
                hosts = temp
            if not port:
                port = util.get_random_port()
            if not host:
                host = all_interfaces
            name = "Http"
            user_agent = None
            if profile_user_agent:
                user_agent = profile_user_agent
            else:
                user_agent = fake.user_agent()
            headers = None
            if profile_headers:
                headers = profile_headers
            else:
                headers = default_headers
            urls = None
            if profile_request:
                urls = profile_request
            else:
                urls = default_urls
            
            response = None
            if profile_response:
                response = profile_response
            http_listener = Http_Listener(name=name,
                                          hosts=hosts,
                                          port=port,
                                          host_bind=host,
                                          killswitch=None,
                                          workinghours=None,
                                          secure="false",
                                          host_rotation=None,
                                          user_agent=user_agent,
                                          headers=headers,
                                          urls=urls,
                                          cert=None,
                                          proxy=None,
                                          response=response)
            listeners.Add_Http_Listener(http_listener)
            name = "Agent Listener - HTTP/s"
            https_listener = Http_Listener(name=name,
                                          hosts=hosts,
                                          port="443",
                                          host_bind=host,
                                          killswitch=None,
                                          workinghours=None,
                                          secure="true",
                                          host_rotation=None,
                                          user_agent=user_agent,
                                          headers=headers,
                                          urls=urls,
                                          cert=None,
                                          proxy=None,
                                          response=response)
            listeners.Add_Http_Listener(https_listener)
            smb_listener = Smb_Listener("Pivot - Smb")
            listeners.Add_Smb_Listener(smb_listener)
        else:
            for listener in listeners_block:
                for listener_type in listener.keys():
                    listener_name = listener[listener_type].get("name")
                    if not listener_name:
                        listener_name = fake.user_name()
                    if listener_type == "http":
                        listener_hosts = listener[listener_type].get("hosts")
                        if hosts:
                            temp = []
                            try:
                                number_hosts = len(hosts.split(","))
                            except:
                                number_hosts = 1
                            if number_hosts > 1:
                                for _host in hosts.split(","):
                                    temp.append(_host)
                            else:
                                temp = [ hosts ]
                            listener_hosts = temp
                        elif not listener_hosts and not hosts:
                                temp = []
                                number_hosts = random.choice(range(1, 20))
                                for i in range(number_hosts):
                                    temp.append(fake.ipv4())
                                listener_hosts = temp
                        
                        listener_bind = listener[listener_type].get("bind")
                        if not listener_bind and not host:
                            listener_bind = all_interfaces
                        elif listener_bind and host:
                            listener_bind = host
                        elif not listener_bind and host:
                            listener_bind = host
                        listener_port = listener[listener_type].get("port")
                        if not listener_port:
                            listener_port = util.get_random_port()
                        listener_rotation = listener[listener_type].get("rotation")
                        if not listener_rotation:
                            listener_rotation = random.choice([ "random", "round-robin" ])
                        listener_user_agent = listener[listener_type].get("user_agent")
                        if not listener_user_agent:
                            listener_user_agent = fake.user_agent()
                        listener_headers = listener[listener_type].get("headers")
                        if profile_headers and not listener_headers:
                            listener_headers = profile_headers
                        listener_urls = listener[listener_type].get("urls")
                        if profile_request and not listener_urls:
                            listener_urls = profile_request
                        listener_secure = listener[listener_type].get("secure")
                        if not listener_secure:
                            listener_secure = random.choice([ "true", "false" ])
                        listener_killswitch = listener[listener_type].get("killswitch")
                        if not listener_killswitch:
                            listener_killswitch = util.generate_killdate()
                        listener_workinghours = listener[listener_type].get("workinghours")
                        if not listener_workinghours:
                            listener_workinghours = util.generate_workinghours(None, None)
                        listener_cert = listener[listener_type].get("cert")
                        if not listener_cert:
                            listener_cert = None
                        else:
                            listener_cert_cert = listener_cert.get("cert")
                            listener_cert_key  = listener_cert.get("key")
                            listener_cert = Cert(listener_cert_cert, listener_cert_key)
                        listener_proxy = listener[listener_type].get("proxy")
                        if not listener_proxy:
                            listener_proxy = None
                        else:
                            listener_proxy_host = listener_proxy.get("host")
                            listener_proxy_port = listener_proxy.get("port")
                            listener_proxy_user = listener_proxy.get("user")
                            listener_proxy_pass = listener_proxy.get("pass")
                            listener_proxy = Proxy(listener_proxy_host, listener_proxy_port, 
                                                   listener_proxy_user, listener_proxy_pass)
                        listener_response = listener[listener_type].get("response")
                        if profile_response and not listener_response:
                            listener_response = profile_response
                        response = Response(listener_response)
                        listeners.Add_Http_Listener(Http_Listener(
                            name=listener_name, 
                            hosts=listener_hosts,
                            port=listener_port,
                            host_bind=listener_bind, 
                            host_rotation=listener_rotation,
                            killswitch=listener_killswitch,
                            workinghours=listener_workinghours,
                            user_agent=listener_user_agent, 
                            headers=listener_headers,
                            urls=listener_urls, 
                            secure=listener_secure,
                            cert=listener_cert,
                            proxy=listener_proxy,
                            response=response))
                    elif listener_type == "smb":
                        listener_pipename = listener[listener_type].get("pipename")
                        if not listener_pipename and (not profile_pipename or profile_pipename == "None"):
                            listener_pipename = util.generate_pipename(random.choice(default_pipenames))
                        elif not listener_pipename and profile_pipename:
                            listener_pipename = util.generate_pipename(profile_pipename)
                        listener_killdate = listener[listener_type].get("killdate")
                        listener_workinghours = listener[listener_type].get("workinghours")
                        listeners.Add_Smb_Listener(Smb_Listener(listener_name, 
                                                                listener_pipename,
                                                                listener_killdate,
                                                                listener_workinghours))
                    elif listener_type == "external":
                        listener_endpoint = listener[listener_type].get("endpoint")
                        if not listener_endpoint:
                            listener_endpoint = None
                        listeners.Add_External_Listener(External_Listener(listener_name, listener_endpoint))

        if not service_block:
            service = None
        else:
            if not quiet:
                util.print_good("Creating optional service block")
            service_endpoint = dict(service_block).get("endpoint")
            service_password = dict(service_block).get("password")
            if not service_endpoint:
                service_endpoint = None
                service_password = None
            else:
                if not service_password:
                    service_password = fake.password()
            if not service_endpoint and not service_password:
                service = None
            else:
                service = Service(endpoint=service_endpoint, password=service_password)

        if not quiet:
            util.print_good("Creating a demon :)")
        if not demon_block:
            injection = Injection(arch=arch, sysnative=sysnative)
            sleep = random.choice(range(12, 60))
            jitter = random.choice(range(5, 70))
            demon = Demon(sleep=sleep, jitter=jitter, injection=injection)
        else:
            demon_sleep = dict(demon_block).get("sleep")
            if not demon_sleep and not profile_sleep:
                demon_sleep = random.choice(range(12, 60))
            elif not demon_sleep and profile_sleep:
                demon_sleep = profile_sleep
            demon_jitter = dict(demon_block).get("jitter")
            if not demon_jitter and not profile_jitter:
                demon_jitter = random.choice(range(5, 70))
            elif not demon_jitter and profile_jitter:
                demon_jitter = profile_jitter
            demon_xforwardedfor = dict(demon_block).get("trustxforwardedfor")
            if not demon_xforwardedfor and not profile_xforwardedfor:
                demon_xforwardedfor = None
            elif not demon_xforwardedfor and profile_xforwardedfor:
                demon_xforwardedfor = profile_xforwardedfor
            demon_implant = dict(demon_block).get("implant")
            if not demon_implant and not profile_sleep_teq:
                demon_implant = None
            elif not demon_implant and profile_sleep_teq:
                demon_implant = Implant("1", profile_sleep_teq)
            else:
                demon_implant_sleepmask = dict(demon_implant).get("sleep_mask")
                demon_implant_sleepteq  = dict(demon_implant).get("sleep_technique")
                demon_implant = Implant(
                    sleep_mask=demon_implant_sleepmask,
                    sleep_teq=demon_implant_sleepteq)
            demon_binary = dict(demon_block).get("binary")
            if not demon_binary:
                demon_binary = None
            if demon_binary:
                demon_binary_header = demon_binary.get("header")
                if demon_binary_header:
                    demon_binary_magicmzx64 = demon_binary_header.get("magicmzx64")
                    demon_binary_magicmzx86 = demon_binary_header.get("magicmzx86")
                    if demon_binary_magicmzx64 or demon_binary_magicmzx86:
                        demon_binary = Binary(
                                        Header(
                                        MagicMzX64=demon_binary_magicmzx64,
                                        MagicMzX86=demon_binary_magicmzx86
                                        ))
                    if type(demon_binary) is not Binary:
                        demon_binary = None
            injection = dict(demon_block).get("injection")

            if not injection:
                demon_alloc = None
                demon_execute = None
                demon_spawn32 = None
                demon_spawn64 = None

                if profile_spawnx86 and not profile_spawnx86 == "None":
                    demon_spawn32 = profile_spawnx86
                if profile_spawnx64 and not profile_spawnx64 == "None":
                    demon_spawn64 = profile_spawnx64
            else:
                demon_spawn32 = injection.get("spawn32")
                if not demon_spawn32 and not profile_spawnx86:
                    demon_spawn32 = None
                elif not demon_spawn32 and profile_spawnx86 != "None":
                    demon_spawn32_split = profile_spawnx86.split("\\")
                    demon_spawn32 = f"{demon_spawn32_split[0]}\\\\{demon_spawn32_split[1]}\\\\{demon_spawn32_split[2]}\\\\{demon_spawn32_split[3]}"
                else:
                    demon_spawn32 = None
                demon_spawn64 = injection.get("spawn64")
                if not demon_spawn64 and not profile_spawnx64:
                    demon_spawn64 = None
                elif not demon_spawn64 and profile_spawnx64 != "None":
                    demon_spawn64_split = profile_spawnx64.split("\\")
                    demon_spawn64 = f"{demon_spawn64_split[0]}\\\\{demon_spawn64_split[1]}\\\\{demon_spawn64_split[2]}\\\\{demon_spawn64_split[3]}"
                else:
                    demon_spawn64 = None

                demon_alloc = injection.get("alloc")
                if not demon_alloc and not profile_alloc:
                    demon_alloc = None
                elif not demon_alloc and profile_alloc:
                    demon_alloc = profile_alloc
                demon_execute = injection.get("execute")
                if not demon_execute and not profile_execute:
                    demon_execute = None
                elif not demon_execute and profile_execute:
                    demon_execute = profile_execute

                if demon_alloc:
                    demon_alloc = AllocEnum(demon_alloc)
                if demon_execute:
                    demon_execute = ExecuteEnum(demon_execute)

            demon_injection = Injection(spawn_x64=demon_spawn64,
                                        spawn_x86=demon_spawn32,
                                        alloc=demon_alloc,
                                        execute=demon_execute,
                                        arch=arch,
                                        sysnative=sysnative)
            demon = Demon(sleep=demon_sleep,
                          jitter=demon_jitter,
                          xforwardedfor=demon_xforwardedfor,
                          implant=demon_implant,
                          binary=demon_binary,
                          injection=demon_injection)
        
        self.generator = Generator(teamserver=teamserver, 
                                   operators=operators, 
                                   listeners=listeners, 
                                   demon=demon,
                                   service=service)
        if self.generator:
            if not quiet:
                util.print_good("Generator complete")
        else:
            util.print_fail("Generator failed to compile :(")

    def Print(self) -> dict:
        return self.generator.Print()
    
    def Get(self) -> object:
        return self.generator