from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import numpy as np
import os

# 创建 TensorBoard 回调
log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

# 数据集信息
no_sequences = 30
sequence_length = 3
DATA_PATH = os.path.join('MP_Data')
actions = np.array(['hello', 'happy', 'meet', 'you', 'like', 'how', 'more', 'two', 'three', 'no', 'right', 'want', 'wrong', 'null'])
label_map = {label:num for num, label in enumerate(actions)}

# 加载数据
sequences, labels = [], []
for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

X = np.array(sequences)
y = to_categorical(labels).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

# 构建模型
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(3,126)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# 训练模型
model.fit(X_train, y_train, epochs=50, callbacks=[tb_callback])

# 打印模型摘要
model.summary()

# 保存模型
model.save('action.h5')

# 生成模型结构图像并保存
from tensorflow.keras.utils import plot_model
plot_model(model, to_file='model_structure.png', show_shapes=True, show_layer_names=True)
