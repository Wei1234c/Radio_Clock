class Segment:
    SECOND_RANGE_START = None
    SECOND_RANGE_END = None
    WEIGHTS = None


    @classmethod
    def seconds(cls):
        return cls.SECOND_RANGE_END - cls.SECOND_RANGE_START


    @classmethod
    def get_bits(cls, value):
        bits = []

        for weight in cls.WEIGHTS:
            bit = 0 if weight == 0 else int(value >= weight)
            value = value - bit * weight
            bits.append(bit)

        return bits


    @classmethod
    def get_value(cls, bits):
        return sum([bit * weight for bit, weight in zip(bits, cls.WEIGHTS)])



class Year(Segment):
    SECOND_RANGE_START = 41
    SECOND_RANGE_END = 49
    WEIGHTS = (80, 40, 20, 10, 8, 4, 2, 1)


    @classmethod
    def get_bits(cls, value):
        return super().get_bits(value % 100)


    @classmethod
    def get_value(cls, bits, centry = 2000):
        return sum([bit * weight for bit, weight in zip(bits, cls.WEIGHTS)]) + centry



class Hours(Segment):
    SECOND_RANGE_START = 12
    SECOND_RANGE_END = 19
    WEIGHTS = (20, 10, 0, 8, 4, 2, 1)



class Minutes(Segment):
    SECOND_RANGE_START = 1
    SECOND_RANGE_END = 9
    WEIGHTS = (40, 20, 10, 0, 8, 4, 2, 1)



class Day_of_Year(Segment):
    SECOND_RANGE_START = 22
    SECOND_RANGE_END = 34
    WEIGHTS = (200, 100, 0, 80, 40, 20, 10, 8, 4, 2, 1)



class Day_of_Week(Segment):
    SECOND_RANGE_START = 50
    SECOND_RANGE_END = 53
    WEIGHTS = (4, 2, 1)
