from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QListWidget

class NobuToolWindow:
    nobuFuncList = ["功能一","功能一","功能一"]
    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load("ui/nobutool_Main.ui")
        # 將你的函數連接到按鈕點擊訊號上
        self.ui.confirmBtn.clicked.connect(self.say_hello)

        self.ui.funcWidget.addItems(self.nobuFuncList)
        self.ui.funcWidget.currentRowChanged.connect(self.funcItemChange)

    def say_hello(self):
        self.ui.chLabel.setText("Hello~~~")
    
    def funcItemChange(self, index):
        self.ui.chLabel.setText(f"index {index}, {self.ui.funcWidget.item(index).text()}")

if __name__ == '__main__':

    loader = QUiLoader()
    app = QApplication([])

    nbtool_window = NobuToolWindow()
    nbtool_window.ui.show()
    app.exec()