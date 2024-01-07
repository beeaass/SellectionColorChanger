import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QColorDialog, QDesktopWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QIcon
import os
import json
import ctypes

def validate_color(color):
    if len(color) % 3 != 0:
        return False
    for i in range(0, len(color), 3):
        value = color[i:i+3]
        try:
            value = int(value)
            if value < 0 or value > 255:
                return False
        except ValueError:
            return False
    return True

def save_changes(hilight_color, hottracking_color):
    hilight_color = hilight_color.replace(" ", "")
    hottracking_color = hottracking_color.replace(" ", "")
    if not validate_color(hilight_color) or not validate_color(hottracking_color):
        return "Invalid color format", QColor("red")
    hilight_color = ' '.join([hilight_color[i:i+3] for i in range(0, len(hilight_color), 3)])
    hottracking_color = ' '.join([hottracking_color[i:i+3] for i in range(0, len(hottracking_color), 3)])
    try:
        ctypes.windll.shell32.SystemParametersInfoW(20, 0, hilight_color, 3)
        ctypes.windll.shell32.SystemParametersInfoW(20, 0, hottracking_color, 3)
        return "Changes saved", QColor("green")
    except OSError:
        return "Failed to save changes", QColor("red")

class CustomButton(QPushButton):
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(QColor(70, 130, 180))
        painter.setPen(Qt.NoPen)

        rect = self.rect()
        rect.setWidth(rect.width() - 5)
        rect.setHeight(rect.height() - 5)
        painter.drawRoundedRect(rect, 10, 10)

        painter.setPen(QColor("black"))
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, self.text())

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Selection Color Changer')
        self.setWindowIcon(QIcon('C:\\Users\\sasch\\Desktop\\allegryyyProject\\SellectionColorChanger\\icon\\16x16.ico'))
        self.setFixedSize(524, 350)
        self.center()

        self.hilight_label = QLabel('Highlight (RGB):', self)
        self.hilight_label.setAlignment(Qt.AlignCenter)
        self.hilight_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.hilight_entry = QLineEdit(self)
        self.hilight_entry.setPlaceholderText("255 255 255")
        self.hilight_entry.setAlignment(Qt.AlignCenter)
        self.hilight_entry.setStyleSheet("font-size: 20px; padding: 10px; color: black; background-color: #FFFFFF;")
        self.hilight_color_button = CustomButton('Choose Color', self)
        self.hilight_color_button.clicked.connect(lambda: self.open_color_dialog(self.hilight_entry))
        self.hottracking_label = QLabel('HotTrackingColor (RGB):', self)
        self.hottracking_label.setAlignment(Qt.AlignCenter)
        self.hottracking_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.hottracking_entry = QLineEdit(self)
        self.hottracking_entry.setPlaceholderText("255 255 255")
        self.hottracking_entry.setAlignment(Qt.AlignCenter)
        self.hottracking_entry.setStyleSheet("font-size: 20px; padding: 10px; color: black; background-color: #FFFFFF;")
        self.hottracking_color_button = CustomButton('Choose Color', self)
        self.hottracking_color_button.clicked.connect(lambda: self.open_color_dialog(self.hottracking_entry))
        self.status_label = QLabel('', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont('Arial', 14, QFont.Bold))
        self.button_save = CustomButton('Save Profile', self)
        self.button_save.clicked.connect(self.save_profile)
        self.button_reset = CustomButton('Default', self)
        self.button_reset.clicked.connect(self.reset_changes)
        self.button_apply = CustomButton('Apply', self)
        self.button_apply.clicked.connect(self.apply_changes)
        self.button_load = CustomButton('Load Profile', self)
        self.button_load.clicked.connect(self.load_profile)
        self.copyright_label = QLabel('© allegryyy', self)
        self.copyright_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.copyright_label.setAlignment(Qt.AlignLeft)

        hbox = QHBoxLayout()
        hbox.addWidget(self.button_save)
        hbox.addWidget(self.button_apply)
        hbox.addWidget(self.button_reset)
        hbox.addWidget(self.button_load)

        vbox = QVBoxLayout()
        vbox.addWidget(self.hilight_label)
        vbox.addWidget(self.hilight_entry)
        vbox.addWidget(self.hilight_color_button)
        vbox.addWidget(self.hottracking_label)
        vbox.addWidget(self.hottracking_entry)
        vbox.addWidget(self.hottracking_color_button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.status_label)
        vbox.addWidget(self.copyright_label)

        self.setLayout(vbox)
        self.setStyleSheet("background-color: #FFFFFF; color: black;")

        self.show()

    def open_color_dialog(self, line_edit):
        color = QColorDialog.getColor()
        if color.isValid():
            line_edit.setText(f"{color.red():03} {color.green():03} {color.blue():03}")

    def reset_changes(self):
        try:
            ctypes.windll.shell32.SystemParametersInfoW(20, 0, "0 120 215", 3)
            ctypes.windll.shell32.SystemParametersInfoW(20, 0, "0 102 204", 3)
            self.status_label.setText("Reset successful")
            self.status_label.setStyleSheet("color: green")
            self.show_restart_dialog()
        except OSError:
            self.status_label.setText("Failed to reset changes")
            self.status_label.setStyleSheet("color: red")

    def apply_changes(self):
        hilight_color = self.hilight_entry.text()
        hottracking_color = self.hottracking_entry.text()
        if not hilight_color or not hottracking_color:
            self.status_label.setText("Fields cannot be empty")
            self.status_label.setStyleSheet("color: red")
            return
        status, color = save_changes(hilight_color, hottracking_color)
        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"color: {color.name()}")
        if status == "Changes saved":
            self.show_restart_dialog()

    def save_profile(self):
        hilight_color = self.hilight_entry.text()
        hottracking_color = self.hottracking_entry.text()
        if not hilight_color or not hottracking_color:
            self.status_label.setText("Fields cannot be empty")
            self.status_label.setStyleSheet("color: red")
            return
        profile = {"Hilight": hilight_color, "HotTrackingColor": hottracking_color}
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save Profile', os.getenv('HOME'), 'JSON Files (*.json)')
        if file_name:
            with open(file_name, 'w') as f:
                json.dump(profile, f)
            self.status_label.setText("Profile saved")
            self.status_label.setStyleSheet("color: green")

    def load_profile(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Load Profile', os.getenv('HOME'), 'JSON Files (*.json)')
        if file_name:
            with open(file_name, 'r') as f:
                profile = json.load(f)
            self.hilight_entry.setText(profile["Hilight"])
            self.hottracking_entry.setText(profile["HotTrackingColor"])
            self.status_label.setText("Profile loaded")
            self.status_label.setStyleSheet("color: green")

    def show_restart_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Do you want to restart your computer for the changes to take effect?")
        msg.setWindowTitle("Restart Required")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        retval = msg.exec_()
        if retval == QMessageBox.Yes:
            os.system('shutdown -r -t 0')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
