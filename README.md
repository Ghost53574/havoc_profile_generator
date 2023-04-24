Havoc C2 profile generator is a python3 script that generates profiles to be used with the Havoc C2 Framework.

There are six built in profiles copied from https://github.com/xx0hcd/Malleable-C2-Profiles as a base. You can
now parse Cobalt Strike profiles using this tool (I only need to add a couple of additional checks, but it works).

The idea of the this generator was to make it extensable and to separate the parts of a profile out to make easy 
randomization if need be. The randomization works by leaving creating a block but leaving it empty as such:
```txt
{
    "ts_host": "127.0.0.1",
    "ts_port": 8888,
    "listeners": [
        { 
            "http": {
                "name": "Http",
                "hosts": [ "192.168.123.107" ],
                "bind": "192.168.123.107",
                "port": 80,
                "secure": "false",
                "rotation": "round-robin",
                "user_agent": "",
                "headers": [
                    "Accept-Type: */*, charset: utf-8"
                ],
                "urls": [
                ],
                "response": {
                }
            } 
        },
        { 
            "http": {
                "name": "Agent Listener - HTTP/s",
                "hosts": [ "192.168.123.107" ],
                "bind": "192.168.123.107",
                "port": 443,
                "secure": "true"
            }
        },
        { 
            "smb": {
                "name": "Pivot - Smb"
            }
        }
    ],
    "demon": {
        "sleep": 20
    }
}
```

The script will fill this in with a random username and a random password. Even if the above block is not defined the
script will define the core blocks for you with random data. You can then use the JSON config to only clarify what 
you want to be used either from the profiles or from a completely random generation.

This is the generated profile
```txt
Teamserver {
    Host = "127.0.0.1"
    Port = "8888"

    Build {
        Compiler64 = "/usr/bin/x86_64-w64-mingw32-gcc"
        Compiler86 = "/usr/bin/i686-w64-mingw32-gcc"
        Nasm = "/usr/bin/nasm"
    }
}
Operators {
    user "brianpena" {
        Password = "#(1jXGJnqo"
    }
}
Listeners {
    Http {
        Name         = "Http"
        Port         = 80
        Hosts        = ["192.168.123.107"]
        HostBind     = "192.168.123.107"
        HostRotation = "round-robin"
        Secure       = true
        UserAgent    = "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 6.0; Trident/4.1)"
        Uris         = ["/owa/", "/OWA/"]
        Headers      = ["Accept-Type: */*, charset: utf-8"]

        Response {
            Headers  = ["Cache-Control: no-cache", "Pragma: no-cache", "Content-Type: text/html; charset=utf-8", "Server: Microsoft-IIS/10.0", "request-id: 6cfcf35d-0680-4853-98c4-b16723708fc9", "X-CalculatedBETarget: BY2PR06MB549.namprd06.prod.outlook.com", "X-Content-Type-Options: nosniff", "X-OWA-Version: 15.1.1240.20", "X-OWA-OWSVersion: V2017_06_15", "X-OWA-MinimumSupportedOWSVersion: V2_6", "X-Frame-Options: SAMEORIGIN", "X-DiagInfo: BY2PR06MB549", "X-UA-Compatible: IE=EmulateIE7", "X-Powered-By: ASP.NET", "X-FEServer: CY4PR02CA0010", "Connection: close"]
        }
    }

    Http {
        Name         = "Agent Listener - HTTP/s"
        Port         = 443
        Hosts        = ["192.168.123.107"]
        HostBind     = "192.168.123.107"
        HostRotation = "round-robin"
        Secure       = true
        UserAgent    = "Opera/9.14.(X11; Linux i686; mg-MG) Presto/2.9.162 Version/11.00"
        Uris         = ["/owa/", "/OWA/"]
        Headers      = ["Host: www.outlook.live.com", "Accept: */*", "Cookie: MicrosoftApplicationsTelemetryDeviceId=95c18d8-4dce9854;ClientId=1C0F6C5D910F9;MSPAuth=3EkAjDKjI;xid=730bf7;wla42=ZG0yMzA2KjEs"]

        Response {
            Headers  = ["Cache-Control: no-cache", "Pragma: no-cache", "Content-Type: text/html; charset=utf-8", "Server: Microsoft-IIS/10.0", "request-id: 6cfcf35d-0680-4853-98c4-b16723708fc9", "X-CalculatedBETarget: BY2PR06MB549.namprd06.prod.outlook.com", "X-Content-Type-Options: nosniff", "X-OWA-Version: 15.1.1240.20", "X-OWA-OWSVersion: V2017_06_15", "X-OWA-MinimumSupportedOWSVersion: V2_6", "X-Frame-Options: SAMEORIGIN", "X-DiagInfo: BY2PR06MB549", "X-UA-Compatible: IE=EmulateIE7", "X-Powered-By: ASP.NET", "X-FEServer: CY4PR02CA0010", "Connection: close"]
        }
    }

    Smb {
        Name     = "Pivot - Smb"
        PipeName = "ShellEx_3081"
    }
}
Demon {
    Sleep = 20
    Jitter = 42

    Injection {
        Spawn64 = "C:\\Windows\\System32\\conhost.exe 0x4"
        Spawn32 = "C:\\Windows\\System32\\conhost.exe 0x4"
    }
}
```

As always I am not responsible for anything done by this script or anyone using this script. Ultimately this is just a
script that generates profiles, which is just text. So don't shoot the messenger.

~~* Coming up next is using https://github.com/brett-fitz/pyMalleableProfileParser to dynamically parse Cobalt Strike profiles directly into usable Havoc prfoiles~~
* Coming up next is updating this to use the latest push to the Havoc Framework and support versions (later)

Have fun!

*Any support is welcome*
