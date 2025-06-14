"""
Face Enrollment Script for AWS Rekognition
------------------------------------------
This script uploads an image to an S3 bucket and indexes the face
into a Rekognition collection for future face matching.
"""

import boto3

# === Configuration ===
image_file = "sample_face.jpg"            # Local image to enroll
image_name = "sample_user"                # Name for the Rekognition entry
bucket_name = "your-s3-bucket-name"       # Replace with your actual S3 bucket
collection_id = "your-collection-id"      # Replace with your actual collection ID
region = "ap-south-1"                     # Your AWS region

# === Step 1: Upload image to S3 ===
print("🔼 Uploading image to S3...")

try:
    s3_client = boto3.client("s3", region_name=region)
    s3_client.upload_file(image_file, bucket_name, image_name)
    print("✅ Image uploaded successfully.")
except Exception as upload_err:
    print("❌ Failed to upload image to S3.")
    print(upload_err)
    exit()

# === Step 2: Index face into Rekognition collection ===
print("🧠 Indexing face in Rekognition...")

try:
    rekognition_client = boto3.client("rekognition", region_name=region)
    response = rekognition_client.index_faces(
        CollectionId=collection_id,
        Image={"S3Object": {"Bucket": bucket_name, "Name": image_name}},
        ExternalImageId=image_name,
        DetectionAttributes=["DEFAULT"]
    )

    face_records = response.get("FaceRecords", [])
    if face_records:
        for face in face_records:
            face_id = face["Face"]["FaceId"]
            print(f"✅ Face indexed successfully. Face ID: {face_id}")
    else:
        print("⚠️ No face detected in the image.")

except Exception as rekognition_err:
    print("❌ Failed to index face in Rekognition.")
    print(rekognition_err)
