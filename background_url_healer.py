"""
Background URL Healing Service
Automatically runs in background to continuously heal broken document URLs
"""

import threading
import time
import logging
from utils.self_healing_url_system import SelfHealingURLSystem
import schedule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackgroundURLHealer:
    def __init__(self, interval_hours=6):
        """
        Initialize background URL healer
        interval_hours: How often to run healing (default: every 6 hours)
        """
        self.interval_hours = interval_hours
        self.healer = SelfHealingURLSystem()
        self.is_running = False
        self.thread = None
        
    def start(self):
        """Start the background healing service"""
        if self.is_running:
            logger.info("Background URL healer already running")
            return
            
        self.is_running = True
        logger.info(f"Starting background URL healer (every {self.interval_hours} hours)")
        
        # Schedule healing job
        schedule.every(self.interval_hours).hours.do(self._heal_urls_job)
        
        # Run initial healing
        threading.Timer(30, self._heal_urls_job).start()  # Start after 30 seconds
        
        # Start scheduler thread
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop the background healing service"""
        self.is_running = False
        schedule.clear()
        logger.info("Background URL healer stopped")
        
    def _run_scheduler(self):
        """Run the scheduler in background thread"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    def _heal_urls_job(self):
        """The actual healing job"""
        logger.info("Starting automatic URL healing...")
        try:
            stats = self.healer.heal_all_urls()
            logger.info(f"Automatic healing complete: {stats['healed']} healed, {stats['failed']} failed")
        except Exception as e:
            logger.error(f"Error during automatic URL healing: {e}")

# Global healer instance
background_healer = BackgroundURLHealer()

def start_background_healing():
    """Start the background URL healing service"""
    background_healer.start()

def stop_background_healing():
    """Stop the background URL healing service"""
    background_healer.stop()

if __name__ == "__main__":
    # Run as standalone service
    healer = BackgroundURLHealer(interval_hours=1)  # More frequent for testing
    healer.start()
    
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Shutting down background URL healer...")
        healer.stop()