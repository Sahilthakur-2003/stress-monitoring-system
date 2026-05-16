import streamlit as st
import cv2

st.title("Real-Time Stress Monitoring System")

st.write("Webcam based stress monitoring using OpenCV")

run = st.checkbox("Start Camera")

camera = cv2.VideoCapture(0)

frame_window = st.image([])

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

while run:

    ret, frame = camera.read()

    if not ret:
        st.write("Failed to access camera")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        1.1,
        4
    )

    stress = "LOW STRESS"

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        if w * h > 50000:
            stress = "HIGH STRESS"

        cv2.putText(
            frame,
            stress,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame_window.image(frame)

camera.release()