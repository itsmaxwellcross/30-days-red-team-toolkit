"""
Windows API Structures
ctypes Structure definitions for Windows API calls
"""

import ctypes
from ctypes import wintypes


class STARTUPINFO(ctypes.Structure):
    """
    STARTUPINFO structure for CreateProcess
    Contains information about how a process should be started
    """
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("lpReserved", wintypes.LPWSTR),
        ("lpDesktop", wintypes.LPWSTR),
        ("lpTitle", wintypes.LPWSTR),
        ("dwX", wintypes.DWORD),
        ("dwY", wintypes.DWORD),
        ("dwXSize", wintypes.DWORD),
        ("dwYSize", wintypes.DWORD),
        ("dwXCountChars", wintypes.DWORD),
        ("dwYCountChars", wintypes.DWORD),
        ("dwFillAttribute", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("wShowWindow", wintypes.WORD),
        ("cbReserved2", wintypes.WORD),
        ("lpReserved2", ctypes.POINTER(wintypes.BYTE)),
        ("hStdInput", wintypes.HANDLE),
        ("hStdOutput", wintypes.HANDLE),
        ("hStdError", wintypes.HANDLE),
    ]


class PROCESS_INFORMATION(ctypes.Structure):
    """
    PROCESS_INFORMATION structure
    Contains information about a newly created process and its primary thread
    """
    _fields_ = [
        ("hProcess", wintypes.HANDLE),
        ("hThread", wintypes.HANDLE),
        ("dwProcessId", wintypes.DWORD),
        ("dwThreadId", wintypes.DWORD),
    ]


class CONTEXT(ctypes.Structure):
    """
    CONTEXT structure (x64)
    Contains processor-specific register data
    """
    _fields_ = [
        ("P1Home", ctypes.c_ulonglong),
        ("P2Home", ctypes.c_ulonglong),
        ("P3Home", ctypes.c_ulonglong),
        ("P4Home", ctypes.c_ulonglong),
        ("P5Home", ctypes.c_ulonglong),
        ("P6Home", ctypes.c_ulonglong),
        ("ContextFlags", wintypes.DWORD),
        ("MxCsr", wintypes.DWORD),
        ("SegCs", wintypes.WORD),
        ("SegDs", wintypes.WORD),
        ("SegEs", wintypes.WORD),
        ("SegFs", wintypes.WORD),
        ("SegGs", wintypes.WORD),
        ("SegSs", wintypes.WORD),
        ("EFlags", wintypes.DWORD),
        ("Dr0", ctypes.c_ulonglong),
        ("Dr1", ctypes.c_ulonglong),
        ("Dr2", ctypes.c_ulonglong),
        ("Dr3", ctypes.c_ulonglong),
        ("Dr6", ctypes.c_ulonglong),
        ("Dr7", ctypes.c_ulonglong),
        ("Rax", ctypes.c_ulonglong),
        ("Rcx", ctypes.c_ulonglong),
        ("Rdx", ctypes.c_ulonglong),
        ("Rbx", ctypes.c_ulonglong),
        ("Rsp", ctypes.c_ulonglong),
        ("Rbp", ctypes.c_ulonglong),
        ("Rsi", ctypes.c_ulonglong),
        ("Rdi", ctypes.c_ulonglong),
        ("R8", ctypes.c_ulonglong),
        ("R9", ctypes.c_ulonglong),
        ("R10", ctypes.c_ulonglong),
        ("R11", ctypes.c_ulonglong),
        ("R12", ctypes.c_ulonglong),
        ("R13", ctypes.c_ulonglong),
        ("R14", ctypes.c_ulonglong),
        ("R15", ctypes.c_ulonglong),
        ("Rip", ctypes.c_ulonglong),
    ]


class SECURITY_ATTRIBUTES(ctypes.Structure):
    """
    SECURITY_ATTRIBUTES structure
    Determines whether the returned handle can be inherited by child processes
    """
    _fields_ = [
        ("nLength", wintypes.DWORD),
        ("lpSecurityDescriptor", wintypes.LPVOID),
        ("bInheritHandle", wintypes.BOOL),
    ]


class IMAGE_DOS_HEADER(ctypes.Structure):
    """
    IMAGE_DOS_HEADER structure
    DOS header at the beginning of PE files
    """
    _fields_ = [
        ("e_magic", wintypes.WORD),      # Magic number (MZ)
        ("e_cblp", wintypes.WORD),
        ("e_cp", wintypes.WORD),
        ("e_crlc", wintypes.WORD),
        ("e_cparhdr", wintypes.WORD),
        ("e_minalloc", wintypes.WORD),
        ("e_maxalloc", wintypes.WORD),
        ("e_ss", wintypes.WORD),
        ("e_sp", wintypes.WORD),
        ("e_csum", wintypes.WORD),
        ("e_ip", wintypes.WORD),
        ("e_cs", wintypes.WORD),
        ("e_lfarlc", wintypes.WORD),
        ("e_ovno", wintypes.WORD),
        ("e_res", wintypes.WORD * 4),
        ("e_oemid", wintypes.WORD),
        ("e_oeminfo", wintypes.WORD),
        ("e_res2", wintypes.WORD * 10),
        ("e_lfanew", wintypes.DWORD),    # File address of new exe header
    ]


class IMAGE_FILE_HEADER(ctypes.Structure):
    """
    IMAGE_FILE_HEADER structure
    COFF file header
    """
    _fields_ = [
        ("Machine", wintypes.WORD),
        ("NumberOfSections", wintypes.WORD),
        ("TimeDateStamp", wintypes.DWORD),
        ("PointerToSymbolTable", wintypes.DWORD),
        ("NumberOfSymbols", wintypes.DWORD),
        ("SizeOfOptionalHeader", wintypes.WORD),
        ("Characteristics", wintypes.WORD),
    ]