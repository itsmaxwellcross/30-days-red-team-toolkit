"""
Main Red Team Framework orchestrator
"""

import time
from datetime import datetime
from pathlib import Path

from core.config import ConfigManager
from core.logger import EngagementLogger
from core.executor import CommandExecutor
from core.reporter import ReportGenerator
from phases.reconnaissance import ReconnaissancePhase
from phases.weaponization import WeaponizationPhase
from phases.delivery import DeliveryPhase
from phases.exploitation import ExploitationPhase
from phases.post_exploitation import PostExploitationPhase


class RedTeamFramework:
    """
    Master orchestrator for red team engagements
    Coordinates all phases and manages engagement lifecycle
    """
    
    def __init__(self, config_file='config/engagement.json'):
        # Initialize core components
        self.config = ConfigManager(config_file)
        self.engagement_id = self._generate_engagement_id()
        self.logger = EngagementLogger(self.engagement_id)
        self.executor = CommandExecutor(self.logger, Path(__file__).parent.parent)
        
        # Initialize results tracking
        self.results = {
            'engagement_id': self.engagement_id,
            'start_time': datetime.now().isoformat(),
            'target': {
                'domain': self.config.get('target.domain'),
                'company': self.config.get('target.company_name')
            },
            'phases': {}
        }
        
        # Initialize phases
        self.phases = self._initialize_phases()
    
    def _generate_engagement_id(self):
        """Generate unique engagement ID"""
        return f"ENG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _initialize_phases(self):
        """Initialize all engagement phases"""
        return {
            'reconnaissance': ReconnaissancePhase(
                self.config, self.executor, self.logger
            ),
            'weaponization': WeaponizationPhase(
                self.config, self.executor, self.logger
            ),
            'delivery': DeliveryPhase(
                self.config, self.executor, self.logger
            ),
            'exploitation': ExploitationPhase(
                self.config, self.executor, self.logger
            ),
            'post_exploitation': PostExploitationPhase(
                self.config, self.executor, self.logger, self.engagement_id
            )
        }
    
    def run_full_engagement(self):
        """Execute complete engagement workflow"""
        self._print_engagement_header()
        
        phase_sequence = [
            ('reconnaissance', 'Phase 1: Reconnaissance'),
            ('weaponization', 'Phase 2: Weaponization'),
            ('delivery', 'Phase 3: Delivery'),
            ('exploitation', 'Phase 4: Exploitation'),
            ('post_exploitation', 'Phase 5: Post-Exploitation')
        ]
        
        for phase_key, phase_name in phase_sequence:
            self.logger.info(f"\nStarting {phase_name}...")
            
            try:
                phase_results = self._execute_phase(phase_key)
                self.results['phases'][phase_key] = phase_results
                
                # Generate phase report
                reporter = ReportGenerator(self.results, self.config)
                report_path = reporter.generate_phase_report(phase_key, phase_results)
                self.logger.info(f"Phase report saved: {report_path}")
                
                # Delay between phases if configured
                self._phase_delay()
            
            except Exception as e:
                self.logger.error(f"Phase failed: {e}")
                
                if not self.config.get('options.continue_on_error', False):
                    self.logger.error("Stopping engagement due to error")
                    break
        
        # Generate final report
        self._finalize_engagement()
    
    def _print_engagement_header(self):
        """Print engagement header information"""
        self.logger.separator()
        self.logger.info("RED TEAM ENGAGEMENT AUTOMATION")
        self.logger.separator()
        self.logger.info(f"Engagement ID: {self.engagement_id}")
        self.logger.info(f"Target: {self.config.get('target.domain')}")
        self.logger.info(f"Start Time: {self.results['start_time']}")
        self.logger.separator()
    
    def _execute_phase(self, phase_key):
        """Execute a specific phase"""
        phase = self.phases.get(phase_key)
        if not phase:
            raise ValueError(f"Unknown phase: {phase_key}")
        
        return phase.execute()
    
    def _phase_delay(self):
        """Wait between phases if configured"""
        delay = self.config.get('options.delay_between_phases', 0)
        if delay > 0:
            self.logger.info(f"Waiting {delay} seconds before next phase...")
            time.sleep(delay)
    
    def _finalize_engagement(self):
        """Finalize engagement and generate reports"""
        self.results['end_time'] = datetime.now().isoformat()
        
        reporter = ReportGenerator(self.results, self.config)
        json_report, md_report = reporter.generate_final_report()
        
        self.logger.separator()
        self.logger.info("GENERATING FINAL REPORT")
        self.logger.separator()
        self.logger.info(f"Final report saved: {json_report}")
        self.logger.info(f"Markdown report: {md_report}")
        self.logger.info("\nEngagement complete!")
    
    # Individual phase execution methods
    def phase_1_reconnaissance(self):
        """Execute reconnaissance phase only"""
        return self._execute_phase('reconnaissance')
    
    def phase_2_weaponization(self):
        """Execute weaponization phase only"""
        return self._execute_phase('weaponization')
    
    def phase_3_delivery(self):
        """Execute delivery phase only"""
        return self._execute_phase('delivery')
    
    def phase_4_exploitation(self):
        """Execute exploitation phase only"""
        return self._execute_phase('exploitation')
    
    def phase_5_post_exploitation(self):
        """Execute post-exploitation phase only"""
        return self._execute_phase('post_exploitation')