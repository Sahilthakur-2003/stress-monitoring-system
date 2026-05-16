import cv2
import time

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot access webcam")
    exit()

print("Stress Monitoring System Started")

prev_time = 0

while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    frame = cv2.resize(frame, (800, 600))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    stress_level = "LOW STRESS"
    color = (0, 255, 0)

    for (x, y, w, h) in faces:

        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        # Simple stress logic
        face_area = w * h

        if face_area > 50000:
            stress_level = "HIGH STRESS"
            color = (0, 0, 255)

        elif face_area > 30000:
            stress_level = "MEDIUM STRESS"
            color = (0, 255, 255)

        else:
            stress_level = "LOW STRESS"
            color = (0, 255, 0)

    # Display stress
    cv2.putText(
        frame,
        f"Stress Level: {stress_level}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3
    )

    # FPS
    current_time = time.time()

    fps = 1 / (current_time - prev_time + 0.0001)

    prev_time = current_time

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (650, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # Show window
    cv2.imshow("Stress Monitoring System", frame)

    # Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()