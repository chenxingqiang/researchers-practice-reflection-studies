import csv
import random
import json
import os
import time
import logging
from tqdm import tqdm
from openai import OpenAI

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# set DeepSeek API
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com")

# select 20 viewers in random
def select_random_data(file_path, num_samples=20):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return random.sample(data, num_samples)

# 生成访谈回答
def generate_interview_response(prompt, background, max_retries=3, delay=5):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一位中国高校的早期职业学者，正在参与一项关于反思实践的访谈。请基于给定的背景信息，以真实、详细的方式回答以下问题。"},
                    {"role": "user", "content": f"背景信息：{background}\n\n问题：{prompt}"}
                ],
                stream=False
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(
                f"Error generating response (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                return "无回答"

# 保存进度


def save_progress(completed_interviews):
    with open('progress.json', 'w') as f:
        json.dump(completed_interviews, f)

# 加载进度


def load_progress():
    if os.path.exists('./data/deepseek/views/progress.json'):
        with open('./data/deepseek/views/progress.json', 'r') as f:
            return json.load(f)
    return []

# 主函数


def main():
    # 访谈大纲
    interview_outline = {
        "1. 开场白和介绍": [
            "感谢参与",
            "重申研究目的和保密承诺",
            "获得录音许可"
        ],
        "2. 背景信息": [
            "教育背景",
            "当前职位和工作年限",
            "主要研究领域"
        ],
        "3. 反思实践经验": [
            "对反思实践的理解",
            "个人反思实践的方法和频率",
            "反思实践在工作中的应用实例"
        ],
        "4. 学术工作挑战": [
            "主要面临的挑战及其影响",
            "应对策略",
            "机构支持的评价"
        ],
        "5. 教学与研究平衡": [
            "时间分配",
            "整合教学和研究的策略",
            "遇到的困难和解决方法"
        ],
        "6. 学术焦虑": [
            "焦虑的主要来源",
            "对工作和生活的影响",
            "缓解方法"
        ],
        "7. 机构文化和压力": [
            "对机构文化的看法",
            "经历过的不合理压力",
            "\"职场PUA\"的观察或经历"
        ],
        "8. 反思实践的效果": [
            "反思实践带来的变化",
            "对职业发展的影响",
            "推广反思实践的建议"
        ],
        "9. 结束": [
            "补充意见",
            "感谢参与"
        ]
    }

    # 加载已完成的访谈
    completed_interviews = load_progress()

    # 随机选择20条数据
    selected_data = select_random_data(
        './data/deepseek/survey/survey_results.csv')

    # 生成访谈回答并保存
    for i, data in enumerate(tqdm(selected_data)):
        if i in completed_interviews:
            logging.info(f"Skipping interview {i+1} (already completed)")
            continue

        interview_responses = {}
        for section, questions in interview_outline.items():
            section_responses = {}
            for question in questions:
                prompt = f"{section} - {question}"
                response = generate_interview_response(prompt, str(data))
                section_responses[question] = response
            interview_responses[section] = section_responses

        # 将回答保存为JSON文件
        with open(f'./data/deepseek/views/interview_responses_{i+1}.json', 'w', encoding='utf-8') as f:
            json.dump(interview_responses, f, ensure_ascii=False, indent=4)

        # 更新进度
        completed_interviews.append(i)
        save_progress(completed_interviews)

        logging.info(f"Completed interview {i+1}")

    logging.info("All interviews completed")


if __name__ == "__main__":
    main()
