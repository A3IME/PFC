#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime

beg = datetime.now()
subprocess.run(["./VTLockCheck", "virusTotalLock"])
a = sys.argv[2]
end = datetime.now()
print(a)
print((end - beg).seconds)
