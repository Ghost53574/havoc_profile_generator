from .classes import Base

class Writer(Base):
    def __init__(self, 
                 filename: str = None
                 ) -> None:
        self.filename = filename

    def Write(self, 
              profile) -> None:
        teamserver = profile.get("Teamserver")
        operators  = profile.get("Operators")
        listeners  = profile.get("Listeners")
        service    = profile.get("Service")
        demon      = profile.get("Demon")

        teamserver_host = teamserver.get("Host")
        teamserver_port = teamserver.get("Port")
        
        build = teamserver["Build"]
        build_compiler64 = build.get("Compiler64")
        build_compiler86 = build.get("Compiler86")
        build_assembler  = build.get("Nasm")

        teamserver_block = f"""Teamserver {{
    Host = "{teamserver_host}"
    Port = "{teamserver_port}"

    Build {{
        Compiler64 = "{build_compiler64}"
        Compiler86 = "{build_compiler86}"
        Nasm = "{build_assembler}"
    }}
}}
"""
        operator_block = "Operators {"
        for operator in operators:
            operator_user = operator
            operator_pass = operators[operator_user]["Password"]
            operator_block += f"""
    user "{operator_user}" {{
        Password = "{operator_pass}"
    }}
"""
        operator_block += "}\n"

        listener_block = "Listeners {"
        for listener in listeners:
            for listener_type in listener.keys():
                listener_name = listener[listener_type].get("Name")

                if listener_type == "Http":
                    listener_port_bind = listener[listener_type].get("PortBind")
                    listener_conn_bind = listener[listener_type].get("ConnBind")
                    listener_hosts = listener[listener_type].get("Hosts")
                    listener_bind  = listener[listener_type].get("HostBind")
                    listener_killdate = listener[listener_type].get("KillDate")
                    listener_workinghours = listener[listener_type].get("WorkingHours")
                    listener_rotation = listener[listener_type].get("HostRotation")
                    listener_user_agent = listener[listener_type].get("UserAgent")
                    listener_secure = listener[listener_type].get("Secure")
                    listener_headers = listener[listener_type].get("Headers")
                    listener_urls = listener[listener_type].get("Urls")
                    listener_cert = listener[listener_type].get("Cert")
                    listener_proxy = listener[listener_type].get("Proxy")
                    listener_response = listener[listener_type].get("Response")
                    listener_response = listener_response.get("Headers")
                    listener_block += f'''
    {listener_type} {{
        Name         = "{listener_name}"
        KillDate     = "{listener_killdate}"
        WorkingHours = "{listener_workinghours}"
        Hosts        =  {listener_hosts}
        HostBind     = "{listener_bind}"
        HostRotation = "{listener_rotation}"
        PortBind     =  {listener_port_bind}
        PortConn     =  {listener_conn_bind}
        Secure       =  {listener_secure}
        UserAgent    = "{listener_user_agent}"
        Uris         =  {listener_urls}
        Headers      =  {listener_headers}
'''
                    if listener_cert:
                        listener_block += f'''
        Cert {{
            Cert = "{listener_cert["Cert"]}"
            Key  = "{listener_cert["Key"]}"
        }}
'''
                    if listener_proxy:
                        listener_block += f'''
        Proxy {{
            Host     = "{listener_proxy["Host"]}"
            Port     = {listener_proxy["Port"]}
            Username = "{listener_proxy["Username"]}"
            Password = "{listener_proxy["Password"]}"
        }}
'''
                    listener_block += f'''
        Response {{
            Headers  = {listener_response}
        }}
    }}
'''
                elif listener_type == "Smb":
                    listener_smb_pipename = listener[listener_type].get("Pipename")
                    listener_smb_killdate = listener[listener_type].get("KillDate")
                    listener_smb_workinghours = listener[listener_type].get("WorkingHours")
                    listener_block += f'''
    Smb {{
        Name         = "{listener_name}"
        PipeName     = "{listener_smb_pipename}"
'''
                    if listener_smb_killdate:
                        listener_block =+ f'KillDate     = "{listener_smb_killdate}"'
                    if listener_smb_workinghours:
                        listener_block += f'WorkingHours = "{listener_smb_workinghours}"'
                    listener_block += "    }\n"
                elif listener_type == "External":
                    listener_ext_endpoint = listener[listener_type].get("Endpoint")
                    listener_block += f'''
    External {{
        Name      = "{listener_name}"
        Endpoint  = "{listener_ext_endpoint}"
    }}
'''
        listener_block += "}\n"

        if service:
            service_endpoint = service["Endpoint"]
            service_password = service["Password"]

            if service_endpoint and service_password:
                service_block = f"""Service {{
    Endpoint = "{service_endpoint}"
    Password = "{service_password}"
}}
"""
            else:
                service_block = None
        else:
            service_block = None
        # Fix representation of Sleep and other values in the Demon build profile
        demon_sleep = demon["Sleep"]
        demon_jitter = demon["Jitter"]
        demon_xforwardedfor = demon.get("TrustXForwardedFor")
        demon_implant = demon.get("Implant")
        if demon_implant:
            demon_implant_sleepmask = demon_implant.get("SleepMask")
            demon_implant_sleepteq  = demon_implant.get("SleepMaskTechnique")
        demon_binary = demon.get("Binary")
        if demon_binary:
            demon_binary_magicmzx64 = demon_binary["Header"].get("MagicMzX64")
            demon_binary_magicmzx86 = demon_binary["Header"].get("MagicMzX86")
        demon_injection = demon["Injection"]
        injection_spawn64 = demon_injection["Spawn64"]
        injection_spawn32 = demon_injection["Spawn86"]
        demon_block = f"""Demon {{
    Sleep  = {demon_sleep}
    Jitter = {demon_jitter}"""
        if demon_xforwardedfor:
            demon_block += f"""
    TrustXForwardedFor = "{demon_xforwardedfor}" 
"""
        if demon_implant:
            demon_block += f"""
    Implant {{"""
            if demon_implant_sleepmask:
                demon_block += f"""
        SleepMask = {demon_implant_sleepmask}"""
            if demon_implant_sleepteq:
                demon_block += f"""
        SleepMaskTechnique = "{demon_implant_sleepteq}" """
            demon_block += f"""
    }}
"""
        if demon_binary and (demon_binary_magicmzx64 or demon_binary_magicmzx86):
            demon_block += f"""
    Binary {{
        Header {{
"""
            if demon_binary_magicmzx64:
                demon_block += f"            MagicMzX64 = \"{demon_binary_magicmzx64}\""
            if demon_binary_magicmzx86:
                demon_block += f"            MagicMzX64 = \"{demon_binary_magicmzx86}\""
            demon_block += f"""
        }}
    }}
"""
        demon_block += f"""
    Injection {{
        Spawn64 = "{injection_spawn64}"
        Spawn32 = "{injection_spawn32}" """
        demon_block += f"""
    }}
}}"""
        profile_block = teamserver_block + operator_block + listener_block
        if service_block:
            profile_block += service_block
        profile_block += demon_block
        profile_block = profile_block.replace("\'", "\"")
        
        if self.filename:
            with open(self.filename, 'w') as f:
                f.write(profile_block)
        else:
            print(profile_block)
