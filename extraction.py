import xml.etree.ElementTree as ET
import pandas as pd
import os

"""
observable 당 하나의 row
observable tag 하위 데이터 다 뽑아서 row로 만들었습니다.
index는 observable_id로 했습니다.

related_object는 하나의 object에 달려 있는 수가 많아서 일단 콤마로 구분지어 놨고,
나중에 필요하면 row로 만들어서 쓰면 될 것 같습니다.
"""


def get_child(parent, df, data):
    # 최하위 tag
    if len(parent) == 0:
        tag = parent.tag.replace(parent.tag[:parent.tag.find('}') + 1], "")
        # print(tag, parent.text)
        if parent.text is not None:
            if tag in data.keys():
                data[tag] = data[tag] + ', ' + str(parent.text)
            else:
                data[tag] = parent.text

    for child in parent:
        tag = child.tag.replace(child.tag[:child.tag.find('}') + 1], "")
        if tag == 'Related_Object':
            continue
        if tag == 'Observable':
            if len(data) != 0:
                # print(data)
                df = df.append(data, ignore_index=True)
            data = dict()
        # if len(child) > 0:
        #     if tag == 'Observable':
        #         data['observable_id'] = child.attrib['id']
        #         # print(tag, 'id:', child.attrib['id'])
        #     if tag == 'Object':
        #         data['object_id'] = child.attrib['id']
            # if tag == 'Related_Object':
            #     if 'idref' in data.keys():
            #         data['idref'] = data['idref'] + ', ' + child.attrib['idref']
            #     else:
            #         data['idref'] = child.attrib['idref']
            # print(tag, 'idref:', child.attrib['idref'])
        get_child(child, df, data)

    return df


"""
# df -> process 모음
# ref_df -> process 이외 모음
"""
df = pd.DataFrame()

path_dir = './VMray Dataset'
file_list = os.listdir(path_dir)
for file in file_list:
    print('file:', file)
    # xml 파일 parsing
    if not file.endswith('.xml'):
        continue
    tree = ET.parse(path_dir + '/' + file)
    # root tag
    root = tree.getroot()
    tmp = pd.DataFrame()
    tmp = get_child(root[1], tmp, dict())
    tmp['file_name'] = file
    df = pd.concat([df, tmp], ignore_index=True)
    print(df)

df = df.set_index('file_name')
# print(df)

df.to_csv('extraction_v2.csv', mode='w')
