from . import *


class CellDataDialog(QDialog):
    def __init__(self, cell_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cell Data")
        self.setGeometry(100, 100, 400, 800)
        layout = QVBoxLayout()
        self.text_browser = QTextBrowser()
        self.text_browser.setHtml(self.format_cell_data(cell_data))
        layout.addWidget(self.text_browser)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)

    def format_cell_data(self, cell_data):
        html = "<h2>Cell Data</h2>"
        for key, value in cell_data.items():
            html += f"<p><strong>{key}:</strong> {value}</p>"
        return html