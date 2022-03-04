import xml.etree.ElementTree as ET
import pandas as pd
import os
from collections import Counter

"""
observable 당 하나의 row
observable tag 하위 데이터 다 뽑아서 row로 만들었습니다.
index는 observable_id로 했습니다.

related_object는 하나의 object에 달려 있는 수가 많아서 일단 콤마로 구분지어 놨고,
나중에 필요하면 row로 만들어서 쓰면 될 것 같습니다.
"""


def extraction(parent, df, sample, exc_tag):
    # 최하위 tag
    if len(parent) == 0:
        tag = parent.tag.replace(parent.tag[:parent.tag.find('}') + 1], "")
        if parent.text is not None:
            if tag in sample.keys():
                sample[tag] = sample[tag] + ',' + str(parent.text)
            else:
                sample[tag] = parent.text

    for child in parent:
        tag = child.tag.replace(child.tag[:child.tag.find('}') + 1], "")
        if tag in exc_tag:
            continue
        extraction(child, df, sample, exc_tag)

    return df


# df -> process 모음
df = pd.DataFrame()
path_dir = './VMray Dataset'
file_list = os.listdir(path_dir)
for file in file_list:
    # xml 파일 parsing
    print('file:', file)
    if not file.endswith('.xml'):
        continue
    tree = ET.parse(path_dir + '/' + file)
    # root tag
    root = tree.getroot()
    # 추출 시 제외 태그
    exclude_tag = ['Title', 'Property', 'Related_Object']
    # row
    sample = dict()
    sample['file_name'] = file
    # tag 추출
    extraction(root[1], df, sample, exclude_tag)

    # 최빈값으로 저장
    for feat in sample:
        data = sample[feat].split(',')
        sample[feat] = Counter(data).most_common(1)[0][0]
    print(sample)
    df = df.append(sample, ignore_index=True)

df = df.set_index('file_name')

df.to_csv('dataset.csv', mode='w')
