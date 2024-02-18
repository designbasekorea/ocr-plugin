from flask import Flask, request, jsonify, make_response, render_template

import os
import easyocr
import numpy as np
from flask_cors import CORS
import base64
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)


reader = easyocr.Reader(["ko", "en"])  # 미리 Reader 객체 생성


# 폴더 생성
if not os.path.exists("uploaded_images"):
    os.makedirs("uploaded_images")

# 설정 변수
app.config["IMAGE_UPLOAD_FOLDER"] = "uploaded_images"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

# 허용되는 확장자 확인
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )

@app.route("/")
def index():
    return 'Hello designbase'

@app.route("/test")
def index():
    return 'test'

@app.route("/ocr_process", methods=["POST"])
def ocr_process():
    # 현재 시간 및 이미지 정보 로깅
    print(f"Request received at {datetime.now()}")
    
    
    request_data = request.json
    base64_image = request_data["image"]
    image_bytes = base64.b64decode(base64_image.split(",")[-1])

    # 이미지 바이트 데이터를 임시 파일로 저장
    temp_filename = "temp_image.jpg"
    
    with open(temp_filename, "wb") as f:
        f.write(image_bytes)

    text = reader.readtext(temp_filename, detail=0)
    print(f"Processed image: {temp_filename}")
    
    # 임시 파일 삭제
    os.remove(temp_filename)

    # OCR 결과 반환
    results = [{"filename": temp_filename, "text": text}]
    response = make_response(jsonify(results))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
