"""
Domain warmup schedule generator
"""
from typing import List, Tuple
from ..config.settings import Settings

class WarmupScheduler:
    """Generate email warmup schedules"""
    
    def generate_schedule(self, days: int = 14) -> List[Tuple[int, int, str]]:
        """
        Generate warmup schedule
        
        Args:
            days: Total days for warmup
            
        Returns:
            List of (day, volume, audience) tuples
        """
        print(f"\n[*] Domain Warm-up Schedule ({days} days):")
        print("=" * 60)
        print("    Gradually increase sending volume to build reputation\n")
        
        schedule = Settings.WARMUP_SCHEDULE
        
        # Filter schedule to match requested days
        filtered_schedule = [s for s in schedule if s[0] <= days]
        
        for day, volume, audience in filtered_schedule:
            print(f"    Day {day:2d}: Send {volume:4d} emails to {audience}")
        
        print("\n[*] Warmup Best Practices:")
        print("  • Start with engaged recipients who will open/click")
        print("  • Maintain consistent sending patterns")
        print("  • Monitor bounce rates (<2% is good)")
        print("  • Avoid spam trigger words in early emails")
        print("  • Use proper unsubscribe mechanisms")
        print("  • Monitor sender reputation tools daily")
        
        return filtered_schedule
    
    def get_daily_volume(self, day: int, schedule: List[Tuple[int, int, str]]) -> int:
        """
        Get recommended volume for a specific day
        
        Args:
            day: Day number
            schedule: Warmup schedule
            
        Returns:
            Recommended email volume
        """
        for s_day, volume, _ in reversed(schedule):
            if day >= s_day:
                return volume
        return 0