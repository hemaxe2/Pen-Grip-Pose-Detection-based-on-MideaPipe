import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


def load_and_clean_data(file_path):
    # 加载数据集
    data = pd.read_excel(file_path)

    # 删除特征值为空的行
    data.dropna(subset=feature_columns, inplace=True)

    # 删除Gesture不是"Correct Posture"或"Wrong Posture"的行
    data = data[data['Gesture'].isin(['Correct Posture', 'Wrong Posture'])]

    # 将"Left"和"Right"转换为0和1
    data['Hand'] = data['Hand'].map({'Left': 0, 'Right': 1})

    # 将"Gesture"转换为数值型变量，1代表"Correct Posture"，0代表"Wrong Posture"
    data['Gesture'] = data['Gesture'].map({'Correct Posture': 1, 'Wrong Posture': 0})

    return data


def descriptive_analysis_and_plotting(data, save_dir):
    # 描述性统计分析
    description = data[feature_columns].describe(percentiles=[.05, .10, .20, .30, .50, .80, .90, .95])
    print(description)

    # 计算百分位数值
    percentiles_values = np.percentile(data[feature_columns], [5, 10, 20, 30, 50, 80, 90, 95], axis=0)

    # 绘制密度图并保存
    print("绘制密度图...")
    plt.figure(figsize=(20, 15))
    data[feature_columns].plot(kind='density', subplots=True, layout=(6, 3), sharex=False, figsize=(20, 15))
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, '密度图.png'))
    print("密度图已保存")
    plt.close()

    # 绘制箱线图并保存
    print("绘制箱线图...")
    plt.figure(figsize=(20, 10))
    boxplot = data[feature_columns].boxplot(figsize=(20, 10))
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(save_dir, '箱线图.png'))
    print("箱线图已保存")
    plt.close()

    # 绘制直方图并标记指定百分位数值
    print("绘制直方图...")
    plt.figure(figsize=(20, 15))
    for i, column in enumerate(feature_columns):
        plt.subplot(6, 3, i + 1)
        sns.histplot(data[column], bins=20, kde=True)
        plt.title(column)

        # 在直方图上标记指定百分位数值
        for percentile, value in zip([5, 10, 20, 30, 50, 80, 90, 95], percentiles_values[:, i]):
            plt.axvline(x=value, color='red', linestyle='--')
            plt.text(value, 10, f'{percentile}% ({value:.2f})', fontsize=8, rotation=90, ha='right', va='bottom',
                     color='red')

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, '直方图与百分位数值.png'))
    print("直方图已保存")
    plt.close()


if __name__ == "__main__":
    # 文件路径
    wrong_data_path = "Wrong Hand  Gestures Data.xlsx"
    correct_data_path = "Correct Hand  Gestures Data.xlsx"

    # 特征列
    feature_columns = ['Thumb Angle', 'Index Angle', 'Middle Angle', 'Ring Angle', 'Pinky Angle',
                       'Angle 5', 'Angle 6', 'Angle 7', 'Angle 8', 'Angle 9', 'Angle 10', 'Angle 11',
                       'Distance 48', 'Distance 37', 'Distance 26', 'distance_812', 'distance_1216', 'distance_1620']

    # 创建保存图片的文件夹
    wrong_save_dir = 'Results_of_correct_gestures'
    correct_save_dir = 'Results of incorrect gestures'

    for save_dir, data_path in zip([wrong_save_dir, correct_save_dir], [wrong_data_path, correct_data_path]):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 加载并清洗数据
        data = load_and_clean_data(data_path)

        # 进行描述性统计分析和绘图
        descriptive_analysis_and_plotting(data, save_dir)
