import Config

config = Config.getConfig()

class InstructionTable(object):

    def __init__(self, coefficients, q):
        self.q = q
        self.coefficients = coefficients

    def generateTable(self):
        degree = config.get("general", "features")
        table = []
        # TODO: add in G
        for i in range(1, degree + 1):
            table.append([i,
                          self.polynomial(self.coefficients, 2 * i),
                          self.polynomial(self.coefficients, 2 * i + 1)])
        return table

    def polynomial(self, base):
        result = 0
        exponent = 0
        for coefficient in self.coefficients:
            result += coefficient * pow(base, exponent)
            exponent += 1
        return result
