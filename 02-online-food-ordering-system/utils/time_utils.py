from datetime import datetime


class TimeUtils:
    @staticmethod
    def get_current_time() -> str:
        # Java: "EEE MMM dd HH:mm:ss yyyy"  ->  Python strftime equivalent
        return datetime.now().strftime("%a %b %d %H:%M:%S %Y")
