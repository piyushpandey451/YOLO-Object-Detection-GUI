import tkinter as tk
from tkinter import filedialog, messagebox
from ultralytics import YOLO
import cv2
from PIL import Image, ImageTk
import threading

# ---------------- YOLO MODEL ----------------
model = YOLO("yolov8n.pt")

# ---------------- THEMES ----------------
DARK_THEME = {
    "bg": "#121212",
    "panel": "#1E1E1E",
    "text": "#FFFFFF",
    "subtext": "#AAAAAA",
    "button": "#2D89EF"
}

LIGHT_THEME = {
    "bg": "#F4F4F4",
    "panel": "#FFFFFF",
    "text": "#000000",
    "subtext": "#555555",
    "button": "#1976D2"
}

current_theme = "dark"

# ---------------- GUI ----------------
root = tk.Tk()
root.title("YOLO Object Detection System")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

# ---------------- FUNCTIONS ----------------

def apply_theme(theme):
    root.configure(bg=theme["bg"])
    header.configure(bg=theme["panel"])
    content.configure(bg=theme["bg"])
    footer.configure(bg=theme["panel"])

    title_label.configure(bg=theme["panel"], fg=theme["text"])
    footer_label.configure(bg=theme["panel"], fg=theme["subtext"])

    canvas.configure(bg=theme["panel"])

    for btn in buttons:
        btn.configure(bg=theme["button"], fg=theme["text"])

    toggle_btn.configure(bg=theme["button"], fg=theme["text"])


def toggle_theme():
    global current_theme
    if current_theme == "dark":
        current_theme = "light"
        apply_theme(LIGHT_THEME)
        toggle_btn.config(text="🌙 Dark Mode")
    else:
        current_theme = "dark"
        apply_theme(DARK_THEME)
        toggle_btn.config(text="☀ Light Mode")


def detect_image():
    path = filedialog.askopenfilename(
        filetypes=[("Images", "*.jpg *.png *.jpeg")]
    )
    if not path:
        return

    results = model(path)
    annotated = results[0].plot()

    img = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img).resize((900, 500))

    img_tk = ImageTk.PhotoImage(img)
    canvas.delete("all")
    canvas.image = img_tk
    canvas.create_image(0, 0, anchor="nw", image=img_tk)


def detect_video():
    path = filedialog.askopenfilename(
        filetypes=[("Videos", "*.mp4 *.avi *.mov")]
    )
    if not path:
        return

    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        cv2.imshow("Video Detection (Press Q)", results[0].plot())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def realtime_detection():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        cv2.imshow("Real-Time Detection (Press Q)", results[0].plot())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def run_video():
    threading.Thread(target=detect_video, daemon=True).start()


def run_camera():
    threading.Thread(target=realtime_detection, daemon=True).start()


# ---------------- COPYRIGHT POPUP ----------------
messagebox.showinfo("Copyright", "© Piyush Kumar\nAll Rights Reserved")

# ---------------- HEADER ----------------
header = tk.Frame(root, height=80)
header.pack(fill="x")

title_label = tk.Label(
    header,
    text="YOLO Object Detection System",
    font=("Segoe UI", 22, "bold")
)
title_label.pack(side="left", padx=30)

toggle_btn = tk.Button(
    header,
    text="☀ Light Mode",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    cursor="hand2",
    command=toggle_theme
)
toggle_btn.pack(side="right", padx=30)

# ---------------- CONTENT ----------------
content = tk.Frame(root)
content.pack(expand=True)

canvas = tk.Canvas(
    content,
    width=900,
    height=500,
    highlightthickness=0
)
canvas.pack(pady=30)

canvas.create_text(
    450, 250,
    text="No image loaded",
    font=("Segoe UI", 16),
    fill=DARK_THEME["subtext"]
)

# ---------------- BUTTONS ----------------
btn_frame = tk.Frame(content)
btn_frame.pack(pady=20)

buttons = []

def create_btn(text, cmd):
    btn = tk.Button(
        btn_frame,
        text=text,
        width=22,
        height=2,
        font=("Segoe UI", 12, "bold"),
        relief="flat",
        cursor="hand2",
        command=cmd
    )
    btn.pack(side="left", padx=15)
    buttons.append(btn)

create_btn("🖼 Image Detection", detect_image)
create_btn("🎬 Video Detection", run_video)
create_btn("📷 Real-Time Detection", run_camera)

# ---------------- FOOTER ----------------
footer = tk.Frame(root, height=40)
footer.pack(fill="x", side="bottom")

footer_label = tk.Label(
    footer,
    text="© Piyush Kumar | Press ESC to exit fullscreen",
    font=("Segoe UI", 10)
)
footer_label.pack(pady=10)

# ---------------- APPLY DEFAULT THEME ----------------
apply_theme(DARK_THEME)

# ---------------- START ----------------
root.mainloop()
