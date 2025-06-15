import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# 引入你的分析脚本（我们稍后会创建它）
import model_analyzer

# 初始化 Flask 应用
app = Flask(__name__)
# 允许来自前端的跨域请求
CORS(app)

# 创建一个用于保存上传文件的文件夹
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# 定义一个 API 端点，用于处理文件上传和分析
@app.route('/analyze', methods=['POST'])
def analyze_music():
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


# 启动服务器
if __name__ == '__main__':
    # 使用 0.0.0.0 使其在网络上可见，端口设为 5000
    app.run(host='0.0.0.0', port=5000, debug=True)