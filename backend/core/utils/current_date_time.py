from datetime import datetime

class CurrentDateTime:
    
    # Get current time formatted
    def get_current_time(self) -> str:
        """
        Returns current time in YYYY/MM/DD HH:MM:SS format
        """
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")