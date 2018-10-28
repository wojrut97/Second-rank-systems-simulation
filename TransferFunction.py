
integralStep = 0.001
whereWeAre = 0
output = []

class TransferFunction:

    data = None
    def value_check(self):
        for value in self.template:
            if value not in self.data.keys():
                print("missing parameters from input")
                return False
        return True

    def get_data(self):
        return self.data

    def __init__(self, data):
        if data is not None:
            self.data = data
            self.value_check()

    @staticmethod
    def read_dictionary( b0, a0, a1, a2, a3):
        dictionary = {"b0": b0, "a3": a3, "a2": a2, "a1": a1, "a0": a0}
        value = dictionary.values()
        print("sector clear")
        return dictionary

    def state_model(self, data):
        A = [[0,1,0,0],
             [0,0,1,0],
             [0,0,0,1],
             [-data["a0"], -data["a1"], -data["a2"], -data["a3"]]]
        bonk = 0
        return bonk

    @staticmethod
    def liczenie_rzeczy_rurznych(stateVariable, transParam, signal):

        x4prim = -(transParam["a0"]* stateVariable["x1"]) - (transParam["a1"]* stateVariable["x2"]) -(transParam["a2"] * stateVariable["x3"]) - (transParam["a3"] * stateVariable["x4"]) + signal
        stateVariable["x4"] = integralStep * x4prim
        x3prim = stateVariable["x4"]
        stateVariable["x3"] = integralStep * x3prim
        x2prim = stateVariable["x3"]
        stateVariable["x2"] = integralStep * x2prim
        x1prim = stateVariable["x2"]
        stateVariable["x1"] = integralStep * x1prim
        return stateVariable["x1"]


