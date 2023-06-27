from enum import Enum

class Arch(Enum):
    X86 = 0
    X64 = 1
    X86_64 = 3

class AllocEnum(Enum):
    Win32 = 0
    Syscall = 1
    Empty = 2

class ExecuteEnum(Enum):
    Win32 = 0
    Syscall = 1
    Empty = 2