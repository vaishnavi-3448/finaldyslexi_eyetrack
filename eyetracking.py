import cv2
import threading
import tkinter as tk
from tkinter import Label, messagebox
import time
import random


focus_time = 0
unfocus_time = 0
total_time = 30  
last_update = time.time()
test_running = True
senetence=["The quick brown fox jumps over the lazy dog.","Was it a car or a cat I saw?","She sells seashells by the seashore.","The boy went to the store to buy milk."]
num=random.randint(0,3)
def display_reading_task():
    global test_running
    root = tk.Tk()
    root.title("Reading Task")
    root.geometry("800x300")

    
    text = Label(root, text=senetence[num], font=("Helvetica", 24))
    text.pack(pady=30)

    
    status_label = Label(root, text="Status: Tracking...", font=("Helvetica", 18), fg="blue")
    status_label.pack()

    focus_label = Label(root, text="Focus Time: 0s", font=("Helvetica", 18), fg="green")
    focus_label.pack()
    
    unfocus_label = Label(root, text="Unfocus Time: 0s", font=("Helvetica", 18), fg="red")
    unfocus_label.pack()
    root.attributes('-topmost', 1)  # Force window to front
    root.after(1000, lambda: root.attributes('-topmost', 0))  # Allow normal behavior after 1 second

    
    def update_labels():
        while test_running:
            status_label.config(text=f"Status: {'Focused' if focus_time >= unfocus_time else 'Unfocused'}")
            focus_label.config(text=f"Focus Time: {int(focus_time)}s")
            unfocus_label.config(text=f"Unfocus Time: {int(unfocus_time)}s")
            root.update_idletasks()
            time.sleep(1)

    
    def calculate_score():
        global test_running
        test_running = False  # Stop test
        total_observed_time = focus_time + unfocus_time
        focus_ratio = focus_time / total_observed_time if total_observed_time > 0 else 0
        score = min(25, int(focus_ratio * 25))  # Scale score to 25
        # Show result
        messagebox.showinfo("Test Completed", f"Your Focus Score: {score}/25")
        root.destroy()

   
    threading.Thread(target=update_labels, daemon=True).start()

    
    root.after(total_time * 1000, calculate_score)

    root.mainloop()


def gaze_tracking():
    global focus_time, unfocus_time, last_update

    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

   
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    while test_running:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame.")
            break

        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        focused = False

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)

            if len(eyes) > 0:
                focused = True
                cv2.putText(frame, "Focused!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Not Focused!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        current_time = time.time()
        time_diff = current_time - last_update
        last_update = current_time

        if focused:
            focus_time += time_diff
        else:
            unfocus_time += time_diff

       
        cv2.imshow('Gaze Tracking', frame)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.namedWindow('Gaze Tracking', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Gaze Tracking', cv2.WND_PROP_TOPMOST, 1)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    text_thread = threading.Thread(target=display_reading_task)
    gaze_thread = threading.Thread(target=gaze_tracking)

    text_thread.start()
    gaze_thread.start()

    text_thread.join()
    gaze_thread.join()
