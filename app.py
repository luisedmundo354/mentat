from config import CONFIG
from ui.main_window import MainWindow
from threading import Thread
import time

def auto_start_function():
    # Background task: runs continuously or periodically.
    while True:
        print("Background task running...")
        time.sleep(5)

def main():

    # Instantiate the main window from the ui module.
    app = MainWindow()
    
    # Start a background thread if needed.
    auto_thread = Thread(target=auto_start_function, daemon=True)
    auto_thread.start()
    
    # Start the Tkinter event loop.
    app.mainloop()

if __name__ == '__main__':
    main()