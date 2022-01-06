import os, json, yaml
#from baseFunction import *
#from baseFunction import loadEyeTrackerData, outputProbData, crateXlsFile, outputPatternToXlwt
from baseFunction import loadEyeTrackerDataNew, loadEyeTrackerData, outputProbData, outputPatternToXlwt_mutiSheet, outputRankToXlwt, outputAllinTopNToXlwt, crateXlsxFile_mutiSheet
from baseFunction import crateGazeProbData, crateGazeTrackProbData, crateGazeTrackProbData_new

from miningFuntion import PrefixSpan_for_Sequential_Pattern_muti, PrefixSpan_for_Sequential_Pattern, PrefixSpan_for_Sequential_Pattern_new, Classical_Sequential_Pattern, getTotalSupp

INF_rank = 1000000

if __name__ == "__main__":
    with open('config.yaml') as config_file:
        try:
            config = yaml.load(config_file, Loader=yaml.SafeLoader)
            CORRECT_ROOT_PATH, INCORRECT_ROOT_PATH, OUTPUT_PATH = config['CORRECT_ROOT_PATH'], config['INCORRECT_ROOT_PATH'], config["OUTPUT_PATH"]
        except:
            print("There is no config.yaml, or no information in config.yaml")
            exit(0)
        ROOT_PATH_list = []
        ROOT_PATH_list.append(INCORRECT_ROOT_PATH)
        ROOT_PATH_list.append(CORRECT_ROOT_PATH)

        Pattern_Summary_Dict_point_correct, Pattern_Summary_Dict_point_incorrect = {}, {}
        Pattern_Summary_Dict_track_correct, Pattern_Summary_Dict_track_incorrect = {}, {}
        Pattern_Summary_Dict_track_new_correct, Pattern_Summary_Dict_track_new_incorrect = {}, {}

        for root_path in ROOT_PATH_list:
            GAZE_POINT_DICT, GAZE_TRACK_DICT = {}, {}
            Pattern_Summary_Dict_point, Pattern_Summary_Dict_track, Pattern_Summary_Dict_track_new = {}, {}, {}
            for file_name in os.listdir(root_path):
                file_path = root_path + file_name
                # raw_data_dict = loadEyeTrackerData(file_path)
                raw_data_dict = loadEyeTrackerDataNew(file_path)
                user_name = str(file_name.split(".txt")[0])

                gaze_prob_data = raw_data_dict
                # gaze_prob_data = crateGazeProbData(raw_data_dict)
                # GAZE_POINT_DICT[user_name] = gaze_prob_data; print(gaze_prob_data)
                # #gazetrack_prob_data = crateGazeTrackProbData(raw_data_dict)
                # gazetrack_prob_data_muti = []
                # for i in range(2, 4):#2\3\(4)左闭右开
                #     gazetrack_prob_data_muti.append(crateGazeTrackProbData_new(raw_data_dict, i))
                # gazetrack_prob_data = {}
                # index = 0
                # #合并不同长度的
                # for i in range(len(gazetrack_prob_data_muti)):
                #     for j in range(len(gazetrack_prob_data_muti[i])):
                #         gazetrack_prob_data[index] = gazetrack_prob_data_muti[i][j]
                #         index += 1
                #
                # GAZE_TRACK_DICT[user_name] = gazetrack_prob_data; print(gazetrack_prob_data)
                #
                # """ 中间结果保存至本地 """
                # output_dir_path_1 = OUTPUT_PATH + "gaze_point/"
                # outputProbData(output_dir_path_1, file_name, gaze_prob_data)
                # output_dir_path_2 = OUTPUT_PATH + "gaze_track/"
                # outputProbData(output_dir_path_2, file_name, gazetrack_prob_data)

                """ 挖掘算法 """
                Pattern_Summary_Dict_point[user_name], Pattern_Summary_Dict_track[user_name], Pattern_Summary_Dict_track_new[user_name] = {}, {}, {}

                # PrefixSpan_for_Sequential_Pattern([], gaze_prob_data, [], Pattern_Summary_Dict_point[user_name], 2, 5)
                PrefixSpan_for_Sequential_Pattern_muti([], gaze_prob_data, [], Pattern_Summary_Dict_point[user_name], 2, 5)
                #PrefixSpan_for_Sequential_Pattern([], gazetrack_prob_data, [], Pattern_Summary_Dict_track[user_name], 2, 3)
                '''
                for i in range(2, 6):
                    gazetrack_prob_data_new = crateGazeTrackProbData_new(raw_data_dict, i)#新加的
                    PrefixSpan_for_Sequential_Pattern_new([], gazetrack_prob_data_new, [], Pattern_Summary_Dict_track_new[user_name], i)
                '''

            """ 计算模式的综合得分 """
            getTotalSupp(Pattern_Summary_Dict_point)
            # getTotalSupp(Pattern_Summary_Dict_point, user_ids= [], user_type= "nomal_students")

            getTotalSupp(Pattern_Summary_Dict_track)
            # getTotalSupp(Pattern_Summary_Dict_track, user_ids=[], user_type="nomal_students")

            getTotalSupp(Pattern_Summary_Dict_track_new)
            """ 序列模式挖掘的结果输出到xls文件中 
            sheet_name_list = ["GAZE_POINT", "GAZE_TRACK"]
            workbook, sheet_dict = crateXlsFile(OUTPUT_PATH, sheet_name_list)
            outputPatternToXlwt(sheet_dict["GAZE_POINT"], Pattern_Summary_Dict_point)
            outputPatternToXlwt(sheet_dict["GAZE_TRACK"], Pattern_Summary_Dict_track)
            """

            user_type = 'total'
            if 'in' in root_path:
                Pattern_Summary_Dict_point_incorrect = Pattern_Summary_Dict_point[user_type]#{} key=pattern,string 类型value =Classical_Sequential_Pattern
                Pattern_Summary_Dict_track_incorrect = Pattern_Summary_Dict_track[user_type]
                Pattern_Summary_Dict_track_new_incorrect = Pattern_Summary_Dict_track_new[user_type]
            else:
                Pattern_Summary_Dict_point_correct = Pattern_Summary_Dict_point[user_type]
                Pattern_Summary_Dict_track_correct = Pattern_Summary_Dict_track[user_type]
                Pattern_Summary_Dict_track_new_correct = Pattern_Summary_Dict_track_new[user_type]

            '''
            #不连续
            workbook = crateXlsxFile_mutiSheet(OUTPUT_PATH)
            outputPatternToXlwt_mutiSheet(workbook, Pattern_Summary_Dict_point)
            
            #不连续内连续
            workbook = crateXlsxFile_mutiSheet(OUTPUT_PATH)
            outputPatternToXlwt_mutiSheet(workbook, Pattern_Summary_Dict_track)
            '''


            '''
            #连续
            workbook = crateXlsxFile_mutiSheet(OUTPUT_PATH)
            outputPatternToXlwt_mutiSheet(workbook, Pattern_Summary_Dict_track_new)



            out_name = root_path[:-1]
            workbook.save(OUTPUT_PATH + out_name + ".xlsx")
            '''

        Pattern_Summary_Dict_correct = Pattern_Summary_Dict_track_correct
        Pattern_Summary_Dict_incorrect = Pattern_Summary_Dict_track_incorrect
        top_n = 20
        threshold = 20
        i = 0
        incorrect_rank_correct_rank = [] #tuple
        flag = 0
        for pattern in Pattern_Summary_Dict_incorrect.keys():
            if i >= top_n:
                break
            i += 1
            for find_pattern in Pattern_Summary_Dict_correct.keys():
                if pattern == find_pattern:
                    flag = 1
                    difference_value = Pattern_Summary_Dict_correct[find_pattern].rank - Pattern_Summary_Dict_incorrect[pattern].rank
                    temp_tuple = (pattern, Pattern_Summary_Dict_incorrect[pattern].rank,
                                  Pattern_Summary_Dict_correct[find_pattern].rank, difference_value)
                    if abs(difference_value) > threshold:
                        temp_tuple = temp_tuple + (1, )#mark一下
                    incorrect_rank_correct_rank.append(temp_tuple)
                    break
            if flag == 0:#没有出现在另一个表中
                difference_value = 'INF'
                temp_tuple = (pattern, Pattern_Summary_Dict_incorrect[pattern].rank, INF_rank, INF_rank, 1)  # mark一下
                incorrect_rank_correct_rank.append(temp_tuple)

        i = 0
        correct_rank_incorrect_rank = []  # tuple
        flag = 0
        for pattern in Pattern_Summary_Dict_correct.keys():
            if i >= top_n:
                break
            i += 1
            for find_pattern in Pattern_Summary_Dict_incorrect.keys():
                if pattern == find_pattern:
                    flag = 1
                    difference_value = Pattern_Summary_Dict_incorrect[find_pattern].rank - Pattern_Summary_Dict_correct[pattern].rank
                    temp_tuple = (pattern, Pattern_Summary_Dict_correct[pattern].rank, Pattern_Summary_Dict_incorrect[find_pattern].rank, difference_value)
                    if abs(difference_value) > threshold:
                        temp_tuple = temp_tuple + (1, ) # mark一下
                    correct_rank_incorrect_rank.append(temp_tuple)
                    break
            if flag == 0:#没有出现在另一个表中
                temp_tuple = (pattern, Pattern_Summary_Dict_correct[pattern].rank, INF_rank, INF_rank, 1)  # mark一下
                correct_rank_incorrect_rank.append(temp_tuple)

        #都在topN中的序列
        all_in_topN = []
        for tuple in incorrect_rank_correct_rank:
            if tuple[1] <= top_n and tuple[2] <= top_n:
                all_in_topN.append(tuple)

        rank_workbook = crateXlsxFile_mutiSheet(OUTPUT_PATH)
        outputRankToXlwt(rank_workbook, incorrect_rank_correct_rank, "disconsequence-incorrect", threshold)
        outputRankToXlwt(rank_workbook, correct_rank_incorrect_rank, "disconsequence-correct", threshold)
        outputAllinTopNToXlwt(rank_workbook, all_in_topN)

        rank_workbook.save(OUTPUT_PATH + 'incorrect_rank_correct_rank' + ".xlsx")
