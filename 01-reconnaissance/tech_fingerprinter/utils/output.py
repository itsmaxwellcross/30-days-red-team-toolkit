#!/usr/bin/env python3
"""
Output formatting and export utilities
"""

import json
from typing import Dict, Any

class OutputFormatter:
    """Handle result formatting and export"""
    
    @staticmethod
    def print_results(technologies: Dict[str, Any]) -> None:
        """Pretty print the results"""
        for category, data in technologies.items():
            if isinstance(data, dict):
                print(f"[{category.upper()}]")
                for key, value in data.items():
                    if isinstance(value, dict):
                        print(f"  {key}:")
                        for k, v in value.items():
                            print(f"    • {k}: {v}")
                    else:
                        print(f"  • {key}: {value}")
            elif isinstance(data, list):
                print(f"[{category.upper()}]")
                for item in data:
                    print(f"  • {item}")
            else:
                print(f"[{category.upper()}]: {data}")
            print()
    
    @staticmethod
    def export_json(technologies: Dict[str, Any], filename: str) -> None:
        """Export results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(technologies, f, indent=2, default=str)
    
    @staticmethod
    def export_markdown(technologies: Dict[str, Any], filename: str) -> None:
        """Export results to Markdown file"""
        with open(filename, 'w') as f:
            f.write("# Technology Fingerprint Report\n\n")
            
            for category, data in technologies.items():
                f.write(f"## {category.title()}\n\n")
                
                if isinstance(data, dict):
                    for key, value in data.items():
                        f.write(f"**{key}**: {value}\n\n")
                elif isinstance(data, list):
                    for item in data:
                        f.write(f"- {item}\n")
                    f.write("\n")
                else:
                    f.write(f"{data}\n\n")
    
    @staticmethod
    def get_sanitized_filename(url: str) -> str:
        """Create safe filename from URL"""
        return url.replace("://", "_").replace("/", "_").replace(":", "_")