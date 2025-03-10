import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from queue import Queue
from services.stt_service import start_transcription

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mentat")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Create a label at the top of the window.
        self.label = tk.Label(self, text="Welcome to My App!", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Create a button to start a task.
        self.start_button = tk.Button(self, text="Start Task", command=self.on_start, width=20)
        self.start_button.pack(pady=10)

        # Create another button to exit the application.
        self.exit_button = tk.Button(self, text="Exit", command=self.on_exit, width=20)
        self.exit_button.pack(pady=10)

    def on_start(self):
        """
        Callback triggered when the 'Start Task' button is pressed.
        This function can call additional functions or start background processing.
        """
        print("Start Task button pressed!")
        messagebox.showinfo("Information", "Task is starting!")

        self.text_widget = ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.text_widget.pack(padx=10, pady=10)

        # Create a queue to receive transcription text from the background thread
        self.transcription_queue = Queue()

        # Start the transcription thread
        start_transcription(self.transcription_queue)

        # Start polling for transcription updates
        self.update_text()
        # You could call other functions or update widgets here

    def update_text(self):
        # Poll the queue and update the text widget if new transcription is available.
        while not self.transcription_queue.empty():
            text = self.transcription_queue.get()
            self.text_widget.insert(tk.END, text + "\n")
            self.text_widget.see(tk.END)
        # Schedule the next poll after 100 milliseconds
        self.after(100, self.update_text)

    def on_exit(self):
        """
        Callback for the 'Exit' button; closes the application.
        """
        self.destroy()
