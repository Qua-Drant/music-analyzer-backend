# 音乐智能分析平台 - 后端
(Music Intelligence Analysis Platform - Backend)

本项目是“音乐智能分析平台”的后端服务。它基于 Python 和 Flask 构建，提供一个核心的 API 接口，负责接收前端上传的音频文件，调用预训练的深度学习模型进行分析，并以 JSON 格式返回评分和评论结果。

---

### ✨ 主要功能 (Features)

-   **Flask API**: 提供一个 `/analyze` API 接口，用于处理文件上传和模型调用。
-   **AI 模型集成**: 无缝集成了基于 PyTorch 的 `masterwork_new` 模块，执行核心智能分析任务。
-   **核心处理逻辑**:
    -   音频特征提取 (Embedding & Keywords)
    -   基于关键词的乐评文本生成
    -   基于嵌入向量和评论的乐曲评分
-   **数据标准化**: 将模型输出的原始分数（0-30范围）通过线性映射，转换为前端友好的标准分数（0-5范围）。
-   **生产环境就绪**: 配置了 Gunicorn 作为 WSGI 服务器，可通过 systemd 进行服务管理，确保稳定运行。
-   **跨域支持**: 集成了 Flask-Cors，允许来自任何源的前端应用进行访问。

### 🛠️ 技术栈 (Technology Stack)

-   **核心语言**: Python 3.11+
-   **Web 框架**: [Flask](https://flask.palletsprojects.com/)
-   **WSGI 服务器**: [Gunicorn](https://gunicorn.org/)
-   **深度学习框架**: [PyTorch](https://pytorch.org/)
-   **跨域解决方案**: [Flask-Cors](https://flask-cors.readthedocs.io/)

### 📖 API 文档 (API Documentation)

#### `POST /analyze`

接收一个音频文件，并返回其分析结果。

-   **请求 (Request)**:
    -   **Method**: `POST`
    -   **Body**: `multipart/form-data`
    -   **Fields**:
        -   `musicFile`: 用户的音频文件 (e.g., an `.mp3` file)

-   **成功响应 (Success Response - 200 OK)**:
    -   **Content-Type**: `application/json`
    -   **Body**:
        ```json
        {
          "track_name": "示例曲目",
          "rating": 4.5,
          "comment": "这是一段由AI生成的、关于这首音乐的优美评论。"
        }
        ```

-   **失败响应 (Error Response)**:
    -   **Content-Type**: `application/json`
    -   **Body**:
        ```json
        {
          "error": "具体的错误信息描述。"
        }
        ```

### 🚀 本地开发与运行 (Local Development)

1.  **前提条件**:
    -   Python 3.11+
    -   熟悉 Python 虚拟环境 (`venv`)

2.  **克隆仓库**:
    ```bash
    git clone [https://github.com/Qua-Drant/music-analyzer-backend.git](https://github.com/Qua-Drant/music-analyzer-backend.git)
    ```

3.  **进入项目目录**:
    ```bash
    cd music-analyzer-backend
    ```

4.  **创建并激活虚拟环境**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(在 Windows CMD 中，激活命令为 `venv\Scripts\activate`)*

5.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

6.  **准备模型文件 (重要！)**:
    -   在项目根目录下创建一个名为 `weights` 的文件夹。
    -   将您训练好的模型权重文件（例如 `final_model_score.pth` 等）放入这个 `weights/` 文件夹中。

7.  **启动服务**:
    -   **开发模式 (用于调试)**:
        ```bash
        flask run --port=5000
        ```
    -   **生产模式 (用于实际运行)**:
        ```bash
        gunicorn --bind 0.0.0.0:5000 --timeout 300 app:app
        ```

---
