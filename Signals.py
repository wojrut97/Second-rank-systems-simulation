import math

class Signal:
    @staticmethod
    def sine(amplification, length, period):
        signal = []
        for temp in range(0, period*length):
            signal.append(amplification*math.sin((temp*2*math.pi)/period))
        return signal

    @staticmethod
    def rectangle(amplification, length, period):
        signal = []
        for temp in range(0, period*length):
            if temp % period < period/2:
                signal.append(amplification)
            else:
                signal.append(-amplification)
        return signal

    #@staticmethod
    # def triangle(amplification, length, period):
    #     signal = []
    #     for temp in range(0, period*length):
    #         if 0.25*period > temp % period > 0.75*period:
