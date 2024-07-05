import streamlit as st
import numpy as np
import cv2

# st.title("Fall Detection")

cap = cv2.VideoCapture(0)

bg_subtractor = cv2.createBackgroundSubtractorMOG2()
fall_threshold_area = 20_000
temp = [0, 0, 0, 0]

# Streamlit webcam input
FRAME_WINDOW = st.image([])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.write("Failed to capture video")
        break

    fg_mask = bg_subtractor.apply(frame)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    # fg_mask[fg_mask < 200] = 0

    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        variance = np.var(contour)
        if area > fall_threshold_area:
            x, y, w, h = cv2.boundingRect(contour)
            temp = [x, y, w, h]
            cv2.putText(frame, "Fall Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
