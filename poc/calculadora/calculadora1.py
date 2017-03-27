import sys
#Esta calculadora solo acepta numeros enteros
class Calculator:
	def __init__(self,num1,operator,num2):
		self.oneNumber=num1
		self.twoNumber=num2
		self.operator=operator
		self.validOperator=["+","-","/","*"]

	#Primero verifico que el operador sea un operador valido de la calculadora
	#Luego verifico que los los atributos sean numeros enteros 
	def isValid(self):
		return self.operator in self.validOperator and (self.oneNumber.isdigit() and self.twoNumber.isdigit())


	def operar(self):
		if self.isValid():
			print( eval(self.oneNumber + self.operator + self.twoNumber ))
		else:
			print("Error: por favor ingrese un numero un, operador y otro numero separado por espacio")

def main():

	c=Calculator(sys.argv[1],sys.argv[2],sys.argv[3])
	print(c.operar())

if __name__ == '__main__':
	main()
