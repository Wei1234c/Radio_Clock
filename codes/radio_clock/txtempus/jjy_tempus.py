def to_padded5_bcd(n):
    return (int((n / 100) % 10) << 10) | (int((n / 10) % 10) << 5) | (n % 10)



def to_bcd(n):
    return (int((n / 100) % 10) << 8) | (int((n / 10) % 10) << 4) | (n % 10)



def parity(d, from_, to_including):
    result = 0
    for bit in range(from_, to_including + 1):
        if (d & (1 << bit)):
            result += 1
    return result & 0x1



def PrepareMinute(t):
    # (year, month, month_day, hour, minute, second, week_day, year_day) = local_time
    time_bits_ = 0
    time_bits_ |= to_padded5_bcd(t.tm_min) << (59 - 8)
    time_bits_ |= to_padded5_bcd(t.tm_hour) << (59 - 18)
    time_bits_ |= to_padded5_bcd(t.tm_yday + 1) << (59 - 33)
    time_bits_ |= to_bcd(t.tm_year % 100) << (59 - 48)
    time_bits_ |= to_bcd(t.tm_wday) << (59 - 52)

    time_bits_ |= parity(time_bits_, 59 - 18, 59 - 12) << (59 - 36)
    time_bits_ |= parity(time_bits_, 59 - 8, 59 - 1) << (59 - 37)

    return bin(time_bits_)

