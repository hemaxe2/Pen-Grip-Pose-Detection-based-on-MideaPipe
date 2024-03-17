import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 加载数据集并进行数据清洗
data = pd.read_excel("hand_gestures_data.xlsx")

# 删除特征值为空的行
data.dropna(subset=['Thumb Angle', 'Index Angle', 'Middle Angle', 'Ring Angle', 'Pinky Angle',
                    'Angle 5', 'Angle 6', 'Angle 7', 'Angle 8', 'Angle 9', 'Angle 10', 'Angle 11',
                    'Distance 48', 'Distance 37', 'Distance 26', 'distance_812', 'distance_1216', 'distance_1620'], inplace=True)

# 删除Gesture不是"Correct Posture"或"Wrong Posture"的行
data = data[data['Gesture'].isin(['Correct Posture', 'Wrong Posture'])]

# 将"Left"和"Right"转换为0和1
data['Hand'] = data['Hand'].map({'Left': 0, 'Right': 1})

# 将"Gesture"转换为数值型变量，1代表"Correct Posture"，0代表"Wrong Posture"
data['Gesture'] = data['Gesture'].map({'Correct Posture': 1, 'Wrong Posture': 0})

# 2. 描述性统计分析和绘图
feature_columns = ['Thumb Angle', 'Index Angle', 'Middle Angle', 'Ring Angle', 'Pinky Angle',
                   'Angle 5', 'Angle 6', 'Angle 7', 'Angle 8', 'Angle 9', 'Angle 10', 'Angle 11',
                   'Distance 48', 'Distance 37', 'Distance 26', 'distance_812', 'distance_1216', 'distance_1620']

# 描述性统计分析
description = data[feature_columns].describe()
print(description)

# 绘制直方图
data[feature_columns].hist(figsize=(20, 15))
plt.tight_layout()
plt.show()

# 绘制密度图
data[feature_columns].plot(kind='density', subplots=True, layout=(6, 3), sharex=False, figsize=(20, 15))
plt.tight_layout()
plt.show()

# 绘制箱线图
data[feature_columns].boxplot(figsize=(20, 10))
plt.xticks(rotation=45)
plt.show()

# 3. 计算特征与目标变量之间的相关性
# 计算相关性矩阵
correlation_matrix = data.corr()

# 提取与目标变量"Gesture"相关的相关系数
gesture_correlation = correlation_matrix['Gesture'].drop(['Gesture', 'Hand'])

# 绘制热力图
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# 4. 使用卡方检验、信息增益等方法来筛选特征
# 这部分需要根据具体的机器学习模型和特征选择的方法来进行进一步操作
# 在这里可以使用Scikit-learn中的特征选择模块来进行操作
