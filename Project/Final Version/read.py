import pandas as pd

# 解压缩文件
import zipfile
with zipfile.ZipFile("C:/Users/Hema/Downloads/Compressed/100015657.parquet.zip", 'r') as zip_ref:
    zip_ref.extractall("C:/Users/Hema/Downloads/Compressed")

# 读取Parquet文件
df = pd.read_parquet("C:/Users/Hema/Downloads/Compressed/100015657.parquet")

# 打印数据框的前几行
print(df.head())
