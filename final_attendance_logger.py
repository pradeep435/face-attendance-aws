"""
Final Attendance Logger Script
------------------------------
This script uploads a test face image to S3, searches for a match in the
Rekognition collection, and logs attendance to RDS MySQL if a match is found.
"""

import boto3
import mysql.connector
from datetime import datetime

# === Configuration ===
image_file = "sample_face.jpg"            # Local image to test
image_name = "sample_user"                # User name for attendance log
bucket_name = "your-s3-bucket-name"       # Your S3 bucket
collection_id = "your-collection-id"      # Your Rekognition collection ID
region = "ap-south-1"                     # AWS region

# === Step 1: Upload image to S3 ===
print("🔼 Uploading image to S3...")

try:
    s3 = boto3.client('s3', region_name=region)
    with open(image_file, 'rb') as image:
        s3.put_object(Bucket=bucket_name, Key=image_file, Body=image)
    print("✅ Image uploaded.")
except Exception as err:
    print("❌ Failed to upload image to S3:", err)
    exit()

# === Step 2: Search face in Rekognition ===
print("🔍 Searching for matching face...")

try:
    rekognition = boto3.client('rekognition', region_name=region)
    response = rekognition.search_faces_by_image(
        CollectionId=collection_id,
        Image={'S3Object': {'Bucket': bucket_name, 'Name': image_file}},
        MaxFaces=1,
        FaceMatchThreshold=85
    )

    face_matches = response.get('FaceMatches', [])
    if not face_matches:
        print("⚠️ No matching face found.")
        exit()

    face_id = face_matches[0]['Face']['FaceId']
    confidence = face_matches[0]['Similarity']
    print(f"✅ Match found: Face ID = {face_id}, Confidence = {confidence:.2f}%")

except Exception as err:
    print("❌ Face match failed:", err)
    exit()

# === Step 3: Log attendance to MySQL ===
print("📝 Logging attendance to RDS MySQL...")

try:
    connection = mysql.connector.connect(
        host="your-rds-endpoint",
        user="your-db-username",
        password="your-db-password",
        database="attendance_db"
    )

    cursor = connection.cursor()
    query = "INSERT INTO attendance (student_name, face_id, timestamp) VALUES (%s, %s, %s)"
    cursor.execute(query, (image_name, face_id, datetime.now()))
    connection.commit()

    print("✅ Attendance logged successfully.")

except Exception as db_err:
    print("❌ Failed to log attendance to MySQL:", db_err)

finally:
    if 'cursor' in locals(): cursor.close()
    if 'connection' in locals(): connection.close()
