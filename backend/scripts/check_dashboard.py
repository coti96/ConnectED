import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.dashboard import DashboardModel

def check_marie_stats():
    try:
        stats = DashboardModel.get_stats('marie@etudiant.com')
        print(f"Marie stats: {stats}")
        activity = DashboardModel.get_recent_activity('marie@etudiant.com')
        print(f"Marie activity count: {len(activity)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_marie_stats()
