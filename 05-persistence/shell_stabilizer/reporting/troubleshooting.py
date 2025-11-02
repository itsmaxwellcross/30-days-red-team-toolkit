"""Troubleshooting guides for common shell issues"""

def get_linux_troubleshooting():
    """Get Linux troubleshooting guide"""
    return """
Issue: Shell dies when you Ctrl+C
Solution: Use full TTY upgrade (python pty + stty raw)

Issue: No tab completion
Solution: export TERM=xterm and use full TTY

Issue: Backspace doesn't work properly
Solution: stty raw -echo before foregrounding shell

Issue: Can't use interactive programs (vi, less, etc.)
Solution: Full TTY upgrade is required

Issue: Shell hangs/freezes
Solution: Check if TERM is set correctly, use 'reset' command
"""

def get_windows_troubleshooting():
    """Get Windows troubleshooting guide"""
    return """
Issue: Limited command output
Solution: Use PowerShell instead of cmd.exe

Issue: No command history
Solution: Use rlwrap on attacker side or ConPTY

Issue: Encoding issues
Solution: [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Issue: Execution policy blocks scripts
Solution: powershell -ExecutionPolicy Bypass
"""