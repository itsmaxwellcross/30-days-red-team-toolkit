# Attack Chain Templates

Pre-configured, repeatable attack workflows for common red team scenarios.

## Overview

Attack chain templates provide structured, step-by-step workflows that can be executed repeatedly with different targets. Each template includes:

- **Phases**: Logical groupings of attack activities
- **Steps**: Individual commands with success criteria
- **Variable Substitution**: Dynamic command generation
- **Documentation**: Expected outputs and notes

## Directory Structure

```
templates/
├── __init__.py                 # Package initialization
├── manager.py                  # Template management
├── executor.py                 # Template execution engine
├── cli.py                      # Command-line interface
├── web_app.py                  # Web application templates
├── domain.py                   # Active Directory templates
├── lateral.py                  # Lateral movement templates
├── exfiltration.py             # Data exfiltration templates
├── ransomware.py               # Ransomware simulation templates
└── chains/                     # Custom template storage
    └── *.json                  # User-defined templates
```

## Available Templates

### 1. Web Application Takeover
**ID**: `web_app_takeover`  
**Target**: Web applications with upload functionality or vulnerabilities  
**Difficulty**: Medium  
**Time**: 2-4 hours

**Phases**:
- Reconnaissance (subdomain enumeration, tech fingerprinting, dorking)
- Exploitation (vulnerability scanning, web shell upload)
- Post-Exploitation (reverse shell, credential harvesting, database dump)

### 2. Domain Compromise
**ID**: `domain_compromise`  
**Target**: Windows Active Directory environments  
**Difficulty**: High  
**Time**: 4-8 hours

**Phases**:
- AD Reconnaissance (user enumeration, SMB/LDAP discovery)
- Initial Access (password spraying, phishing)
- Privilege Escalation (local exploits, Kerberoasting)
- Domain Takeover (DCSync, Pass-the-Hash, Golden Ticket)

### 3. Lateral Movement
**ID**: `lateral_movement`  
**Target**: Internal network after initial compromise  
**Difficulty**: Medium  
**Time**: 2-6 hours

**Phases**:
- Network Discovery (mapping, port scanning)
- Credential Theft (memory dumps, browser credentials)
- Lateral Movement (PSExec, WMI, SSH)
- Persistence (backdoor accounts, scheduled tasks)

### 4. Data Exfiltration
**ID**: `data_exfiltration`  
**Target**: Systems with sensitive data  
**Difficulty**: Medium  
**Time**: 3-6 hours

**Phases**:
- Data Discovery (file search, database enumeration)
- Data Collection (copying, dumping databases)
- Data Staging (compression, encryption)
- Exfiltration (HTTP, DNS, ICMP tunneling)

### 5. Ransomware Simulation
**ID**: `ransomware_simulation`  
**Target**: Test environments only  
**Difficulty**: High  
**Time**: 4-8 hours

**⚠️ WARNING**: Authorized use only in isolated test environments

**Phases**:
- Initial Compromise (phishing, payload execution)
- Reconnaissance (domain/backup enumeration)
- Lateral Spread (credential theft, deployment)
- Encryption Simulation (safe testing mode only)

## Usage

### Command-Line Interface

```bash
# List all templates
python3 -m templates.cli --list

# Show template details
python3 -m templates.cli --show web_app_takeover

# Execute template with variable file
python3 -m templates.cli --execute web_app_takeover --vars config.json

# Execute specific phase only
python3 -m templates.cli --execute lateral_movement --phase reconnaissance

# Execute specific step
python3 -m templates.cli --execute domain_compromise --phase initial_access --step 2

# Export template
python3 -m templates.cli --export web_app_takeover --output my_template.json

# Import custom template
python3 -m templates.cli --import my_custom_attack.json
```

### Python API

```python
from templates import AttackChainTemplateManager, TemplateExecutor
from core.logger import EngagementLogger
from core.executor import CommandExecutor

# Initialize
manager = AttackChainTemplateManager()
template = manager.get_template('web_app_takeover')

# Set variables
variables = {
    'target_domain': 'example.com',
    'attacker_ip': '10.10.14.5',
    'attacker_port': 4444
}

# Execute
logger = EngagementLogger('template_execution')
command_executor = CommandExecutor(logger)
executor = TemplateExecutor(template, variables, command_executor, logger)

results = executor.execute()
executor.save_results('results/templates/')
```

## Variable Configuration

### Using JSON File

Create a `variables.json` file:

```json
{
  "target_domain": "example.com",
  "company_name": "Example Corporation",
  "target_ip": "192.168.1.100",
  "internal_subnet": "192.168.1.0/24",
  "attacker_ip": "10.10.14.5",
  "attacker_port": 4444,
  "domain": "EXAMPLE",
  "username": "compromised_user",
  "password": "P@ssw0rd123"
}
```

Then execute:
```bash
python3 -m templates.cli --execute web_app_takeover --vars variables.json
```

### Interactive Prompts

If no variables file is provided, the CLI will prompt for required variables:

```bash
python3 -m templates.cli --execute web_app_takeover

Variable Configuration
================================
Enter values for required variables:

attacker_ip: 10.10.14.5
attacker_port: 4444
target_domain: example.com
```

## Creating Custom Templates

### Template Structure

```json
{
  "name": "My Custom Attack",
  "description": "Description of attack chain",
  "target_type": "web_application",
  "difficulty": "medium",
  "estimated_time": "2-4 hours",
  "phases": [
    {
      "phase": "reconnaissance",
      "name": "Information Gathering",
      "description": "Gather target information",
      "steps": [
        {
          "step": 1,
          "name": "Port Scanning",
          "tool": "nmap",
          "command": "nmap -sV {target_ip}",
          "expected_output": "Open ports and services",
          "success_criteria": "Found accessible services",
          "required_vars": ["target_ip"],
          "optional": false
        }
      ]
    }
  ]
}
```

### Template Fields

**Template Level**:
- `name`: Template name
- `description`: Brief description
- `target_type`: Type of target
- `difficulty`: easy/medium/high
- `estimated_time`: Expected duration
- `prerequisites`: Required conditions (optional)
- `warnings`: Important warnings (optional)
- `phases`: Array of phase objects

**Phase Level**:
- `phase`: Phase identifier (lowercase, underscores)
- `name`: Display name
- `description`: Phase description (optional)
- `steps`: Array of step objects

**Step Level**:
- `step`: Step number
- `name`: Step name
- `tool`: Tool used
- `command`: Command to execute (with {variable} placeholders)
- `expected_output`: What output indicates
- `success_criteria`: How to determine success
- `required_vars`: Array of required variable names
- `optional`: Whether step is optional (default: false)
- `timeout`: Command timeout in seconds (default: 300)
- `notes`: Additional information (optional)

### Variable Substitution

Use curly braces for variables: `{variable_name}`

Example:
```json
{
  "command": "python3 scan.py {target_domain} -p {port}",
  "required_vars": ["target_domain", "port"]
}
```

## Safety Features

### Confirmations

The executor will prompt for confirmation before running:
- Steps marked as dangerous (delete, encrypt, disable commands)
- Optional steps
- Templates with warnings

### Dry Run Mode

Test templates without execution:

```python
executor = TemplateExecutor(template, variables, command_executor, logger)
# Validate template and variables without executing
executor.validate()
```

### Result Tracking

All executions are logged with:
- Timestamp for each step
- Command executed
- Success/failure status
- Output/error messages
- Results saved to JSON

## Best Practices

1. **Test First**: Run templates in lab environments before production engagements
2. **Variable Files**: Use variable files for repeatable executions
3. **Phase Execution**: Execute phase-by-phase for better control
4. **Custom Templates**: Create templates for organization-specific scenarios
5. **Documentation**: Document custom templates thoroughly
6. **Version Control**: Track template changes in git
7. **Review Results**: Always review execution results for anomalies

## Integration with Framework

Templates integrate with the main framework:

```python
from core.framework import RedTeamFramework
from templates import AttackChainTemplateManager

framework = RedTeamFramework('config/engagement.json')
template_manager = AttackChainTemplateManager()

# Execute template as part of engagement
template = template_manager.get_template('web_app_takeover')
# ... execute template with framework components
```

## Troubleshooting

**Missing Variables**:
```
[!] Missing required variables: target_ip, domain
```
Solution: Provide all required variables in JSON file or via prompts

**Command Failures**:
- Check logs in `logs/` directory
- Verify tool installation
- Confirm network connectivity
- Review variable values

**Template Not Found**:
```
[!] Template 'xyz' not found
```
Solution: Run `--list` to see available templates

## Examples

### Quick Web App Test

```bash
# Create variables file
cat > webapp_vars.json << EOF
{
  "target_domain": "testapp.example.com",
  "attacker_ip": "10.10.14.5",
  "attacker_port": 4444
}
EOF

# Execute reconnaissance phase only
python3 -m templates.cli --execute web_app_takeover \
  --vars webapp_vars.json \
  --phase reconnaissance
```

### Full Domain Compromise

```bash
# Interactive execution with prompts
python3 -m templates.cli --execute domain_compromise

# Or with pre-configured variables
python3 -m templates.cli --execute domain_compromise \
  --vars domain_vars.json
```

### Custom Lateral Movement

```bash
# Export template for customization
python3 -m templates.cli --export lateral_movement \
  --output my_lateral.json

# Edit my_lateral.json with your modifications

# Import and execute
python3 -m templates.cli --import my_lateral.json
python3 -m templates.cli --execute my_lateral --vars vars.json
```