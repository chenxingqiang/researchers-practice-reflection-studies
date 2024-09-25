import csv
import random
import time
import os
import json
import logging
from openai import OpenAI

# 设置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 设置 DeepSeek API
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com")


def generate_open_ended_response(prompt, max_retries=3, delay=5):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system",
                     "content": "你是一位中国高校的早期职业学者，正在参与一项关于反思实践的调查。请以简洁、真实的方式回答以下问题。"},
                    {"role": "user", "content": prompt}
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

def load_progress(filename):
    """加载已生成数据的进度"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = list(csv.DictReader(f))
        return existing_data
    return []


def save_partial_data(data, filename):
    """保存数据到 CSV 文件，支持追加模式"""
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = [f'Question{i}' for i in range(1, 31)]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()
        writer.writerows(data)


def log_progress(log_filename, row, index):
    """将生成的每条数据记录到日志文件中"""
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_entry = {
            'index': index,
            'row': row
        }
        log_file.write(json.dumps(log_entry, ensure_ascii=False) + '\n')


def generate_survey_data(start_index=0, total_records=150, csv_filename='./data/deepseek/survey/survey_results.csv', log_filename='./data/deepseek/survey/generation_log.txt'):
    data = []
    existing_data = load_progress(csv_filename)
    existing_count = len(existing_data)
    start_index = max(existing_count, start_index)

    if start_index >= total_records:
        logging.info(f"所有数据已生成，无需继续。现有 {existing_count} 条记录。")
        return

    logging.info(f"开始从第 {start_index + 1} 条记录继续生成...")

    for i in range(start_index, total_records):
        row = {}

        # Question 1-5: Demographics
        row['Question1'] = random.choice(
            ['25-30岁', '31-35岁', '36-40岁', '41岁以上'])
        row['Question2'] = random.choice(['男', '女', '其他', '不愿透露'])
        row['Question3'] = random.choice(['0-2年', '3-5年', '6-8年', '8年以上'])
        row['Question4'] = random.choice(['人文学科', '社会科学', '自然科学', '工程', '其他'])
        row['Question5'] = random.choice(['讲师', '助理教授', '副教授', '其他'])

        # Question 6: Familiarity with reflective practice
        row['Question6'] = random.choice(
            ['非常熟悉', '比较熟悉', '有所了解', '不太熟悉', '完全不熟悉'])

        # Question 7: Frequency of reflection
        row['Question7'] = random.choices(
            ['每天', '每周', '每月', '每学期', '很少或从不'], weights=[15, 53, 20, 7, 5])[0]

        # Question 8: Methods of reflective practice
        methods = ['教学日志', '同行观察', '学生反馈分析', '研究日志', '导师/同事讨论', '自我评估']
        row['Question8'] = ', '.join(random.sample(
            methods, random.randint(1, len(methods))))

        # Question 9: Helpfulness of reflective practice
        row['Question9'] = random.choices(
            ['非常有帮助', '比较有帮助', '一般', '不太有帮助', '完全没有帮助'], weights=[30, 43, 20, 5, 2])[0]

        # Question 10: Most effective reflective practice method
        prompt = f"作为一名{row['Question4']}领域的{row['Question5']}，请简要描述您最有效的反思实践方法。"
        row['Question10'] = generate_open_ended_response(prompt)

        # Question 11: Biggest challenges
        challenges = ['时间管理', '研究压力', '教学负担', '行政工作', '职业发展不确定性', '工作生活平衡']
        row['Question11'] = ', '.join(
            random.sample(challenges, random.randint(1, 3)))

        # Question 12: Average working hours per week
        row['Question12'] = random.choice(
            ['40小时以下', '40-50小时', '51-60小时', '60小时以上'])

        # Question 13: Satisfaction with workload
        row['Question13'] = random.choice(
            ['非常满意', '比较满意', '一般', '不太满意', '非常不满意'])

        # Question 14: Balance between teaching and research
        row['Question14'] = random.choices(
            ['非常好', '比较好', '一般', '不太好', '非常不好'], weights=[12, 50, 25, 10, 3])[0]

        # Question 15: Time allocation
        teaching = random.randint(30, 50)
        research = random.randint(30, 50)
        admin = random.randint(10, 30)
        other = 100 - teaching - research - admin
        row['Question15'] = f"教学: {teaching}%, 研究: {research}%, 行政工作: {admin}%, 其他: {other}%"

        # Question 16: Conflict between teaching and research
        row['Question16'] = random.choice(['总是', '经常', '有时', '很少', '从不'])

        # Question 17: Agreement on teaching and research synergy
        row['Question17'] = random.choices(
            ['非常同意', '比较同意', '中立', '不太同意', '非常不同意'], weights=[20, 50, 20, 8, 2])[0]

        # Question 18: Frequency of work-related anxiety
        row['Question18'] = random.choices(
            ['总是', '经常', '有时', '很少', '从不'], weights=[15, 50, 25, 8, 2])[0]

        # Question 19: Main sources of academic anxiety
        anxiety_sources = ['发表压力', '申请资助', '职称评定', '教学评估', '同行竞争', '工作不稳定性']
        selected_sources = random.choices(anxiety_sources, k=3)
        row['Question19'] = ', '.join(set(selected_sources))

        # Question 20: Methods to cope with academic anxiety
        prompt = f"作为一名面临{row['Question19']}的{row['Question5']}，您采取哪些方法来应对学术焦虑？"
        row['Question20'] = generate_open_ended_response(prompt)

        # Question 21: Academic atmosphere in the institution
        row['Question21'] = random.choices(
            ['非常支持', '比较支持', '中立', '不太支持', '非常不支持'], weights=[15, 40, 30, 12, 3])[0]

        # Question 22: Unreasonable pressure from the institution
        row['Question22'] = random.choices(
            ['总是', '经常', '有时', '很少', '从不'], weights=[8, 40, 35, 15, 2])[0]

        # Question 23: Encouragement of reflective practice by the institution
        row['Question23'] = random.choices(
            ['非常鼓励', '比较鼓励', '中立', '不太鼓励', '完全不鼓励'], weights=[18, 40, 30, 10, 2])[0]

        # Question 24: Reasonableness of the institution's evaluation system
        row['Question24'] = random.choice(
            ['非常合理', '比较合理', '一般', '不太合理', '非常不合理'])

        # Question 25: Experience of workplace PUA
        row['Question25'] = random.choices(
            ['经常', '有时', '很少', '从未', '不确定'], weights=[5, 43, 30, 15, 7])[0]

        # Question 26: Areas where reflective practice is most helpful
        areas = ['提高教学质量', '增强研究能力', '改善时间管理', '减轻工作压力', '明确职业目标']
        row['Question26'] = ', '.join(
            [f"{area}: {random.randint(1, 5)}" for area in areas])

        # Question 27: Helpfulness of reflective practice in relieving academic anxiety
        row['Question27'] = random.choices(
            ['非常有帮助', '比较有帮助', '一般', '不太有帮助', '完全没有帮助'], weights=[25, 46, 20, 7, 2])[0]

        # Question 28: Impact of reflective practice on career development
        prompt = f"作为一名{row['Question7']}进行反思的{row['Question5']}，反思实践对您的职业发展有何影响？请考虑它如何帮助您增强个人自主性（66%报告增强）和改善整体学术表现（61%报告改善）。"
        row['Question28'] = generate_open_ended_response(prompt)

        # Question 29: Main obstacles to promoting reflective practice
        prompt = "您认为在中国学术环境中推广反思实践的主要障碍是什么？"
        row['Question29'] = generate_open_ended_response(prompt)

        # Question 30: Suggestions for improving academic environment
        prompt = "您对改善早期职业学者的学术环境有什么建议？"
        row['Question30'] = generate_open_ended_response(prompt)

        data.append(row)

        # 保存生成的数据行到 CSV 文件和日志
        save_partial_data([row], csv_filename)
        log_progress(log_filename, row, i + 1)

        # 打印当前进度
        logging.info(f"已生成 {i + 1}/{total_records} 条数据。")

        # 避免 API 速率限制，暂停 1 秒
        time.sleep(1)

    logging.info("数据生成完成。")


# 启动数据生成
generate_survey_data()
