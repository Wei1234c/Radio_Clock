from radio_clock.jjy.jjy import *


t = time_stamp = 1585870980.0


# print(Encoder.get_time_code(t))

bits = Encoder.get_bits(t)
print(bits)

print(Encoder.get_symbols(t))

t1 = Decoder.get_time(bits)
print(t1 == t)
