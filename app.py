# backend/app.py

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import model_analyzer

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ===============================================================
# 【新增的诊断路由】
# 这是一个最简单的路由，用于测试服务器是否在正常运行。
# ===============================================================
@app.route('/')
def health_check():
    return "Backend is running!"

# 您原来的分析路由
@app.route('/analyze', methods=['POST'])
def analyze_music():
    # ... 您现有的 analyze_music 函数代码保持不变 ...
    """
    接收上传的音乐文件，调用模型进行分析，并返回结果。
    """
    # 1. 检查是否有文件被上传
    if 'musicFile' not in request.files:
        return jsonify({"error": "没有文件部分"}), 400

    file = request.files['musicFile']

    # 2. 检查文件名是否为空
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400

    # 3. 保存上传的文件
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 4. 调用你的核心分析逻辑
        # 这个函数会处理文件并返回一个包含评分和评论的字典
        analysis_result = model_analyzer.analyze(file.filename, filepath)

        # 5. （可选）清理上传的文件
        os.remove(filepath)

        # 6. 将结果以 JSON 格式返回给前端
        return jsonify(analysis_result)

    return jsonify({"error": "文件上传失败"}), 500
