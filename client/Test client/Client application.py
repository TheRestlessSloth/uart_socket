import sys
import Client_application_new

from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow)

if hasattr(Client_application_new, 'Ui_MainWindow'):
    ui = Client_application_new.Ui_MainWindow()
else:
    ui = Client_application_new.Ui_Form()


if __name__ == '__main__':
    app = QApplication([])
    #win = uic.loadUi('Client_application_new.ui')
    win = QMainWindow()

    ui.setupUi(win)

    win.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window')