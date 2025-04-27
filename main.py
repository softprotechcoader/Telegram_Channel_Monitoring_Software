import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget, QInputDialog, QScrollArea, QTextEdit
from PyQt5.QtCore import Qt
from excel_handler import generate_empty_excel, load_excel
import asyncio
from telegram_handler import main as telegram_main
from qasync import QEventLoop, QApplication as QAsyncApplication
import pandas as pd

class TelegramAutomationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Automation")
        self.setGeometry(100, 100, 800, 600)  # Adjusted for responsiveness

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

        self.abort_button = QPushButton("Abort Process")
        self.abort_button.clicked.connect(self.abort_process)
        layout.addWidget(self.abort_button)

        self.export_button = QPushButton("Export to Excel")
        self.export_button.clicked.connect(self.export_to_excel)
        layout.addWidget(self.export_button)

        # Scrollable area for displaying content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.scroll_area.setWidget(self.text_display)
        layout.addWidget(self.scroll_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.accounts = None
        self.abort_flag = False
        self.channel_content = []

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
            self.abort_flag = False
            loop = asyncio.get_event_loop()
            loop.create_task(self.run_telegram_automation())
        else:
            self.label.setText("Please load a valid Excel file first.")

    def abort_process(self):
        self.abort_flag = True
        self.label.setText("Process aborted.")

    def export_to_excel(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Excel File", "", "Excel Files (*.xlsx)", options=options)
        if file_path:
            # Prepare data for export
            data_by_date = {}
            channel_names = set()

            # Organize content by date and channel
            for entry in self.channel_content:
                date = entry["Date"].date() if isinstance(entry["Date"], pd.Timestamp) else entry["Date"]
                channel_name = entry["Channel Name"]
                content = entry["Content"]

                if date not in data_by_date:
                    data_by_date[date] = {}
                data_by_date[date][channel_name] = content
                channel_names.add(channel_name)

            # Sort dates and channels
            sorted_dates = sorted(data_by_date.keys())
            sorted_channels = sorted(channel_names)

            # Create a DataFrame for export
            export_data = []
            for date in sorted_dates:
                row = {"DATE": date}
                for channel in sorted_channels:
                    row[channel] = data_by_date[date].get(channel, "No Content")
                export_data.append(row)

            df = pd.DataFrame(export_data, columns=["DATE"] + sorted_channels)

            # Export to Excel
            df.to_excel(file_path, index=False)
            self.label.setText(f"Content exported to: {file_path}")

    async def run_telegram_automation(self):
        async def get_login_code(phone_number):
            code, ok = QInputDialog.getText(self, "Login Code", f"Enter the login code for {phone_number}:")
            if ok and code:
                return code
            else:
                return None

        async def monitor_channels_with_ui(client):
            async for dialog in client.iter_dialogs():
                if dialog.is_channel:
                    self.text_display.append(f"Monitoring channel: {dialog.name}")
                    async for message in client.iter_messages(dialog.id):
                        if self.abort_flag:
                            return
                        content = f"[{dialog.name}] {message.date}: {message.text}"
                        self.text_display.append(content)
                        self.channel_content.append({"Date": message.date, "Channel Name": dialog.name, "Content": message.text})

        await telegram_main(self.accounts, get_login_code, monitor_channels_with_ui)

if __name__ == "__main__":
    app = QAsyncApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = TelegramAutomationApp()
    window.show()

    with loop:
        loop.run_forever()