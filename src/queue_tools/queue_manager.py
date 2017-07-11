#!/usr/bin/env python3
import subprocess

p = subprocess.Popen(["./scripttest", "test", "2"], stdout=subprocess.PIPE)
a, err = p.communicate()
a = a.decode("UTF-8").rstrip().split(";")
print(a)
