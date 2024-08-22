from enum import Enum

class Arch(Enum):
    X86 = 0
    X64 = 1
    X86_64 = 3

class AllocEnum(Enum):
    Win32 = 0
    Syscall = 1

class ExecuteEnum(Enum):
    Win32 = 0
    Syscall = 1

class SleepObfEnum(Enum):
    No_Obf = 0
    Ekko = 1
    Zilean = 2
    Foliage = 3

class SleepBypassEnum(Enum):
    No_Bypass = 0
    JmpRAX = 1
    JmpRBX = 2

class AmsiPatchEnum(Enum):
    No_Patch = 0
    HWBP_Patch = 1
    Mem_Patch = 2

class SslRsaKeyLen(Enum):
    RSA_1024 = 1024
    RSA_2048 = 2048
    RSA_4096 = 4096