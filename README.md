# Barcode/QR Scanner with Camera Swap & Logs

A Python application to scan barcodes and QR codes using your webcam, display a live camera feed, log scanned data, and show the most recent scan. Supports multiple barcode formats and allows switching between cameras.

---

## 📦 Features

* Scans barcodes and QR codes: `CODE_128`, `CODE_39`, `DATA_MATRIX`, `PDF_417`, `AZTEC`, `QRCODE`
* Live camera feed in **black & white** for better contrast
* Draws **red boxes** around detected codes
* Logs all scanned codes and shows the **most recent log entry**
* Limits logging the same code to **3 repeats**
* Supports **camera swap** for multiple connected webcams
* Customizable GUI using **CustomTkinter**
* Fully responsive layout: camera view on left, logs on right

---

## 🛠 Requirements

* Python 3.8+
* Packages:

```bash
pip install opencv-python pyzbar pillow customtkinter
```

---

## ⚡ Usage

1. Clone or download the project.
2. Open a terminal in the project folder.
3. Run the scanner:

```bash
python main.py
```

4. The UI will open:

* **Left side:** Live camera feed (black & white)
* **Right side:** Log of scanned barcodes/QR codes
* **Top of log:** Label shows most recent scan
* **Swap Camera button:** Switch between available webcams

5. The application will automatically draw **red boxes** around valid scanned codes and **green boxes** for ignored codes.

---

## 🎨 Customization

* **Rectangle color:** Change BGR values in the `cv2.rectangle()` calls:

```python
cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)  # Green
cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)  # Red
```

* **Allowed barcode types:** Update the `ALLOWED_TYPES` set:

```python
ALLOWED_TYPES = {"CODE_128", "CODE_39", "DATA_MATRIX", "PDF_417", "AZTEC", "QRCODE"}
```

* **Repeat limit:** Change the maximum repeats in `repeat_count` logic if needed.

---

**Compile:**
```python
pyinstaller --noconsole --onefile --windowed main.py
```

---

## ⚙ Notes

* The app uses **pyzbar** for barcode detection and **OpenCV** for camera access.
* The video feed is converted to grayscale for better contrast.
* The app automatically resets the repeat counter when the code is no longer visible.

---

## 📜 License

MIT License – free to use, modify, and distribute.
