# backend/model_analyzer.py (更新版)

import os
import torch
# 确保可以从 masterwork_2 模块中正确导入
from masterwork_2.extract_music import extract_music_embedding
from masterwork_2.infer_music_reviews import MusicReviewInference
from masterwork_2.infer_music_score import MusicReviewScorer

# 【关键修复】使用相对路径来定位权重文件，使其在任何服务器上都能工作
# 获取当前文件所在的目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 构造权重文件的绝对路径
REVIEW_MODEL_PATH = os.path.join(BASE_DIR, 'weights', 'best_model_new.pt')
SCORE_MODEL_PATH = os.path.join(BASE_DIR, 'weights', 'final_model_score.pth')


# 我们将您的处理逻辑封装在一个名为 analyze 的函数中，以便 app.py 调用
def analyze(track_name, mp3_path):
    """
    使用真实的深度学习模型来处理上传的音乐文件。
    """
    try:
        # Step 1: 提取音乐嵌入
        # 不再需要 strip('"')，因为文件路径由我们的服务器直接提供
        music_data = extract_music_embedding(mp3_path)
        if music_data is None:
            print("无法提取音乐片段，请检查输入参数。")
            # 【修改】返回一个错误信息的字典
            return {"error": "无法处理该音频文件。"}

        music_embedding = music_data['embedding']

        # Step 2: 使用音乐嵌入生成评论
        # 【修改】使用我们构造的相对路径加载模型
        review_inference = MusicReviewInference(weights_path=REVIEW_MODEL_PATH)
        reviews = review_inference.generate_reviews([music_embedding])
        review_text = reviews[0]

        # Step 3: 使用音乐嵌入和评论文本进行打分
        # 【修改】使用我们构造的相对路径加载模型
        scorer = MusicReviewScorer(model_path=SCORE_MODEL_PATH)
        score = scorer.predict_score(music_embedding, review_text)

        # 确保评分是一个 Python 内置的数字类型，而不是 numpy 或 tensor 类型
        # 假设 score 是一个 numpy array 或者单元素 tensor
        if hasattr(score, 'item'):
            score = score.item()

        final_score = round(float(score), 1)

        # Step 4: 【修改】返回一个包含结果的字典，而不是打印
        print(f"曲目: {track_name}, 评论: {review_text}, 打分: {final_score}")
        return {
            "track_name": track_name.split('.')[0],
            "rating": final_score,
            "comment": review_text
        }

    except Exception as e:
        print(f"处理音频时发生错误: {e}")
        return {"error": f"模型处理失败: {e}"}