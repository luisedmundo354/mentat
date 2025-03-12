import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from queue import Queue
from services.stt_service import start_transcription
from services.report_generation_service import generate_report
from services.text_miner import mine_text

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set an initial 16:9 resolution (e.g. 1280x720)
        self.geometry("1280x720")
        self.title("Mentat")
        self.configure_grid()
        self.create_widgets()
        self.recording = False

    def configure_grid(self):
        # Configure grid weights to allow responsiveness.
        self.grid_rowconfigure(2, weight=1)  # The text widget row will expand
        self.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        # Title label at the top.
        self.label = tk.Label(self, text="Welcome to Mentat!", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        # Controls frame for recording buttons.
        self.controls_frame = tk.Frame(self)
        self.controls_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(1, weight=1)
        self.controls_frame.grid_columnconfigure(2, weight=1)

        self.start_button = tk.Button(self.controls_frame, text="Start Recording", command=self.on_start_recording, width=20)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(self.controls_frame, text="Pause", command=self.on_pause, width=20, state=tk.DISABLED)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.stop_button = tk.Button(self.controls_frame, text="Stop Recording", command=self.on_stop_recording, width=20, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=2, padx=5)

        # Exit button at the bottom.
        self.exit_button = tk.Button(self, text="Exit", command=self.on_exit, width=20)
        self.exit_button.grid(row=3, column=0, pady=10)

    def on_start_recording(self):
        """
        Start the transcription process and enable pause/stop controls.
        """
        self.recording = True
        
        # Create a ScrolledText widget and set it to expand.
        self.text_widget = ScrolledText(self, wrap=tk.WORD)
        self.text_widget.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        
        # Create a queue for transcription output.
        self.transcription_queue = Queue()
        start_transcription(self.transcription_queue)
        self.update_text()
        
        # Update button states.
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)

    def on_pause(self):
        """
        Pause the recording (logic depends on your transcription service).
        """
        self.recording = False
        messagebox.showinfo("Paused", "Recording paused. When ready, press Stop to generate the report.")

    def on_stop_recording(self):
        """
        Stop the recording, generate the report, and prompt for database update.
        """
        self.recording = False
        # (Stop the transcription thread if needed.)
        # Save what has been recorded in a file
        # Generate report using an external service.
        report_data = generate_report()  # Expected to return a dict: {'title': ..., 'summary': ..., 'details': ..., 'file_name': ...}
        self.display_report(report_data)

        # Ask if the user wants to update the database.
        if messagebox.askyesno("Database Update", "Do you want to update the database information?"):
            self.update_database_info()

        # Reset the interface.
        self.reset_state()
        messagebox.showinfo("Report Saved")

    def display_report(self, report_data):
        """
        Display the generated report in a new, responsive window.
        """
        report_window = tk.Toplevel(self)
        report_window.title("Generated Report")
        report_window.geometry("800x600")
        report_window.grid_rowconfigure(0, weight=1)
        report_window.grid_columnconfigure(0, weight=1)

        text_area = ScrolledText(report_window, wrap=tk.WORD)
        text_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        report_content = (
            f"Title: {report_data['title']}\n\n"
            f"Summary:\n{report_data['summary']}\n\n"
            f"Report:\n{report_data['report']}\n"
        )
        text_area.insert(tk.END, report_content)
        text_area.config(state=tk.DISABLED)

    def update_database_info(self):
        """
        Retrieve database update fields and display them for user confirmation.
        """
        update_fields = mine_text()  # Expected to return a dict: {field_name: current_value, ...}

        update_window = tk.Toplevel(self)
        update_window.title("Update Database Fields")
        update_window.geometry("600x400")

        # Use grid layout for dynamic resizing.
        update_window.grid_columnconfigure(1, weight=1)

        entries = {}
        row = 0
        for field, value in update_fields.items():
            tk.Label(update_window, text=field).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(update_window)
            entry.insert(0, value)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            entries[field] = entry
            row += 1

        def confirm_update():
            updated_data = {field: entry.get() for field, entry in entries.items()}
            # Call your update_database function here if needed.
            messagebox.showinfo("Update", "Database fields updated!")
            update_window.destroy()

        def cancel_update():
            messagebox.showinfo("Cancelled", "No changes made to the database.")
            update_window.destroy()

        tk.Button(update_window, text="Yes, update these fields", command=confirm_update).grid(row=row, column=0, padx=5, pady=10)
        tk.Button(update_window, text="No, cancel", command=cancel_update).grid(row=row, column=1, padx=5, pady=10)

    def reset_state(self):
        """
        Reset the interface to its initial state.
        """
        if hasattr(self, 'text_widget'):
            self.text_widget.destroy()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    def update_text(self):
        """
        Poll the transcription queue and update the text widget.
        """
        while not self.transcription_queue.empty():
            text = self.transcription_queue.get()
            self.text_widget.insert(tk.END, text + "\n")
            self.text_widget.see(tk.END)
        self.after(100, self.update_text)

    def on_exit(self):
        """
        Exit the application.
        """
        self.destroy()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()