import math

class Classical_Sequential_Pattern:
    def __init__(self, pattern_name, length, support):
        self.pattern_name = pattern_name
        self.length = length
        self.support = support
        self.username_support_list = []
    def appendSubsupport(self, username_support_tuple):
        self.username_support_list.append(username_support_tuple)

class Prefix_Item:
    def __init__(self, prefix_name, prob, end_pos):
        self.prefix_name = prefix_name
        self.prob = prob
        self.end_pos = end_pos


""" 找到可能在 alpha 之后发生的事件 """
def findCategory(alpha, Sess_after_alpha):
    get_category = lambda item: item[0]
    categories = list(map(get_category, Sess_after_alpha.values()))
    # print(set(categories) - set(alpha))
    return set(categories) - set(alpha)

""" 找到 事件cate 在数据中的实例 """
def findInstanceList(cate, Sess_after_alpha):
    InstanceList = [[key, Sess_after_alpha[key][-1]] for key in Sess_after_alpha.keys() if cate in Sess_after_alpha[key][0]]
    if len(InstanceList):
        InstanceList = sorted(InstanceList, key=lambda item: item[0])
    # print(InstanceList)
    return InstanceList

""" 根据 事件cate的实例的位置， 找到距离它最近的前缀的出现概率 """
def findRecord(prefix_record, position):
    list_ = list(filter(lambda item: item.end_pos < position, prefix_record))
    prefix_list = sorted(list_, key=lambda item:item.end_pos)
    # for prefix in prefix_list: print("prefix:", prefix.prefix_name, prefix.prob, prefix.end_pos)
    p = prefix_list[-1].prob if len(prefix_list) > 0 else 0.0
    return p


def PrefixSpan_for_Sequential_Pattern(alpha, Sess_after_alpha, Record_alpha, Pattern_Summary_Dict, min_len, max_len):
    next_categories = findCategory(alpha, Sess_after_alpha)
    for cate in next_categories:
        ''' beta is the new pattern '''
        beta = alpha.copy(); beta.append(str(cate)); beta_len = len(beta)
        ''' get instance action of cate '''
        InstanceList = findInstanceList(cate, Sess_after_alpha)
        ''' S_beta is the suffix set; R_beta is the ; Supp_beta is the ; '''
        Sess_after_beta, Supp_beta, Record_beta = {}, {}, []

        """ 支持度计算方法 *** 闪亮登场 *** """
        '''P is the occurrence probability in each session, p_j2 recaod the last probability'''
        P, p_j2 = 0, 0
        '''InstanceList is a event set. j[0] = key, j[1]=prob '''
        for [key, prob] in InstanceList:
            '''if beta is the first topic p_star = 1, else p_star = findRecord '''
            p_star = 1.0 if beta_len - 1 <= 0 else findRecord(Record_alpha, key)
            P = prob * p_star + (1 - prob) * p_j2
            p_j2 = P
            if P > 0.0:
                Record_beta.append(Prefix_Item(prefix_name=beta, prob=P, end_pos=key))
        """ 支持度计算方法 *** 完美谢幕 *** """

        ''' filter out patterns with support equal to 0 '''
        if  beta_len >= min_len and beta_len <= max_len and P > 0.0:
            support = math.pow(P, 1 / beta_len)     # """ 针对序列模式长度进行归一化的支持度 """
            pattern_str = "; ".join(beta)
            Pattern_Summary_Dict[pattern_str] = Classical_Sequential_Pattern(pattern_name=tuple(beta), length=beta_len, support=support)
            #print("Classical_Sequential_Pattern", tuple(beta), beta_len, support)

        """ 基于模式增长思想的递归算法 """
        if P > 0.0 and beta_len < max_len and InstanceList[0][0] + 1 < len(Sess_after_alpha):
            Sess_after_beta = dict(filter(lambda item: item[0]>InstanceList[0][0], Sess_after_alpha.items()))
            # {key:Sess_after_alpha[key] for key in Sess_after_alpha.keys() if key > InstanceList[0][0]}
            PrefixSpan_for_Sequential_Pattern(beta, Sess_after_beta, Record_beta, Pattern_Summary_Dict, min_len, max_len)


def PrefixSpan_for_Sequential_Pattern_new(alpha, Sess_after_alpha, Record_alpha, Pattern_Summary_Dict, length):
    min_len, max_len = 1, 1

    next_categories = findCategory(alpha, Sess_after_alpha)
    for cate in next_categories:
        ''' beta is the new pattern '''
        beta = alpha.copy(); beta.append(str(cate)); beta_len = len(beta)
        ''' get instance action of cate '''
        InstanceList = findInstanceList(cate, Sess_after_alpha)
        ''' S_beta is the suffix set; R_beta is the ; Supp_beta is the ; '''
        Sess_after_beta, Supp_beta, Record_beta = {}, {}, []

        """ 支持度计算方法 *** 闪亮登场 *** """
        '''P is the occurrence probability in each session, p_j2 recaod the last probability'''
        P, p_j2 = 0, 0
        '''InstanceList is a event set. j[0] = key, j[1]=prob '''
        for [key, prob] in InstanceList:
            '''if beta is the first topic p_star = 1, else p_star = findRecord '''
            p_star = 1.0 if beta_len - 1 <= 0 else findRecord(Record_alpha, key)
            P = prob * p_star + (1 - prob) * p_j2
            p_j2 = P
            if P > 0.0:
                Record_beta.append(Prefix_Item(prefix_name=beta, prob=P, end_pos=key))
        """ 支持度计算方法 *** 完美谢幕 *** """

        ''' filter out patterns with support equal to 0 '''
        if  beta_len >= min_len and beta_len <= max_len and P > 0.0:
            support = math.pow(P, 1 / beta_len)     # """ 针对序列模式长度进行归一化的支持度 """
            pattern_str = "; ".join(beta)
            Pattern_Summary_Dict[pattern_str] = Classical_Sequential_Pattern(pattern_name=tuple(beta), length=length, support=support)
            #print("Classical_Sequential_Pattern", tuple(beta), beta_len, support)

        """ 基于模式增长思想的递归算法 """
        if P > 0.0 and beta_len < max_len and InstanceList[0][0] + 1 < len(Sess_after_alpha):
            Sess_after_beta = dict(filter(lambda item: item[0]>InstanceList[0][0], Sess_after_alpha.items()))
            # {key:Sess_after_alpha[key] for key in Sess_after_alpha.keys() if key > InstanceList[0][0]}
            PrefixSpan_for_Sequential_Pattern(beta, Sess_after_beta, Record_beta, Pattern_Summary_Dict, min_len, max_len)


def getTotalSupp(Pattern_Summary_Dict, user_ids = [], user_type = "total"):
    total_pattern = {}
    Pattern_Summary_Dict[user_type] = {}
    #for user_id in user_ids:
    for user_id in dict(Pattern_Summary_Dict).keys():
        for pattern in dict(Pattern_Summary_Dict[user_id]).keys():
            if pattern not in total_pattern.keys():
                total_pattern[pattern] = []
                Pattern_Summary_Dict[user_type][pattern] = Classical_Sequential_Pattern(pattern_name=Pattern_Summary_Dict[user_id][pattern].pattern_name, length=Pattern_Summary_Dict[user_id][pattern].length, support=0.0)
            total_pattern[pattern].append(Pattern_Summary_Dict[user_id][pattern].support)
    pattern_support = {}
    for key in total_pattern.keys():
        support = sum(total_pattern[key])
        pattern_support[key] = support
        # support = sum(total_pattern[key]) / len(user_ids)
        Pattern_Summary_Dict[user_type][key].support = support
    pattern_support_order = sorted(pattern_support.items(), key=lambda x: x[1], reverse=True)#这是一个列表，列表内容是元组

    '''   
    #这一段并不能对字典排序
    for pattern_support_tuple in pattern_support_order:
        key = pattern_support_tuple[0]
        support = pattern_support_tuple[-1]
        Pattern_Summary_Dict["total"][key].support = support
    '''

    top_pattern_support_s = pattern_support_order[0:20]
    #top15的模式来自于哪几个文件
    for top_pattern_support in top_pattern_support_s:
        pattern = top_pattern_support[0]
        sum_support = top_pattern_support[1]
        classical_sequential_pattern = Pattern_Summary_Dict["total"][top_pattern_support[0]]
        for user_id in dict(Pattern_Summary_Dict).keys():
            if user_id != "total":
                for pattern in dict(Pattern_Summary_Dict[user_id]).keys():
                    if pattern == top_pattern_support[0]:
                        user_supportPercent = (user_id, Pattern_Summary_Dict[user_id][pattern].support / sum_support)
                        classical_sequential_pattern.appendSubsupport(user_supportPercent)
        Pattern_Summary_Dict["total"][top_pattern_support[0]] = classical_sequential_pattern
