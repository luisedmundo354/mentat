import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from queue import Queue
from services.stt_service import start_file_transcription

class FileUploadWidget(tk.Frame):
    """
    A tkinter widget that allows the user to upload a recording file.
    """
    def __init__(self, parent, on_transcription_start_callback=None, text_widget=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.on_transcription_start_callback = on_transcription_start_callback
        
        # Button for uploading a file.
        self.upload_button = tk.Button(self, text="Upload Recording", command=self.upload_file, width=20)
        self.upload_button.pack(padx=5, pady=5)
        
        # Use the provided text_widget reference.
        self.text_widget = text_widget
        self.transcription_queue = None

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Recording File",
            filetypes=[("Audio Files", "*.wav *.mp3 *.m4a *.flac"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                # Clear the existing text in the provided widget.
                self.text_widget.delete("1.0", tk.END)
                
                # Create a new queue for transcription output.
                self.transcription_queue = Queue()
                
                # Start the file transcription process.
                start_file_transcription(self.transcription_queue, file_path=file_path)
                
                # Update UI via callback.
                if self.on_transcription_start_callback:
                    self.on_transcription_start_callback()
                
                # Begin live updating of the transcription output.
                self.update_text()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process the file:\n{e}")

    def update_text(self):
        try:
            while not self.transcription_queue.empty():
                transcription_chunk = self.transcription_queue.get_nowait()
                self.text_widget.insert(tk.END, transcription_chunk + "\n")
                self.text_widget.see(tk.END)
        except Exception as e:
            print("Error updating text:", e)
        self.parent.after(100, self.update_text)
