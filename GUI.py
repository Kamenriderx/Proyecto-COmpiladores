# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import ply.lex as lex
import ply.yacc as yacc

tokens = [
    'NUMBER',
    'BASE'
]
results = [] 

# Reglas léxicas
def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)  # Convertir a entero
    return t

def t_BASE(t):
    r'Hexadecimal|Octal|Binario|Romano'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t\n'

# Error léxico
def t_error(t):
    print(f"Error léxico: Carácter inesperado '{t.value[0]}'")
    t.lexer.skip(1)

def p_conversions(p):
    '''
    conversions : conversion
                | conversions conversion
    '''
    pass

def p_conversion(p):
    '''
    conversion : NUMBER BASE
    '''
    number = p[1]
    base = p[2]
    original_base = "Decimal"  # Base original es decimal por defecto
    result = convert(number, base)
    results.append(f"({original_base}) {number} = ({base}) {result}")




def convert(number, base):
    if base == 'Hexadecimal':
        return hex(number)
    elif base == 'Octal':
        return oct(number)
    elif base == 'Binario':
        return bin(number)
    elif base == 'Romano':
        return "Conversion to Roman"
    



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
        self.listWidget1 = QtWidgets.QListWidget(lexer)
        self.listWidget1.setGeometry(QtCore.QRect(450, 250, 251, 251))
        self.listWidget1.setObjectName("listWidget1")
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
        self.listWidget = QtWidgets.QListWidget(lexer)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 571, 211))
        self.listWidget.setObjectName("listWidget")
        self.tableWidget = QtWidgets.QTableWidget(lexer)
        self.tableWidget.setGeometry(QtCore.QRect(10, 250, 450, 251))
        self.tableWidget.setMinimumSize(QtCore.QSize(411, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(411, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)

        self.retranslateUi(lexer)
        QtCore.QMetaObject.connectSlotsByName(lexer)
    def analyze(self):
        self.tableWidget.setRowCount(0)  
        
        # Construir el lexer
        lexer = lex.lex()

        # Construir el parser
        parser = yacc.yacc()

        lexer.input(self.input_string)

        
        row = 0

        for token in lexer:
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(token.type))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(token.value)))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(token.lineno)))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(token.lexpos)))
            row += 1
        parser.parse(self.input_string)

        for result in results:
            self.listWidget1.addItem(result)

    def openFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog  # Opcional: Evitar el uso del diálogo nativo del sistema

        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("Archivos de Texto (*.txt)")
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        lineString= ""

        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            try:
                with open(selected_file, 'r') as doc:
                    self.input_string = doc.read()
                lines = self.input_string.split('\n')
                for line in lines:
                        self.listWidget.addItem(line)
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
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("lexer", "Tipo"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("lexer", "Valor"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("lexer", "Linea"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("lexer", "Posicion"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    lexer = QtWidgets.QWidget()
    ui = Ui_lexer()
    ui.setupUi(lexer)
    lexer.show()
    sys.exit(app.exec_())
