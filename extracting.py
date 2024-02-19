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

