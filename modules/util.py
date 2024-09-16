import os
import re
import uuid
import math
import json
import random
import datetime
import struct
import fcntl
import socket
from OpenSSL import crypto, SSL
from faker import Factory

import mpp
from mpp.options import Option
from mpp.blocks import Block
from mpp.constants import INVALID_OPTION, INVALID_TERMINATION_STATEMENT, INVALID_STATEMENT, INVALID_BLOCK, \
    DATA_TRANSFORM_BLOCKS, PROFILE, TERMINATION_STATEMENTS
from mpp.statements import Statement, HeaderParameter, StringReplace

Faker = Factory.create
fake = Faker()

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
INFO = '\033[92m'
WARN = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

MAX_WEEKS=52

profile_dir = "profiles"
search_path = os.environ['PATH']
windows_dir_root = "C:\\\\Windows"
windows_dir_sysnative = "\\System32"
windows_dir_syswow64 = "\\SysWow64"

ssl_cert_file = "havoc.crt"
ssl_key_file = "havoc.key"

loaded_profiles_data = {}

def str_to_bool(value):
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def generate_dashost_pid() -> str:
    id = uuid.uuid4().urn[9:].split("-")
    pid = f"{id[0]}-{id[1]}-{id[2]}{id[3]}{id[4]}{random.choice(range(0,9))}"
    return pid

def generate_dllhost_uuid() -> str:
    id = uuid.uuid4().urn[9:]
    return "{" + f"{id}" + "}"

def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range") 

# based on _ilove2pwn's https://gist.github.com/realoriginal/d9178c9b071707fec2d6de89a63e4709
def generate_pipename(
        pid: int = None, 
        tid: int = None, 
        proc: int = None) -> str:
    """
    Generates a named pipe.
    """
    if not pid:
        pid = random.choice(range(2048, 9999))
    if not tid:
        tid = random.choice(range(3096, 8192))
    PipeList = {
        'winsock': 'Winsock2\\\\CatalogChangeListener-$#-0',
        'mojo': f'mojo.{pid}.{tid}.####################',
        'crashpad': f'crashpad_{pid}_@@@@@@@@@@@@@@@@',
        'chromesync': f'chrome.sync.{pid}.{tid}.########',
        'guid': f'{generate_dllhost_uuid()}',
        'chrome': f'chrome.#####.####.#########',
        'discord': f'discord-ipc-##',
        'shellex': f'ShellEx_#####',
        'tcppipe': f'tcppipe.#####-#####-######',
        'ntsvcs': f'netsvcs####',
        'trkwks': f'trkwks####',
        'pshost': f'PShost.##################.{pid}.DefaultAppDomain.powershell',
        'gecko': f'gecko.{pid}.{tid}.##################'
    }
    if not proc:
        PipeName = PipeList[ get_nth_key(PipeList, random.randint( 0, len( PipeList ) - 1 )) ]
    else:
        PipeName = PipeList.get(proc)

    # Loop through and generate a hex character
    for Idx in re.findall( r'\$', PipeName ):
        PipeName = re.sub( r'\$', f'{random.randint( 0, 255 ):x}', PipeName, count = 1 );

    # Loop through and generate a new integer
    for Idx in re.findall( r'#', PipeName ):
        PipeName = re.sub( r'#', f'{random.randint( 0, 9 )}', PipeName, count = 1 );

    # Loop through and generate a character( uppercase )
    for Idx in re.findall( r'@', PipeName ):
        PipeName = re.sub( r'@', f'{chr(random.randint( 65, 90 ))}', PipeName, count = 1 );

    # Loop through and generate a character( lowercase )
    for Idx in re.findall( r'!', PipeName ):
        PipeName = re.sub( r'!', f'{chr(random.randint( 97, 122 ))}', PipeName, count = 1 );

    # return the pipename
    return PipeName

def generate_killdate() -> str:
    return fake.date_time_between_dates(
        datetime_start=datetime.datetime.now(),
        datetime_end=datetime.datetime.now() + datetime.timedelta(weeks=MAX_WEEKS))

def generate_workinghours(start: str = None,
                          end: str = None
                          ) -> str:
    if not start:
        start = "0:00"
    if not end:
        end = "23:59"
    return f"{start}-{end}"

def get_random_port(
        port: int = None, 
        min_port: int = None, 
        max_port: int = None
        ) -> int:
    if not port and (min_port and max_port):
        return random.choice(range(min_port, max_port))
    elif not port and (min_port or max_port):
        if not min_port:
            min_port = 1024
        if not max_port:
            max_port = 65535
        return random.choice(range(min_port, max_port))
    elif not port:
        return random.choice(range(1024, 65535))
    else:
        return port
    
def load_profiles() -> tuple[list, dict]:
    if not os.path.isdir(profile_dir):
        return None
    for _, _, files in os.walk(profile_dir):
        loaded_profiles = files
    loaded_profiles_data = {}
    temp = []
    for f in loaded_profiles:
        if os.path.isfile(f"{profile_dir}/{f}"):
            name = f.split(".")[0]
            profile_data = ""
            with open(f"{profile_dir}/{f}", "r") as fe:
                profile_data = json.loads(fe.read())
            temp.append(name)
            loaded_profiles_data[name] = profile_data
    return (temp, loaded_profiles_data)

def get_cs_profiles(path) -> dict:
    temp = []
    cs_profiles = {}
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(".profile"):
                temp.append(os.path.join(path, file))
    for file in temp:
        cs_profile = mpp.MalleableProfile(profile=file)
        cs_profiles[file] = cs_profile.profile
    return cs_profiles

def structure_list(entries: list) -> list:
    temp = "[ "
    etnries_len = len(entries)
    for i, entry in enumerate(entries):
        e = entry.replace("\\","")
        if not i == etnries_len - 1:
            temp += f"\"{e}\", "
        else:
            temp += f"\"{e}\""
    temp += " ]"
    return temp

def parse_cs_profile(profile: dict, 
                     verb: str = "any"
                     ) -> str:
    sleep = None
    jitter = None
    user_agent = None
    pipename = None
    spawnx86 = None
    spawnx64 = None

    config_uris = []
    config_headers = []
    server_uris = []
    client_headers = []
    server_headers = []

    for kv in profile.keys():
        obj = profile[kv]

        if type(obj) is Option:
            if obj.option == "sleeptime":
                sleep = math.floor(int(obj.value) / 1000)
            elif obj.option == "jitter":
                jitter = int(obj.value)
            elif obj.option == "useragent":
                user_agent = obj.value
            elif obj.option == "spawnto_x86":
                spawnx86 = obj.option
            elif obj.option == "spawnto_x64":
                spawnx64 = obj.option
            elif obj.option == "pipename":
                pipename = obj.value

        elif type(obj) is Block:
            name = profile[kv].name
            data = profile[kv].data

            for d in data:
                if name == "dns-beacon":
                    continue
                elif name == "http-config":
                    if type(data) is Option:
                        if data.option == "headers":
                            vals = data.value.split(",")
                            config_headers = vals
                        elif data.option == "uri":
                            vals = data.value.split(" ")
                            for val in vals:
                                config_uris.append(val)
                elif name == "http-get" and (verb == "any" or verb == "get"):
                    if type(data) is list:
                        for d in data:
                            if type(d) is Option:
                                if d.option == "uri":
                                    vals = d.value.split(" ")
                                    for val in vals:
                                        server_uris.append(val)
                            elif type(d) is Block:
                                if d.name == "client":
                                    for c in d.data:
                                        c_type = c.statement
                                        c_key  = c.key
                                        c_val  = c.value
                                        if c_type == "header":
                                            client_headers.append(f"{c_key}: {c_val}")
                                elif d.name == "server":
                                    for c in d.data:
                                        c_type = c.statement
                                        c_key  = c.key
                                        c_val  = c.value
                                        if c_type == "header":
                                            server_headers.append(f"{c_key}: {c_val}")
                elif name == "http-post" and (verb == "any" or "post"):
                    if type(data) is list:
                        for d in data:
                            if type(d) is Option:
                                if d.option == "uri":
                                    server_uris.append(d.value)
                            elif type(d) is Block:
                                if d.name == "client":
                                    for c in d.data:
                                        c_type = c.statement
                                        c_key  = c.key
                                        c_val  = c.value
                                        if c_type == "header":
                                            client_headers.append(f"{c_key}: {c_val}")
                                elif d.name == "server":
                                    for c in d.data:
                                        c_type = c.statement
                                        c_key  = c.key
                                        c_val  = c.value
                                        if c_type == "header":
                                            server_headers.append(f"{c_key}: {c_val}")
                elif name == "process-inject":
                    if type(data) is list:
                        for d in data:
                            if type(d) is Option:
                                pass
                            elif type(d) is Statement:
                                pass
                elif name == "post-ex":
                    if type(data) is list and (not spawnx64 and not spawnx86):
                        for d in data:
                            if d.option == "spawnto_x86":
                                if d.value:
                                    spawnx86 = d.value
                            elif d.option == "spawnto_x64":
                                if d.value:
                                    spawnx64 = d.value
                            elif d.option == "pipename":
                                if not pipename:
                                    pipename = d.value
        else:
            continue

    config_headers = list(dict.fromkeys(config_headers))
    client_headers = list(dict.fromkeys(client_headers))
    server_headers = list(dict.fromkeys(server_headers))

    config_uris = list(dict.fromkeys(config_uris))
    server_uris = list(dict.fromkeys(server_uris))

    server_uris = structure_list(config_uris + server_uris)
    client_headers = structure_list(config_headers + client_headers)
    server_headers = structure_list(config_headers + server_headers)

    if pipename:
        pipename = pipename[:-2]

    if spawnx86:
        spawnx86_split = spawnx86.split("\\")
        if spawnx86_split[0] == "%windir%" and spawnx86_split[2] == "sysnative":
            spawnx86 = f"{windows_dir_root}\\{windows_dir_sysnative}\\\\{spawnx86_split[4]}"
        elif spawnx86_split[0] == "%windir%" and spawnx86_split[2] == "syswow64":
            spawnx86 = f"{windows_dir_root}\\{windows_dir_syswow64}\\\\{spawnx86_split[4]}"
    if spawnx64:
        spawnx64_split = spawnx64.split("\\")
        if spawnx64_split[0] == "%windir%" and spawnx64_split[2] == "sysnative":
            spawnx64 = f"{windows_dir_root}\\{windows_dir_sysnative}\\\\{spawnx64_split[4]}"
        elif spawnx64_split[0] == "%windir%" and spawnx64_split[2] == "syswow64":
            spawnx64 = f"{windows_dir_root}\\{windows_dir_syswow64}\\\\{spawnx64_split[4]}"

    parsed_profile = f"""{{
    "Request": {server_uris},
    "Response": {server_headers},
    "Headers": {client_headers},
    "User Agent": "{user_agent}",
    "Pipename": "{pipename}",
    "Sleep": "{sleep}",
    "Jitter": "{jitter}",
    "Spawnx86": "{spawnx86}",
    "Spawnx64": "{spawnx64}"
}}"""
    return json.loads(parsed_profile)

def create_self_signed_cert(
        rsa_key_len: int = 1024,
        san_c: str = "UK",
        san_st: str = "London",
        san_l: str = "London",
        san_o: str = "Dummy Company Ltd",
        san_ou: str = "Dummy Company Ltd",
        san_cn: str = "dummy.domain"
):
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, rsa_key_len)

    cert = crypto.X509()
    cert.get_subject().C = san_c
    cert.get_subject().ST = san_st
    cert.get_subject().L = san_l
    cert.get_subject().O = san_o
    cert.get_subject().OU = san_ou
    cert.get_subject().CN = san_cn
    cert.set_serial_number(1000)
    cert.set_version(3)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    open(ssl_cert_file, "wt").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(ssl_key_file, "wt").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

def Find(name, 
         _search_path = None):
    if _search_path:
        paths = _search_path
    else:
        paths = search_path.split(":")
    for path in paths: 
        for root, _, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

def print_good(message):
    print(f"{INFO}[+] {message}{ENDC}")

def print_warn(message):
    print(f"{WARN}[!] {message}{ENDC}")

def print_fail(message):
    raise Exception(f"{FAIL}[x] {message}{ENDC}")
