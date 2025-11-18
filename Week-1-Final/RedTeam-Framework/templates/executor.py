"""
Attack Chain Template Executor
Executes templates with proper variable substitution and logging
"""

import json
from datetime import datetime
from pathlib import Path


class TemplateExecutor:
    """
    Executes attack chain templates
    Handles variable substitution, step execution, and result tracking
    """
    
    def __init__(self, template, variables, executor, logger):
        """
        Initialize template executor
        
        Args:
            template: Attack chain template dictionary
            variables: Dictionary of variables for command substitution
            executor: CommandExecutor instance for running commands
            logger: EngagementLogger instance for logging
        """
        self.template = template
        self.variables = variables
        self.executor = executor
        self.logger = logger
        self.results = {
            'template_name': template['name'],
            'start_time': datetime.now().isoformat(),
            'phases': [],
            'status': 'in_progress'
        }
    
    def execute(self, phase_filter=None, step_filter=None):
        """
        Execute template with optional filters
        
        Args:
            phase_filter: Only execute specified phase (e.g., 'reconnaissance')
            step_filter: Only execute specified step number
        """
        self.logger.section_header(f"EXECUTING TEMPLATE: {self.template['name']}")
        self.logger.info(f"Description: {self.template['description']}")
        
        if 'warnings' in self.template:
            self._display_warnings()
        
        for phase in self.template['phases']:
            # Apply phase filter if specified
            if phase_filter and phase['phase'] != phase_filter:
                continue
            
            phase_result = self._execute_phase(phase, step_filter)
            self.results['phases'].append(phase_result)
        
        self.results['end_time'] = datetime.now().isoformat()
        self.results['status'] = 'completed'
        
        return self.results
    
    def _display_warnings(self):
        """Display template warnings"""
        self.logger.warning("=" * 60)
        self.logger.warning("IMPORTANT WARNINGS:")
        for warning in self.template['warnings']:
            self.logger.warning(f"  * {warning}")
        self.logger.warning("=" * 60)
        
        # Require acknowledgment for dangerous templates
        if 'ransomware' in self.template['name'].lower():
            response = input("\nType 'I ACKNOWLEDGE' to proceed: ")
            if response != "I ACKNOWLEDGE":
                raise ValueError("Template execution aborted - acknowledgment required")
    
    def _execute_phase(self, phase, step_filter=None):
        """Execute a single phase"""
        self.logger.section_header(f"PHASE: {phase['name']}")
        
        if 'description' in phase:
            self.logger.info(f"Description: {phase['description']}")
        
        phase_result = {
            'phase': phase['phase'],
            'name': phase['name'],
            'start_time': datetime.now().isoformat(),
            'steps': []
        }
        
        for step in phase['steps']:
            # Apply step filter if specified
            if step_filter and step['step'] != step_filter:
                continue
            
            # Skip optional steps if not explicitly requested
            if step.get('optional', False) and not self._should_execute_optional(step):
                self.logger.info(f"Skipping optional step {step['step']}: {step['name']}")
                continue
            
            step_result = self._execute_step(step)
            phase_result['steps'].append(step_result)
            
            # Stop phase execution if critical step fails
            if not step_result['success'] and not step.get('optional', False):
                self.logger.error(f"Critical step failed, stopping phase execution")
                break
        
        phase_result['end_time'] = datetime.now().isoformat()
        return phase_result
    
    def _execute_step(self, step):
        """Execute a single step"""
        self.logger.info(f"\n--- Step {step['step']}: {step['name']} ---")
        
        # Display step notes if present
        if 'notes' in step:
            self.logger.info(f"Notes: {step['notes']}")
        
        # Check for required variables
        missing_vars = self._check_required_vars(step)
        if missing_vars:
            self.logger.error(f"Missing required variables: {', '.join(missing_vars)}")
            return {
                'step': step['step'],
                'name': step['name'],
                'success': False,
                'error': f"Missing variables: {', '.join(missing_vars)}"
            }
        
        # Format command with variables
        command = self._format_command(step['command'])
        
        # Log expected output and success criteria
        self.logger.info(f"Expected output: {step['expected_output']}")
        self.logger.info(f"Success criteria: {step['success_criteria']}")
        
        # Ask for confirmation if step is dangerous
        if self._is_dangerous_step(step):
            if not self._confirm_execution(step):
                self.logger.warning("Step execution skipped by user")
                return {
                    'step': step['step'],
                    'name': step['name'],
                    'success': False,
                    'skipped': True
                }
        
        # Execute command
        result = self.executor.run_command(command, timeout=step.get('timeout', 300))
        
        step_result = {
            'step': step['step'],
            'name': step['name'],
            'command': command,
            'success': result['success'],
            'timestamp': datetime.now().isoformat()
        }
        
        if result['success']:
            self.logger.success(f"Step {step['step']} completed successfully")
            step_result['output'] = result.get('stdout', '')
        else:
            self.logger.error(f"Step {step['step']} failed")
            step_result['error'] = result.get('stderr', '')
        
        return step_result
    
    def _format_command(self, command):
        """Format command with variable substitution"""
        formatted = command
        for key, value in self.variables.items():
            formatted = formatted.replace(f'{{{key}}}', str(value))
        return formatted
    
    def _check_required_vars(self, step):
        """Check if all required variables are present"""
        required_vars = step.get('required_vars', [])
        missing = []
        
        for var in required_vars:
            if var not in self.variables:
                missing.append(var)
        
        return missing
    
    def _should_execute_optional(self, step):
        """Prompt user whether to execute optional step"""
        response = input(f"\nExecute optional step '{step['name']}'? (y/n): ")
        return response.lower() in ['y', 'yes']
    
    def _is_dangerous_step(self, step):
        """Determine if step is potentially dangerous"""
        dangerous_keywords = [
            'delete', 'remove', 'format', 'encrypt', 'disable',
            'shadowcopy', 'vssadmin', 'ransomware'
        ]
        
        command_lower = step['command'].lower()
        return any(keyword in command_lower for keyword in dangerous_keywords)
    
    def _confirm_execution(self, step):
        """Get user confirmation for dangerous step"""
        self.logger.warning(f"\n⚠️  POTENTIALLY DANGEROUS OPERATION ⚠️")
        self.logger.warning(f"Step: {step['name']}")
        self.logger.warning(f"Command: {self._format_command(step['command'])}")
        
        response = input("\nProceed with execution? (yes/no): ")
        return response.lower() == 'yes'
    
    def save_results(self, output_dir):
        """Save execution results to file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"template_execution_{self.template['name'].replace(' ', '_')}_{timestamp}.json"
        filepath = output_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        self.logger.info(f"Results saved to: {filepath}")
        return str(filepath)