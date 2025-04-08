import json
import pandas as pd

# JSON ����
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

# ���� JSON ����
parsed_data = json.loads(json_data)

# ��ȡ��һ���ֶκ͵�����ֶ�
extracted_data = [(entry[0], entry[4]) for entry in parsed_data['data']]

# ���� DataFrame
df = pd.DataFrame(extracted_data, columns=['Field1', 'Field5'])

# ����Ϊ����ʽ
df.to_csv('output.csv', index=False)

print("Data saved successfully.")
