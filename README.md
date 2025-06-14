# 🎯 Real-Time Face Recognition Attendance System (AWS)

This project implements a real-time attendance tracking system using face recognition powered by **AWS Rekognition**. It uses AWS services such as **S3** for image storage, **RDS (MySQL)** for attendance logging, and **EC2** for backend processing using Python and Boto3.

---

## 🚀 Features

- Upload and index face images into Rekognition collection
- Match test/live images against the Rekognition collection
- Log successful face matches (attendance) into an RDS MySQL database
- Uses secure and modular AWS architecture with IAM role-based access

---

## 🛠️ Tech Stack

- **AWS EC2** – Runs Python scripts  
- **AWS S3** – Stores face images  
- **AWS Rekognition** – Performs face indexing and matching  
- **AWS RDS (MySQL)** – Stores attendance logs  
- **IAM** – Manages access permissions  
- **Python** – Backend logic using `boto3` and `mysql-connector-python`

---

## 🔧 Setup & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/pradeep435/face-attendance-aws.git
cd face-attendance-aws
```

---

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🧠 Index a New Face to Rekognition

1. Open `index_face_enroll.py`
2. Set `image_file` and `image_name` to your new image and person’s name
3. Run the script:

```bash
python3 index_face_enroll.py
```

✅ This uploads the image to S3 and indexes it into the Rekognition collection.

---

### 📝 Run the Final Attendance Logger

1. Open `final_attendance_logger.py`
2. Set `image_file` and `image_name` to your test image
3. Run:

```bash
python3 final_attendance_logger.py
```

✅ This script:
- Uploads the test image  
- Searches for a match in Rekognition  
- Logs the attendance in RDS (MySQL)

---

### 🔐 IAM Permissions Used

Ensure your EC2 instance is attached with an IAM Role that has the following policies:

- `AmazonEC2FullAccess`
- `AmazonS3FullAccess`
- `AmazonRDSFullAccess`
- `AmazonRekognitionFullAccess`
- `AmazonSNSFullAccess`
- `AWSLambda_FullAccess`
