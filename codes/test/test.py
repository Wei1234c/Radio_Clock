from radio_clock.txtempus.jjy_tempus import *

import time
t = time.localtime()

bits = PrepareMinute(t)

print(bits)