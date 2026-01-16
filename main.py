import cv2
from pyzbar.pyzbar import decode
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
from datetime import datetime

# Allowed scan types
ALLOWED_TYPES = {"CODE_128", "CODE_39", "DATA_MATRIX", "PDF_417", "AZTEC", "QRCODE"}

class ScannerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Barcode/QR Scanner")
        self.geometry("1920x1080")

        self.cam_index = 0
        self.running = True

        # For repeat logic
        self.last_code = None
        self.repeat_count = 0

        # Toolbar
        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=10, pady=(10, 0))

        swap_button = ctk.CTkButton(toolbar, text="Swap Camera", command=self.swap_camera)
        swap_button.pack(side="left", padx=5)

        # Main Layout
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Video display
        self.video_label = ctk.CTkLabel(main_frame, text="")
        self.video_label.grid(row=0, column=0, sticky="nsew", padx=10)

        # Right side logs
        logs_frame = ctk.CTkFrame(main_frame)
        logs_frame.grid(row=0, column=1, sticky="ns", padx=10)

        self.recent_label = ctk.CTkLabel(logs_frame, text="Recent: None", font=("Arial", 16))
        self.recent_label.pack(pady=(0,5))

        self.log_box = ctk.CTkTextbox(logs_frame, width=350)
        self.log_box.pack(fill="y", expand=True)

        self.log("Scanner Initialized...")

        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.cap = None
        self.start_camera(self.cam_index)

    # ---------- Logging ----------
    def log(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("0.0", f"[{timestamp}] {text}\n")
        self.recent_label.configure(text=f"Recent: {text}")

    # ---------- Camera Swap ----------
    def swap_camera(self):
        self.cam_index += 1
        self.log(f"Switching to camera {self.cam_index}")
        self.start_camera(self.cam_index)

    def start_camera(self, index):
        if self.cap:
            self.cap.release()

        self.cap = cv2.VideoCapture(index)

        if not self.cap.isOpened():
            self.log(f"Camera {index} not available, reverting to 0")
            self.cam_index = 0
            self.cap = cv2.VideoCapture(0)

        threading.Thread(target=self.update_frame, daemon=True).start()

    # ---------- Video Loop ----------
    def update_frame(self):
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Convert to grayscale for black & white
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # Convert back to 3 channels for pyzbar

            detections = decode(frame)

            if detections:
                barcode = detections[0]
                data = barcode.data.decode("utf-8")
                btype = barcode.type.upper()

                # Log detection always
                self.log(f"Detected {btype}: {data}")

                x, y, w, h = barcode.rect

                if btype in ALLOWED_TYPES:
                    # Repeat logic
                    if data == self.last_code:
                        if self.repeat_count < 3:
                            self.repeat_count += 1
                            self.log(f"{btype}: {data} ({self.repeat_count}/3)")
                    else:
                        self.last_code = data
                        self.repeat_count = 1
                        self.log(f"{btype}: {data} (1/3)")

                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)  # Red box for detection

                else:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)  # Green box for ignored

            else:
                # Reset when no code visible
                self.last_code = None
                self.repeat_count = 0

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(rgb))
            self.video_label.configure(image=imgtk)
            self.video_label.imgtk = imgtk

    # ---------- Shutdown ----------
    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = ScannerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
