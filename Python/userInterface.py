import sys
import PyQt6.QtCore as qtCore
import PyQt6.QtWidgets as qtWidgets

class App(qtCore.QThread) :
    
    def __init__(self):
        
        return
    
    def createMenu(self):
        
        return

def launchApp():
    
    app = qtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())