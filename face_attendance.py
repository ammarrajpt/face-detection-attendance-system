import cv2
import csv
import os
from datetime import datetime

# ─── Configuration ───────────────────────────────────────────────
ATTENDANCE_FILE = "attendance.csv"
STUDENTS = {
    "Student_1": None,  # Baad mein asal naam add karo
    "Student_2": None,
}
# ─────────────────────────────────────────────────────────────────


def load_attendance():
    """Aaj ki already marked attendance load karo."""
    marked = set()
    today = datetime.now().strftime("%Y-%m-%d")

    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader, None)  # Header skip
            for row in reader:
                if row and row[1] == today:
                    marked.add(row[0])
    return marked


def mark_attendance(name, marked_today):
    """Student ki attendance CSV mein save karo."""
    if name in marked_today:
        return False  # Already marked

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    file_exists = os.path.exists(ATTENDANCE_FILE)

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Date", "Time", "Status"])
        writer.writerow([name, date_str, time_str, "Present"])

    marked_today.add(name)
    print(f"[✓] Attendance marked: {name} at {time_str}")
    return True


def main():
    # Haar Cascade face detector load karo
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Webcam open karo
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Webcam open nahi ho saki.")
        return

    # Aaj ki attendance load karo
    marked_today = load_attendance()
    print(f"[i] System started | Already marked today: {len(marked_today)}")
    print("[i] Q dabao exit karne ke liye\n")

    face_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Frame receive nahi hua.")
            break

        # Grayscale conversion
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Face detection
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        face_count = len(faces)

        # Har face par rectangle draw karo
        for i, (x, y, w, h) in enumerate(faces):

            # Demo: Pehle face ko Student_1 maano
            # Real system mein face recognition hogi
            student_name = f"Student_{i+1}"

            # Attendance mark karo
            is_new = mark_attendance(student_name, marked_today)

            # Color: Green = naya, Blue = already marked
            color = (0, 255, 0) if is_new else (255, 150, 0)
            label = f"{student_name} - {'Marked!' if is_new else 'Already Present'}"

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                frame, label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2
            )

        # Screen par info show karo
        today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, f"Date/Time: {today_str}",
                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
        cv2.putText(frame, f"Faces: {face_count} | Marked Today: {len(marked_today)}",
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
        cv2.putText(frame, "Press Q to Exit",
                    (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)

        cv2.imshow("Face Detection Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\n[✓] Session complete. Total marked today: {len(marked_today)}")
    print(f"[i] Attendance file: {ATTENDANCE_FILE}")


if __name__ == "__main__":
    main()
