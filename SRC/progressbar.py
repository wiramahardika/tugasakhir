import sys
import time

print "start"
for i in range(10):
    sys.stdout.write("\r"+str(i))
    sys.stdout.flush()
    time.sleep(0.5)
sys.stdout.flush()
print "done"
