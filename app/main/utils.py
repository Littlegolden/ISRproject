from main.db import consult_db, connect_db


def pic_info(res_list):
    """
    由一张图的序号获得这张图的所有信息的json
    @param res_list: 数字列表
    @return: 结果列表
    """
    # 连接数据库
    db_session = connect_db("129.211.91.153:3306", "isrbqb", 'admin', 'abcd')
    # 查出所有的description,role,emotion,style,topic
    res_description = consult_db(db_session, "bqb_description", "geng")
    res_role = consult_db(db_session, "bqb_role", "role")
    res_emotion = consult_db(db_session, "bqb_emotion", "emotion")
    res_style = consult_db(db_session, "bqb_style", "style")
    res_topic = consult_db(db_session, "bqb_context", "context")
    # 生成匹配的Res
    res = [{'name': str("{:0>4}".format(str(i[0]))) + '.jpg',
            'src_path': 'static/bqbSource/' + str(
                "{:0>4}".format(str(i[0]))) + '.jpg',
            'score': i[1],
            'role': [],
            'emotion': [],
            'style': [],
            'topic': []
            } for i in res_list]
    for i in res_description:
        for j in res:
            if i[0] == j['name']:
                j['description'] = i[1]

    for i in res_role:
        for j in res:
            if i[0] == j['name']:
                j['role'].append(i[1])
    for i in res_emotion:
        for j in res:
            if i[0] == j['name']:
                j['emotion'].append(i[1])
    for i in res_style:
        for j in res:
            if i[0] == j['name']:
                j['style'].append(i[1])
    for i in res_topic:
        for j in res:
            if i[0] == j['name']:
                j['topic'].append(i[1])
    print(res)
    return res


def in_filter(pic_item, filter_dict):
    """
    检查一个图片是否符合特征过滤器
    @param pic_item: 检查的图片（字典）
    @param filter_dict: 过滤器（字典）
    @return: 是否符合
    """
    feature_list = ['role', 'emotion', 'style', 'topic']
    feature_flag = {k: False for k in feature_list if
                    filter_dict[k]}  # 过滤器中存在项目的特征才检查
    for feature_item in feature_list:  # 依次查看每一个特征
        for feature in pic_item[feature_item]:
            if feature in filter_dict[feature_item]:
                feature_flag[feature_item] = True  # 只要有一个值是符合的，那么该特征检查通过
    # 所有特征都通过的才行
    for flag_item in feature_flag.values():
        if not flag_item:  # 有一个检查没通过就不行
            return False
    return True


# 返回list
def sorted_dict_values(a_dict, reverse=False):
    lst = sorted(a_dict.items(), key=lambda item: item[1], reverse=reverse)
    # 先转换为lst，然后根据第二个元素排序
    return lst