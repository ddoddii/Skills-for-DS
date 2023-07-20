import argparse
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
import logging
import os
import csv

""" 
1. ArgumentParser 설정 
"""
# ArgumentParser 객체 생성
parser = argparse.ArgumentParser(description='이 프로그램의 설명')

# 인자 추가하기
parser.add_argument('--text', type=str, required=True, default= None, help='input text 값')
parser.add_argument('--env', required=False, default='dev', help='실행환경은 뭐냐')

conf = parser.parse_args()

if conf.text is None:
    print("\n No Text is supplied. Please input text. \n")
elif conf.text.endswith(".txt"):
    with open(conf.text, 'r', encoding='utf-8') as f:
        text = f.read()

""" 
2. Logger 설정
"""
# logger 객체 생성
logger = logging.getLogger(name='MyLog')
logger.setLevel(logging.INFO) ## 경고 수준 설정

# log 의 format 
formatter = logging.Formatter('|%(asctime)s||%(name)s||%(levelname)s|\n%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )

stream_handler = logging.StreamHandler() ## 스트림 핸들러 생성
stream_handler.setFormatter(formatter) ## 텍스트 포맷 설정
logger.addHandler(stream_handler) ## 핸들러 등록

# log file 에 로그들을 모두 저장하고 싶을 때
logging.basicConfig(filename='myinfo.log',level=logging.INFO)


# https://huggingface.co/arpanghoshal/EmoRoBERTa 참고 
tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline('sentiment-analysis', 
                    model='arpanghoshal/EmoRoBERTa')

emotion_labels = emotion(text)
#print(emotion_labels)
logger.info(emotion_labels)


""" 
Q1. debug 수준은 출력될까 ? -> 출력안된다 !
""" 
debug_test = "hi I am debug"
logger.debug(debug_test)

""" 
Task1. 만약 file 내에 있는 모든 textfile 에 대해 결과를 csv 로 출력하고 싶으면 ? 
"""

# Define input folder and output file paths
input_folder = 'textfile'
output_file = 'emotion_results.csv'

# Define CSV headers
headers = ['file_name', 'label','score']


# Initialize an empty list to store the results
results = []

# Iterate over the files in the input folder
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    
    # Check if the file is a text file
    if filename.endswith(".txt"):
        # Read the text file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Process the text and get the results
        rst_data_list = emotion(text)

        # Iterate over the elements in the rst_data_list
        for rst_data in rst_data_list:
            # Create a dictionary for each result
            result_dict = {
                'file_name': os.path.splitext(filename)[0],
                'label': rst_data['label'],
                'score': rst_data['score']
            }

            # Append the result dictionary to the list
            results.append(result_dict)
        
        logger.info(result_dict)

# Write the results to the CSV file
with open(output_file, 'w', newline='',encoding='utf-8-sig') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)

    # Write headers
    writer.writeheader()

    # Write rows
    for result in results:
        writer.writerow(result)

print('Results saved to', output_file)

