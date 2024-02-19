import cv2
import pytesseract
import sqlite3

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'<path_to_tesseract_executable>'

# Connect to SQLite database
conn = sqlite3.connect('text_data.db')
c = conn.cursor()

# Create table to store extracted text
c.execute('''CREATE TABLE IF NOT EXISTS extracted_text (
             id INTEGER PRIMARY KEY,
             text TEXT)''')

# Function to extract text from image
def extract_text(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to preprocess the image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(thresh)
    return text

# Capture video from default camera
cap = cv2.VideoCapture(0)

while True:
    # Read frame from camera
    ret, frame = cap.read()
    if not ret:
        break
    
    # Extract text from the frame
    extracted_text = extract_text(frame)
    
    # Store extracted text in database
    c.execute("INSERT INTO extracted_text (text) VALUES (?)", (extracted_text,))
    conn.commit()
    
    # Display the frame
    cv2.imshow('Video', frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

# Close database connection
conn.close()
