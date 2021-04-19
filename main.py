import os, json, yaml
#from baseFunction import *
#from baseFunction import loadEyeTrackerData, outputProbData, crateXlsFile, outputPatternToXlwt
from baseFunction import loadEyeTrackerData, outputProbData, outputPatternToXlwt_mutiSheet, crateXlsxFile_mutiSheet
from baseFunction import crateGazeProbData, crateGazeTrackProbData, crateGazeTrackProbData_new

from miningFuntion import PrefixSpan_for_Sequential_Pattern, PrefixSpan_for_Sequential_Pattern_new, Classical_Sequential_Pattern, getTotalSupp



if __name__ == "__main__":
    with open('config.yaml') as config_file:
        try:
            config = yaml.load(config_file, Loader=yaml.SafeLoader)
            ROOT_PATH, OUTPUT_PATH = config['ROOT_PATH'], config["OUTPUT_PATH"]
        except:
            print("There is no config.yaml, or no information in config.yaml")
            exit(0)

        GAZE_POINT_DICT, GAZE_TRACK_DICT = {}, {}
        Pattern_Summary_Dict_point, Pattern_Summary_Dict_track = {}, {}
        Pattern_Summary_Dict_track_new = {}
        for file_name in os.listdir(ROOT_PATH):
            file_path = ROOT_PATH + file_name
            raw_data_dict = loadEyeTrackerData(file_path)
            user_name = str(file_name.split(".txt")[0])

            gaze_prob_data = crateGazeProbData(raw_data_dict)
            GAZE_POINT_DICT[user_name] = gaze_prob_data; print(gaze_prob_data)
            #gazetrack_prob_data = crateGazeTrackProbData(raw_data_dict)
            gazetrack_prob_data_muti = []
            for i in range(2, 5):#2\3\4
                gazetrack_prob_data_muti.append(crateGazeTrackProbData_new(raw_data_dict, i))
            gazetrack_prob_data = gazetrack_prob_data_muti[0]
            for i in range(len(gazetrack_prob_data_muti)):
                gazetrack_prob_data


            GAZE_TRACK_DICT[user_name] = gazetrack_prob_data; print(gazetrack_prob_data)

            """ 中间结果保存至本地 """
            output_dir_path_1 = OUTPUT_PATH + "gaze_point/"
            outputProbData(output_dir_path_1, file_name, gaze_prob_data)
            output_dir_path_2 = OUTPUT_PATH + "gaze_track/"
            outputProbData(output_dir_path_2, file_name, gazetrack_prob_data)

            """ 挖掘算法 """
            Pattern_Summary_Dict_point[user_name], Pattern_Summary_Dict_track[user_name], Pattern_Summary_Dict_track_new[user_name]= {}, {}, {}
            PrefixSpan_for_Sequential_Pattern([], gaze_prob_data, [], Pattern_Summary_Dict_point[user_name], 2, 4)
            PrefixSpan_for_Sequential_Pattern([], gazetrack_prob_data, [], Pattern_Summary_Dict_track[user_name], 2, 4)
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

        '''
        #不连续
        workbook = crateXlsxFile_mutiSheet(OUTPUT_PATH)
        outputPatternToXlwt_mutiSheet(workbook, Pattern_Summary_Dict_point)
        '''


        #不连续内连续
        workbook = crateXlsxFile_mutiSheet(OUTPUT_PATH)
        outputPatternToXlwt_mutiSheet(workbook, Pattern_Summary_Dict_track)



        '''
        #连续
        workbook = crateXlsxFile_mutiSheet(OUTPUT_PATH)
        outputPatternToXlwt_mutiSheet(workbook, Pattern_Summary_Dict_track_new)
        '''


        workbook.save(OUTPUT_PATH + "Sequential_Pattern.xlsx")
