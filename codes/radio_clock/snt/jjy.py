# https://github.com/snt/rpi_jjy_server
# https://en.wikipedia.org/wiki/Radio_clock
# https://en.wikipedia.org/wiki/JJY


import datetime
import sched
import sys
import time

from RPIO import PWM as pwm  # *** RPIO is deprecated.***


JJY_FORMAT = "M{0:03b}0{1:04b}M00{2:02b}0{3:04b}M00{4:02b}0{5:04b}M{6:04b}00{10}{11}0M0{7:04b}{8:04b}M{9:03b}000000M"

IO_PIN = 4  # BCM4 = board 7
INCREMENT_US = 5
DMA_CHANNEL = 1



def pwm_setup():
    pwm.set_loglevel(pwm.LOG_LEVEL_ERRORS)
    pwm.setup(INCREMENT_US)
    pwm.init_channel(DMA_CHANNEL, 5000)



# M 200 [ms]
# 1 500 [ms]
# 0 800 [ms]
SIGNAL_LENGTHS = {'M': 0.2, '1': 0.5, '0': 0.8}

DEBUG = False



def send_signal(signal):
    for x in range(1, 1000, INCREMENT_US):
        pwm.add_channel_pulse(DMA_CHANNEL, IO_PIN, x, 3)
    time.sleep(SIGNAL_LENGTHS[signal])
    pwm.clear_channel_gpio(DMA_CHANNEL, IO_PIN)
    if DEBUG:
        sys.stdout.write(signal)
        sys.stdout.flush()



def schedule_next(scheduler):
    a = datetime.datetime.now() + datetime.timedelta(minutes = 1)
    next0sec = time.mktime(datetime.datetime(a.year, a.month, a.day, a.hour, a.minute, 0, 0).timetuple())
    ts = a.strftime('%M%H%j%y%w,%H,%M').split(',')
    data = [int(x) for x in ts[0]]
    parities = ["".join(["{:b}".format(int(x)) for x in ps]).count('1') % 2 for ps in ts[1:]]
    signals = JJY_FORMAT.format(*(data + parities))
    for i, signal in enumerate(signals):
        scheduler.enterabs(next0sec + i, 1, send_signal, (signal,))
    scheduler.enterabs(next0sec, 1, schedule_next, (scheduler,))
    print(datetime.datetime.now())



def main():
    pwm_setup()
    scheduler = sched.scheduler(time.time, time.sleep)
    schedule_next(scheduler)
    scheduler.run()
    print("schedule empty")



if __name__ == '__main__':
    main()
