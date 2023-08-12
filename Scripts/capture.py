import cv2

# Open the default camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Failed to open the camera")
    exit()

# Capture a frame from the camera
ret, frame = cap.read()

# Check if the frame was captured successfully
if not ret:
    print("Failed to capture frame")
    exit()

# Save the captured frame to an image file
cv2.imwrite("web/captured_image.jpg", frame)

# Release the camera
cap.release()

# Display a message
print("Image captured successfully")

