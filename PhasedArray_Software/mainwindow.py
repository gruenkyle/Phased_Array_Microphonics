from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QMenu, QToolButton
from PySide6.QtGui import QAction
import sys, subprocess, shutil, os
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize default values for input variables
        self.sad = None
        self.sod = None
        self.mic_count = None
        self.total_spread = None
        self.type = "VOICE"
        self.noise = "VOICE"

        # Connections
        self.ui.actionMenu.triggered.connect(self.import_py_file)
        self.ui.actionClear.triggered.connect(self.clear_console)
        self.ui.refreshList.clicked.connect(self.refresh_list)
        self.ui.saveButton.clicked.connect(self.save_settings)
        self.ui.deleteFile.clicked.connect(self.delete_selected_file)
        self.ui.recordButton.clicked.connect(self.record_live)

        # Initialize dropdowns for type and noise
        self.init_type_dropdown()
        self.init_noise_dropdown()

        # Load Python files from the recorder directory
        self.load_python_files()

    # Initialize the typeButton dropdown with specific options
    def init_type_dropdown(self):
        type_menu = QMenu(self)
        for option in ["VOICE", "TONE", "BACKGROUND"]:
            action = QAction(option, self)
            action.triggered.connect(lambda checked, opt=option: self.set_type(opt))
            type_menu.addAction(action)

        self.ui.typeButton.setMenu(type_menu)
        self.ui.typeButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.ui.typeButton.setText(self.type)  # Display default selection

    # Initialize the noiseButton dropdown with specific options
    def init_noise_dropdown(self):
        noise_menu = QMenu(self)
        for option in ["VOICE", "TONE", "BACKGROUND", "VOICE + BACKGROUND"]:
            action = QAction(option, self)
            action.triggered.connect(lambda checked, opt=option: self.set_noise(opt))
            noise_menu.addAction(action)

        self.ui.noiseButton.setMenu(noise_menu)
        self.ui.noiseButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.ui.noiseButton.setText(self.noise)  # Display default selection

    # Set the selected type and update button text
    def set_type(self, selected_type):
        self.type = selected_type.upper()
        self.ui.typeButton.setText(self.type)
        self.ui.consoleLog.append(f"Type set to: {self.type}")

    # Set the selected noise and update button text
    def set_noise(self, selected_noise):
        self.noise = selected_noise.upper()
        self.ui.noiseButton.setText(self.noise)
        self.ui.consoleLog.append(f"Noise set to: {self.noise}")

    # Clear Console
    def clear_console(self):
        self.ui.consoleLog.clear()

    # Importing .py file
    def import_py_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Python File", "", "Python Files (*.py)")
        if file_name:
            self.add_file_to_list_view(file_name)
            self.copy_file_to_recorder(file_name)

    # Add .py file to list view
    def add_file_to_list_view(self, file_name):
        item = QListWidgetItem(os.path.basename(file_name))
        item.setData(1000, file_name)
        self.ui.listView.addItem(item)

    # Copy .py file to pythonfiles directory
    def copy_file_to_recorder(self, file_name):
        destination_directory = os.path.abspath("pythonfiles")
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        destination_path = os.path.join(destination_directory, os.path.basename(file_name))
        shutil.copy(file_name, destination_path)
        self.load_python_files()

    # Load Python files at startup
    def load_python_files(self):
        self.ui.listView.clear()
        destination_directory = os.path.abspath("pythonfiles")
        if os.path.exists(destination_directory):
            for file_name in os.listdir(destination_directory):
                if file_name.endswith('.py'):
                    self.add_file_to_list_view(os.path.join(destination_directory, file_name))

    # Refresh list of files
    def refresh_list(self):
        self.load_python_files()
        self.ui.consoleLog.append("List Refreshed.")

    # Delete file
    def delete_selected_file(self):
        selected_item = self.ui.listView.currentItem()
        if selected_item is None:
            self.ui.consoleLog.append("No Selection: Please select a file to delete.")
            return

        file_path = selected_item.data(1000)
        if os.path.exists(file_path):
            os.remove(file_path)
            self.ui.listView.takeItem(self.ui.listView.row(selected_item))
            self.ui.consoleLog.append(f"Deleted: '{selected_item.text()}' has been deleted.")
        else:
            self.ui.consoleLog.append("Error: File not found.")

    # Save user inputs
    def save_settings(self):
        self.sad = int(self.ui.SAD.text())
        self.sod = int(self.ui.SOD.text())
        self.mic_count = int(self.ui.micCount.text())
        self.total_spread = int(self.ui.totalSpread.text())
        self.ui.consoleLog.append(
            f"Variables saved.\n\tSAD: {self.sad}\n\tSOD: {self.sod}\n\tMic Count: {self.mic_count}\n"
            f"\tTotal Spread: {self.total_spread}\n\tType: {self.type}\n\tNoise: {self.noise}"
        )

    def record_live(self):
        try:
            script_path = os.path.abspath(os.path.join("PhasedArray_Software", "pythonfiles", "wavCollection.py"))
            self.ui.consoleLog.append("Launching real-time recording script...")
            subprocess.Popen([sys.executable, script_path], shell=False)
        except Exception as e:
            self.ui.consoleLog.append(f"Error launching recording: {e}")

    # Run the selected script with user inputs 
    # THIS IS CURRENTLY NOT BEING USED SINCE RECORD USES wavCollection.py
    def run_script(self):
        selected_item = self.ui.listView.currentItem()

        # Ensure a file is selected
        if selected_item is None:
            self.ui.consoleLog.append("No Selection: Please select a Python file to run.")
            return

        # Absolute path of the selected script
        script_path = os.path.abspath(selected_item.data(1000))
        if not script_path.endswith('.py'):
            self.ui.consoleLog.append("Invalid File: The selected file is not a Python file.")
            return

        # Ensure that save_settings has been called and fields have values
        if None in [self.sad, self.sod, self.mic_count, self.total_spread]:
            self.ui.consoleLog.append("Error: Please save settings before running the script.")
            return

        # Convert integers to strings for subprocess arguments
        args = [
            str(self.sad),
            str(self.sod),
            str(self.mic_count),
            str(self.total_spread),
            self.type,
            self.noise
        ]

        # Log and verify the command
        command = [sys.executable, script_path] + args
        self.ui.consoleLog.append(f"Running command: {' '.join(command)}")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                cwd=os.path.dirname(script_path)  # Set working directory to script location
            )
            self.ui.consoleLog.append(result.stdout)
        except subprocess.CalledProcessError as e:
            self.ui.consoleLog.append(f"Error: {e.stderr}")
        except Exception as e:
            self.ui.consoleLog.append(f"Execution Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
