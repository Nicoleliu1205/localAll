import json
import pandas as pd

# JSON 数据
json_data = '''
{
    "code": "0",
    "msg": "",
    "data": [
        [
            "1714060800000",
            "66840.6",
            "67990.2",
            "66477.8",
            "66973.7",
            "238325",
            "355.0976",
            "23832500",
            "0"
        ],
        [
            "1713974400000",
            "67613.4",
            "68121.4",
            "65230.6",
            "66844.8",
            "1330382",
            "1997.9107",
            "133038200",
            "1"
        ]
    ]
}
'''

# 解析 JSON 数据
parsed_data = json.loads(json_data)

# 提取第一个字段和第五个字段
extracted_data = [(entry[0], entry[4]) for entry in parsed_data['data']]

# 创建 DataFrame
df = pd.DataFrame(extracted_data, columns=['Field1', 'Field5'])

# 保存为表格格式
df.to_csv('output.csv', index=False)

print("Data saved successfully.")
