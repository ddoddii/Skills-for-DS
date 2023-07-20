import requests
import xmltodict
import json
import logging

# logger
logger = logging.getLogger(name='MyLog')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('|%(asctime)s||%(name)s||%(levelname)s|\n%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )

stream_handler = logging.StreamHandler() 
stream_handler.setFormatter(formatter) 
logger.addHandler(stream_handler) 

# API URL
url = "https://business.juso.go.kr/addrlink/addrLinkApi.do"

# Parameters  
confmKey = "devU01TX0FVVEgyMDIzMDcxODE0MDUxNDExMzkzODk="
currentPage = 1
countPerPage = 10
keyword = "서대문구 연세로 50"

# Construct the URL with encoded parameters
params = {
    "confmKey": confmKey,
    "currentPage": currentPage,
    "countPerPage": countPerPage,
    "keyword": keyword
}
encoded_params = "&".join([f"{key}={value}" for key, value in params.items()])
full_url = f"{url}?{encoded_params}"

# Send the GET request
response = requests.get(full_url)

# Process the response
if response.status_code == 200:
    xml_data = response.text
    data_dict = xmltodict.parse(xml_data)
    json_data = json.dumps(data_dict, ensure_ascii=False)
    parsed_data = json.loads(json_data)
    #logger.info(json_data)
    #logger.info(parsed_data)
    
    # Process the data as needed
else:
    # Request failed
    print(f"Request failed with status code {response.status_code}")

for i in range(10):
    road_addr = parsed_data['results']['juso'][i]['roadAddr']
    logger.info(road_addr)