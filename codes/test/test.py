from radio_clock.jjy import *


ts = time.localtime()
ts = time.strptime('{}-{} {}:{}'.format(ts.tm_year, ts.tm_yday, ts.tm_hour, ts.tm_min), '%Y-%j %H:%M')
t = time.mktime(ts)
print(ts)

print(Encoder.get_time_code(t))

bits = Encoder.get_bits(t)
print(bits)

print(Encoder.get_symbols(t))

t1 = Decoder.get_time(bits)
print(t1 == t)
