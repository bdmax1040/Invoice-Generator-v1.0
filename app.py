import sys
from PyQt6.QtWidgets import QApplication
from data.config import ensure_config, load_config, get_env

# Import the main app window and setup wizard
from ui.main.main import MainWindow
from ui.wizard.wizard import WizardWindow

def main():
    # Ensure config.json and .env exist
    ensure_config()

    # Load user config and env variables
    config = load_config()
    env = get_env()

    # Create Qt application
    app = QApplication(sys.argv)

    # Launch setup wizard or main window based on config
    if config.get("setup", {}).get("completed", False):
        print("Launching main window...")
        window = MainWindow(config, env)
    else:
        print("Launching setup wizard...")
        window = WizardWindow(config)

    # Show and execute app
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()