# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import ply.lex as lex
import ply.yacc as yacc
import random

tokens = [
    'NUMBER',
    'BASE'
]
results = [] 

# Reglas léxicas
#una regla de token en PLY (Python Lex-Yacc) utilizada para identificar y manejar tokens que representan números en un análisis léxico
def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)  # Convertir a entero
    return t

def t_BASE(t):
    r'Hexadecimal|Octal|Binario|Romano|Aleatoreo|Base3'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t\n'

# Error léxico
#Esta función se define como un manejador para errores léxicos. En PLY, los prefijos t_ se utilizan para designar funciones relacionadas con tokens.
def t_error(t):
    print(f"Error léxico: Carácter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

## La producción gramatical conversions : conversion | conversions conversion indica que una secuencia de conversion puede ser una única conversion o múltiples conversiones concatenadas.
def p_conversions(p):
    '''
    conversions : conversion
                | conversions conversion
    '''
    pass

# callback utilizado en un parser generado por PLY (Python Lex-Yacc) para procesar la producción gramatical definida por la regla conversion : NUMBER BASE
def p_conversion(p):
    '''
    conversion : NUMBER BASE
    '''
    print(p)
    number = p[1]
    base = p[2]
    original_base = "Decimal"  # Base original es decimal por defecto
    result = convert(number, base)
    results.append(f"({original_base}) {number} = ({base}) {result}")




def convert(number, base):
    if base == 'Aleatoreo':
        bases = ['Hexadecimal','Octal','Binario','Romano','Base3']
        base = bases[random.randint(0, 100)%4]
          
    if base == 'Hexadecimal':
        return hex(number)
    elif base == 'Octal':
        return oct(number)
    elif base == 'Binario':
        return bin(number)
    elif base == 'Romano':
            roman_numerals = [
                (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
                (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
                (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
            ]
            roman = ''
            for value, symbol in roman_numerals:
                while number >= value:
                    roman += symbol
                    number -= value
            return roman
    elif base == "Base3":
            if number == 0:
                return "0"  

            result = ""
            n = abs(number)

            while n > 0:
                remainder = n % 3
                result = str(remainder) + result
                n //= 3
            return result

            



class Ui_lexer(object):
    def setupUi(self, lexer):
        self.input_string =""
        lexer.setObjectName("lexer")
        lexer.resize(714, 512)
        self.pushButton = QtWidgets.QPushButton(lexer)
        self.pushButton.setGeometry(QtCore.QRect(600, 10, 101, 51))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./magnifying-glass-chart-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.analyze)
        self.syntaxAnalyzer = QtWidgets.QListWidget(lexer)
        self.syntaxAnalyzer.setGeometry(QtCore.QRect(450, 250, 251, 251))
        self.syntaxAnalyzer.setObjectName("listWidget1")
        self.pushButton_2 = QtWidgets.QPushButton(lexer)
        self.pushButton_2.setGeometry(QtCore.QRect(600, 90, 101, 51))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./tree-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(lexer)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 172, 101, 51))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./folder-open-regular.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.openFileDialog)
        self.documentContent = QtWidgets.QListWidget(lexer)
        self.documentContent.setGeometry(QtCore.QRect(10, 10, 571, 211))
        self.documentContent.setObjectName("listWidget")
        self.lexicalAnalysis = QtWidgets.QTableWidget(lexer)
        self.lexicalAnalysis.setGeometry(QtCore.QRect(10, 250, 450, 251))
        self.lexicalAnalysis.setMinimumSize(QtCore.QSize(411, 0))
        self.lexicalAnalysis.setMaximumSize(QtCore.QSize(411, 16777215))
        self.lexicalAnalysis.setObjectName("tableWidget")
        self.lexicalAnalysis.setColumnCount(4)
        self.lexicalAnalysis.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.lexicalAnalysis.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.lexicalAnalysis.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.lexicalAnalysis.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.lexicalAnalysis.setHorizontalHeaderItem(3, item)

        self.retranslateUi(lexer)
        QtCore.QMetaObject.connectSlotsByName(lexer)
     #se utiliza para realizar un análisis léxico y sintáctico de una cadena de entrada utilizando PLY (Python Lex-Yacc)
    def analyze(self):

        self.lexicalAnalysis.clear()  
        self.syntaxAnalyzer.clear()
        headers = ["Tipo", "Valor", "Linea","Posicion"]
        self.lexicalAnalysis.setHorizontalHeaderLabels(headers)
 
        # Construir el lexer
        lexer = lex.lex()

        # Construir el parser
        parser = yacc.yacc()

        lexer.input(self.input_string)

        
        row = 0

        for token in lexer:
            self.lexicalAnalysis.insertRow(row)
            self.lexicalAnalysis.setItem(row, 0, QtWidgets.QTableWidgetItem(token.type))
            self.lexicalAnalysis.setItem(row, 1, QtWidgets.QTableWidgetItem(str(token.value)))
            #token.lineno
            self.lexicalAnalysis.setItem(row, 2, QtWidgets.QTableWidgetItem(str(row + 1 )))
            self.lexicalAnalysis.setItem(row, 3, QtWidgets.QTableWidgetItem(str(token.lexpos)))
            row += 1
        # iniciar el proceso de análisis sintáctico utilizando un parser generado por PLY
        parser.parse(self.input_string)

        for result in results:
            self.syntaxAnalyzer.addItem(result)
        results.clear()
    def openFileDialog(self):
        self.input_string =""
        self.documentContent.clear()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog  

        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("Archivos de Texto (*.txt)")
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            try:
                with open(selected_file, 'r') as doc:
                    self.input_string = doc.read()
                lines = self.input_string.split('\n')
                for line in lines:
                        self.documentContent.addItem(line)
            except FileNotFoundError:
                print(f"El archivo '{selected_file}' no se encontró.")

            except IOError:
                print(f"No se pudo leer el archivo '{selected_file}'.")

    def retranslateUi(self, lexer):
        _translate = QtCore.QCoreApplication.translate
        lexer.setWindowTitle(_translate("lexer", "Lexer Parser"))
        self.pushButton.setText(_translate("lexer", "Analizar"))
        self.pushButton_2.setText(_translate("lexer", "Generar arbol"))
        self.pushButton_3.setText(_translate("lexer", "Cargar archivo"))
        item = self.lexicalAnalysis.horizontalHeaderItem(0)
        item.setText(_translate("lexer", "Tipo"))
        item = self.lexicalAnalysis.horizontalHeaderItem(1)
        item.setText(_translate("lexer", "Valor"))
        item = self.lexicalAnalysis.horizontalHeaderItem(2)
        item.setText(_translate("lexer", "Linea"))
        item = self.lexicalAnalysis.horizontalHeaderItem(3)
        item.setText(_translate("lexer", "Posicion"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    lexer = QtWidgets.QWidget()
    ui = Ui_lexer()
    ui.setupUi(lexer)
    lexer.show()
    sys.exit(app.exec_())
