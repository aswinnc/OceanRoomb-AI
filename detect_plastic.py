import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model(r'C:\Users\Gandhiraj\PycharmProjects\Ocean-RoobAi\backend\plastic_detector_model.h5')

# Function to preprocess the image for the model
def preprocess_image(input_frame):
    resized_frame = cv2.resize(input_frame, (224, 224))  # Resize to model input shape
    normalized_frame = resized_frame.astype('float32') / 255.0  # Normalize pixel values
    expanded_frame = np.expand_dims(normalized_frame, axis=0)  # Add batch dimension
    return expanded_frame

# Start the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame for prediction
    preprocessed_frame = preprocess_image(frame)

    # Make prediction
    prediction = model.predict(preprocessed_frame)
    label = 'Plastic' if prediction[0][0] > 0.5 else 'Not Plastic'

    # Display the prediction on the frame
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Plastic Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
