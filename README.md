Havoc C2 profile generator is a python3 script that generates profiles to be used with the Havoc C2 Framework.

There are six built in profiles copied from https://github.com/xx0hcd/Malleable-C2-Profiles as a base. You can 
now parse Cobalt Strike profiles using this tool (I only need to add a couple of additional checks, but it works).

The idea of this generator was to make it extensible and to separate the parts of a profile out to make easy 
randomization if need be. The randomization works by leaving creating a block but leaving it empty as such.

The script will fill this in with a random username and a random password. Even if the above block is not defined the
script will define the core blocks for you with random data. You can then use the JSON config to only clarify what 
you want to be used either from the profiles or from a completely random generation.

This is the generated profile
```bash
> python3 ./havoc_profile_generator.py -c ./sample.config.json -r ./Malleable-C2-Profiles/normal -p office365_calendar.profile  -H 192.168.1.40 -L 192.168.1.40,192.168.2.2,192.168.2.1 -q
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
    user "Neo" {
        Password = "password"
    }

    user "c0z" {
        Password = "password"
    }
}
Listeners {
    Http {
        Name         = "Http"
        KillDate     = "2023-11-07 11:31:06"
        WorkingHours = "0:00-23:59"
        Hosts        =  ["192.168.1.40", "192.168.2.2", "192.168.2.1"]
        HostBind     = "192.168.1.40"
        HostRotation = "round-robin"
        PortBind     =  80
        PortConn     =  80
        Secure       =  false
        UserAgent    = "Mozilla/5.0 (Android 8.1.0; Mobile; rv:47.0) Gecko/47.0 Firefox/47.0"
        Uris         =  ["/owa/", "/OWA/"]
        Headers      =  ["Accept-Type: */*, charset: utf-8"]

        Response {
            Headers  = ["Cache-Control: no-cache", "Pragma: no-cache", "Content-Type: text/html; charset=utf-8", "Server: Microsoft-IIS/10.0", "request-id: 6cfcf35d-0680-4853-98c4-b16723708fc9", "X-CalculatedBETarget: BY2PR06MB549.namprd06.prod.outlook.com", "X-Content-Type-Options: nosniff", "X-OWA-Version: 15.1.1240.20", "X-OWA-OWSVersion: V2017_06_15", "X-OWA-MinimumSupportedOWSVersion: V2_6", "X-Frame-Options: SAMEORIGIN", "X-DiagInfo: BY2PR06MB549", "X-UA-Compatible: IE=EmulateIE7", "X-Powered-By: ASP.NET", "X-FEServer: CY4PR02CA0010", "Connection: close"]
        }
    }

    Http {
        Name         = "Agent Listener - HTTP/s"
        KillDate     = "2023-08-14 05:47:03"
        WorkingHours = "0:00-23:59"
        Hosts        =  ["192.168.1.40", "192.168.2.2", "192.168.2.1"]
        HostBind     = "192.168.1.40"
        HostRotation = "round-robin"
        PortBind     =  443
        PortConn     =  443
        Secure       =  true
        UserAgent    = "Mozilla/5.0 (Windows 98; kn-IN; rv:1.9.0.20) Gecko/5960-08-08 22:52:45 Firefox/3.6.8"
        Uris         =  ["/owa/", "/OWA/"]
        Headers      =  ["Accept: */*", "Cookie: MicrosoftApplicationsTelemetryDeviceId=95c18d8-4dce9854;ClientId=1C0F6C5D910F9;MSPAuth=3EkAjDKjI;xid=730bf7;wla42=ZG0yMzA2KjEs"]

        Response {
            Headers  = ["Cache-Control: no-cache", "Pragma: no-cache", "Content-Type: text/html; charset=utf-8", "Server: Microsoft-IIS/10.0", "request-id: 6cfcf35d-0680-4853-98c4-b16723708fc9", "X-CalculatedBETarget: BY2PR06MB549.namprd06.prod.outlook.com", "X-Content-Type-Options: nosniff", "X-OWA-Version: 15.1.1240.20", "X-OWA-OWSVersion: V2017_06_15", "X-OWA-MinimumSupportedOWSVersion: V2_6", "X-Frame-Options: SAMEORIGIN", "X-DiagInfo: BY2PR06MB549", "X-UA-Compatible: IE=EmulateIE7", "X-Powered-By: ASP.NET", "X-FEServer: CY4PR02CA0010", "Connection: close"]
        }
    }

    Smb {
        Name         = "Pivot - Smb"
        PipeName     = "ntsvcs571"
    }
    External {
        Name      = "ernestmckenzie"
        Endpoint  = "None"
    }
}
Service {
    Endpoint = "service-endpoint"
    Password = "service-password"
}
Demon {
    Sleep  = 20
    Jitter = 20

    Injection {
        Spawn64 = "C:\\Windows\\System32\\gpupdate.exe"
        Spawn32 = "C:\\Windows\\SysWow64\\gpupdate.exe"
    }
}
```

As always I am not responsible for anything done by this script or anyone using this script. Ultimately this is just a
script that generates profiles, which is just text. So don't shoot the messenger.

~~* Coming up next is using https://github.com/brett-fitz/pyMalleableProfileParser to dynamically parse Cobalt Strike profiles directly into usable Havoc prfoiles~~

* Coming up next is updating this to use the latest push to the Havoc Framework and support versions (later)

Have fun!

*Any support is welcome*
