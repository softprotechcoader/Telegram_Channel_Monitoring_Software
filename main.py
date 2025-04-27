import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget, QInputDialog
from excel_handler import generate_empty_excel, load_excel
import asyncio
from telegram_handler import main as telegram_main
from qasync import QEventLoop, QApplication as QAsyncApplication

class TelegramAutomationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Automation")
        self.setGeometry(100, 100, 400, 200)

        # Layout and widgets
        layout = QVBoxLayout()

        self.label = QLabel("Select an Excel file or generate a new one.")
        layout.addWidget(self.label)

        self.generate_button = QPushButton("Generate Empty Excel")
        self.generate_button.clicked.connect(self.generate_excel)
        layout.addWidget(self.generate_button)

        self.load_button = QPushButton("Load Excel File")
        self.load_button.clicked.connect(self.load_excel_file)
        layout.addWidget(self.load_button)

        self.start_button = QPushButton("Start Automation")
        self.start_button.clicked.connect(self.start_automation)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.accounts = None

    def generate_excel(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx)", options=options)
        if file_path:
            generate_empty_excel(file_path)
            self.label.setText(f"Empty Excel file generated at: {file_path}")

    def load_excel_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)", options=options)
        if file_path:
            try:
                self.accounts = load_excel(file_path).to_dict(orient='records')
                self.label.setText(f"Loaded Excel file: {file_path}")
            except ValueError as e:
                self.label.setText(str(e))

    def start_automation(self):
        if self.accounts:
            self.label.setText("Starting Telegram automation...")
            loop = asyncio.get_event_loop()
            loop.create_task(self.run_telegram_automation())
        else:
            self.label.setText("Please load a valid Excel file first.")

    async def run_telegram_automation(self):
        async def get_login_code(phone_number):
            code, ok = QInputDialog.getText(self, "Login Code", f"Enter the login code for {phone_number}:")
            if ok and code:
                return code
            else:
                return None

        await telegram_main(self.accounts, get_login_code)

if __name__ == "__main__":
    app = QAsyncApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = TelegramAutomationApp()
    window.show()

    with loop:
        loop.run_forever()