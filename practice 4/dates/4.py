from datetime import datetime
date1 = datetime(2025, 3, 1, 12, 0, 0)
date2 = datetime(2025, 3, 5, 15, 30, 0)
difference = date2 - date1
seconds = difference.total_seconds()
print(seconds)