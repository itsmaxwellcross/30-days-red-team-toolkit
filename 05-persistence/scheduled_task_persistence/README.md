# Scheduled Task Persistence Framework

**Educational tool demonstrating Windows Task Scheduler persistence techniques**

⚠️ **WARNING**: Educational and authorized testing only. Unauthorized use is illegal.

## Overview

Comprehensive framework for Windows scheduled task persistence mechanisms. Shows how attackers maintain access via Task Scheduler and helps defenders understand detection.

## Features

- **6 Trigger Types**
  - User Logon
  - System Boot (requires admin)
  - Time-based Schedule (interval, daily, weekly, hourly)
  - System Idle
  - Multi-trigger (combined)

- **Detection Scanner**
  - Scan for suspicious tasks
  - Identify hidden tasks
  - Find SYSTEM-level tasks
  - Export task XML for analysis

- **Auto Cleanup**
  - Generate removal scripts
  - Batch deletion support

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/scheduled-task-persistence
cd scheduled-task-persistence

# Install
pip install -e .

# Or run directly
python main.py --list
```

## File Structure

```
scheduled_task_persistence/
├── main.py                    # CLI entry
├── config.py                  # Configuration
├── core/
│   ├── orchestrator.py       # Main coordinator
│   └── utils.py              # Utilities
├── triggers/
│   ├── logon.py              # Logon triggers
│   ├── schedule.py           # Time-based
│   ├── idle.py               # Idle triggers
│   ├── boot.py               # Boot triggers
│   └── multi.py              # Multiple triggers
├── detection/
│   └── scanner.py            # Task scanner
├── output/
│   └── removal.py            # Removal scripts
└── templates/
    └── xml_templates.py      # XML generators
```

## Usage

### List Trigger Types

```bash
python main.py --list
```

### Scan for Suspicious Tasks

```bash
python main.py --scan
```

### Create Tasks

```bash
# Logon trigger (most common)
python main.py --trigger logon --payload C:\payload.exe

# Boot trigger (requires admin)
python main.py --trigger boot --payload C:\payload.exe

# Every 10 minutes
python main.py --trigger schedule_interval --payload C:\payload.exe --interval 10

# Daily at 2 AM
python main.py --trigger schedule_daily --payload C:\payload.exe --time 02:00

# When system idle for 10 minutes
python main.py --trigger idle --payload C:\payload.exe --idle-minutes 10

# Multi-trigger (logon + hourly + idle)
python main.py --trigger multi --payload C:\payload.exe

# Custom task name
python main.py --trigger logon --payload C:\payload.exe --task-name "WindowsUpdate"
```

### Python API

```python
from core.orchestrator import ScheduledTaskOrchestrator

# Initialize
orch = ScheduledTaskOrchestrator()

# Create logon task
result = orch.create_task('logon', r'C:\payload.exe')

# Create interval task (every 30 minutes)
result = orch.create_task(
    'schedule_interval',
    r'C:\payload.exe',
    interval=30
)

# Scan for suspicious tasks
orch.scan_existing()

# Delete task
orch.delete_task('TaskName')
```

## Trigger Types Explained

### 1. Logon Trigger
- **Executes**: User logs on
- **Admin**: No
- **Detection**: Easy - common location
- **Use**: Standard persistence

### 2. Boot Trigger
- **Executes**: System startup
- **Admin**: Yes (runs as SYSTEM)
- **Detection**: Easy
- **Use**: System-wide persistence

### 3. Schedule Triggers
- **Interval**: Every N minutes
- **Daily**: Specific time each day
- **Hourly**: Every hour
- **Weekly**: Specific day/time weekly
- **Admin**: No
- **Detection**: Medium
- **Use**: Regular execution

### 4. Idle Trigger
- **Executes**: System idle for N minutes
- **Admin**: No
- **Detection**: Medium - less common
- **Use**: Stealthy, activates when user away

### 5. Multi-Trigger
- **Executes**: Multiple conditions (logon + hourly + idle)
- **Admin**: No
- **Detection**: Hard - redundant triggers
- **Use**: Maximum persistence

## Detection

### Manual Detection

```cmd
# List all tasks
schtasks /Query /FO LIST /V

# Check specific task
schtasks /Query /TN "TaskName" /V /FO LIST

# Export task XML
schtasks /Query /TN "TaskName" /XML > task.xml

# List CSV format for analysis
schtasks /Query /FO CSV /V > tasks.csv
```

### Using Scanner

```bash
# Full scan
python main.py --scan

# Shows:
# - Suspicious indicators (PowerShell, hidden, bypass, etc.)
# - Hidden tasks
# - Non-standard SYSTEM tasks
```

### Indicators of Compromise

- Hidden tasks (not in standard Windows folders)
- Tasks with suspicious commands:
  - `powershell -encodedcommand`
  - `-WindowStyle Hidden`
  - `-ExecutionPolicy Bypass`
  - `IEX`, `DownloadString`
- Tasks running as SYSTEM outside Windows folders
- Recently created tasks
- Tasks with unusual trigger combinations

## Removal

### Automatic Removal

Installation generates `remove_tasks_YYYYMMDD_HHMMSS.bat`:

```cmd
remove_tasks_20241118_153045.bat
```

### Manual Removal

```cmd
# Delete specific task
schtasks /Delete /TN "TaskName" /F

# Delete all non-Windows tasks (careful!)
FOR /F "tokens=1 delims=," %i IN ('schtasks /Query /FO CSV ^| findstr /V "Microsoft"') DO schtasks /Delete /TN %i /F
```

## Detection Rules

### Splunk

```spl
index=windows EventCode=4698 OR EventCode=4699
| eval TaskName=lower(TaskName)
| where NOT match(TaskName, "^\\microsoft\\")
| stats count by TaskName, Command
```

### Sigma

```yaml
title: Suspicious Scheduled Task Creation
detection:
  selection:
    EventID: 4698
    TaskContent|contains:
      - 'powershell'
      - 'hidden'
      - 'bypass'
      - 'encodedcommand'
  filter:
    TaskName|startswith: '\Microsoft\'
  condition: selection and not filter
```

## MITRE ATT&CK Mapping

- **T1053.005** - Scheduled Task/Job: Scheduled Task
- **T1543** - Create or Modify System Process
- **T1547** - Boot or Logon Autostart Execution

## Best Practices

### For Red Teams
1. Use legitimate-looking task names
2. Combine multiple triggers for redundancy
3. Hide tasks from GUI
4. Use delayed boot triggers
5. Test detection before deployment

### For Blue Teams
1. Monitor EventID 4698 (Task Created)
2. Monitor EventID 4699 (Task Deleted)
3. Baseline legitimate tasks
4. Alert on tasks outside Windows folders
5. Check for hidden or SYSTEM tasks regularly

## Legal Notice

⚠️ **Educational and authorized testing only**

- Only use on systems you own or have permission to test
- Understand local laws and regulations
- This tool is for defensive security research

**Authors not responsible for misuse.**

## Files Breakdown

### __init__.py Files

```python
# scheduled_task_persistence/__init__.py
"""Scheduled Task Persistence Framework"""
__version__ = "1.0.0"
from core.orchestrator import ScheduledTaskOrchestrator
__all__ = ['ScheduledTaskOrchestrator']

# core/__init__.py
"""Core functionality"""
from core.orchestrator import ScheduledTaskOrchestrator
from core.utils import *
__all__ = ['ScheduledTaskOrchestrator']

# triggers/__init__.py
"""Trigger implementations"""
from triggers.logon import LogonTrigger
from triggers.schedule import ScheduleTrigger
from triggers.idle import IdleTrigger
from triggers.boot import BootTrigger
from triggers.multi import MultiTrigger
__all__ = ['LogonTrigger', 'ScheduleTrigger', 'IdleTrigger', 'BootTrigger', 'MultiTrigger']

# detection/__init__.py
"""Detection utilities"""
from detection.scanner import TaskScanner
__all__ = ['TaskScanner']

# output/__init__.py
"""Output utilities"""
from output.removal import RemovalScriptGenerator
__all__ = ['RemovalScriptGenerator']

# templates/__init__.py
"""XML templates"""
from templates.xml_templates import TaskXMLTemplates
__all__ = ['TaskXMLTemplates']
```

### setup.py

```python
from setuptools import setup, find_packages

setup(
    name="scheduled-task-persistence",
    version="1.0.0",
    author="Maxwell Cross",
    description="Scheduled Task Persistence Framework",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'schtask-persist=main:main',
        ],
    },
)
```

### requirements.txt

```
# No external dependencies - uses Python standard library only
```

### .gitignore

```
__pycache__/
*.py[cod]
*$py.class
*.so
build/
dist/
*.egg-info/
.venv/
venv/
remove_tasks_*.bat
*.xml
```

## Contributing

Contributions welcome! Add new trigger types, improve detection, or enhance documentation.

## License

MIT License

## Author

Maxwell Cross - 30 Days of Red Team Series

## References

- [MITRE ATT&CK - Scheduled Task](https://attack.mitre.org/techniques/T1053/005/)
- [Microsoft Task Scheduler](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page)
- [Windows Event Log Monitoring](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/)