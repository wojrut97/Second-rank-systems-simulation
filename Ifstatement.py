import TransferFunction

class Ifstatement:
    @staticmethod
    def hurwitz_stability_check(data):
        det1 = data["a1"] - data["a2"]*data["a3"]
        det2 = -data["a1"]*(data["a0"]*data["a3"]+det1)
        det3 = -data["a1"]*data["a0"] - det2
        if data["a3"] > 0 and det1 > 0 and det2 > 0 and det3 > 0:               #Stabliny
            return 1
        if data["a3"] < 0 or det1 < 0 or det2 < 0 or det3 < 0:
            return -1                                                        #Granica stabilności
        return 0                                                           #Niestabilny

    @staticmethod
    def routh_stability_check(data):
        if data['a3'] > 0 and data['a2'] > 0 and data['a1'] > 0 and data['a0'] > 0:
            return True
        return False
    @staticmethod
    def is_integer(value):
        if isinstance(value, int):
            return True
        return False








