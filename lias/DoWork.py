import sys

import MainWindow


class DoWork:
    """
    Show the main window and do work
    """
    
    def __init__(self, spec):
        app = QtWidgets.QApplication(sys.argv)
        mainwin = MainWindow(spec)
        mainwin.show()
        sys.exit(app.exec_())
