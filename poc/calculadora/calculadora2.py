
import sys

class calculator:
    #La calculadora solo acepta numeros enteros
    def __init__(self, primerNumero, operador, segundoNumero):
        self.firstNumber=int(primerNumero)
        self.secondNumber=int(segundoNumero)
        self.operator=operador
        self.validOperators=["+","-","*","/"]

    #Retorna true si es una operacion valida, sino false
    def isValidOperation(self):
        for i in self.validOperators:
            if i==self.operator:
                return True
        return False

    def isSum(self):
        return self.operator == "+"

    def addition(self):
        return self.firstNumber + self.secondNumber

    def isSubtraction(self):
        return self.operator == "-"

    def subtraction(self):
        return self.firstNumber - self.secondNumber

    def isMultiplication(self):
        return self.operator == "*"

    def multiplication(self):
        return self.firstNumber * self.secondNumber

    def isValidDivision(self):
        return self.secondNumber != 0

    def isDivision(self):
        return self.operator == "/"

    def division(self):
        return self.firstNumber / self.secondNumber

    #Obtiene el resultado de la operacion
    def operation(self):
        if self.isValidOperation():
            if self.isSum():
                return self.addition()
            elif self.isSubtraction():
                return self.subtraction()
            elif self.isMultiplication():
                return self.multiplication()
            elif self.isDivision() and self.isValidDivision():
                return self.division()
            else:
                return "Invalid Operation"
        else:
            return "Invalid Operation"

def main():
    c=calculator(sys.argv[1],sys.argv[2],sys.argv[3])
    print(c.operation())

if __name__ == '__main__':
    main()
