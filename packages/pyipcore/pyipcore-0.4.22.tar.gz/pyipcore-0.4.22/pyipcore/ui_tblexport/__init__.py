from pyipcore.ipc_utils import *

import pandas as pd

def MatrixArrayRead(
        tbl: pd.DataFrame,
        offset: tuple[int, int],  # 忽略起始的若干列和行，即(offx, offy)
        target: tuple[int, int],  # 目标‘矩阵’的宽和高
        delta: tuple[int, int],  # 矩阵的间隔
        *,
        header: bool = True,  # 描述target的第一行是否是表头  # 如果是表头，要检查每个表头是否一致
        index: bool = True    # 描述target的第一列是否是索引
) -> pd.DataFrame:  # 将所有target纵向拼接.
    # 切换为pd格式
    offset = (offset[1], offset[0])
    target = (target[1], target[0])
    delta = (delta[1], delta[0])

    _shape = tbl.shape
    # 计算shape可以容纳的矩阵数量
    _full_size = (target[0] + delta[0], target[1] + delta[1])

    # 计算可以提取的矩阵数量
    num_matrices_x = (_shape[1] - offset[0] - (target[1] - 1) * delta[1] - 1) // _full_size[1] + 1
    num_matrices_y = (_shape[0] - offset[1] - (target[0] - 1) * delta[0] - 1) // _full_size[0] + 1

    matrices = []

    for y in range(num_matrices_y):
        for x in range(num_matrices_x):
            start_x = offset[0] + x * _full_size[1]
            start_y = offset[1] + y * _full_size[0]
            end_x = start_x + target[1]
            end_y = start_y + target[0]

            # 如果超出了DataFrame的边界，则跳过
            if end_x > _shape[1] or end_y > _shape[0]:
                continue

            # 提取矩阵
            matrix = tbl.iloc[start_y:end_y, start_x:end_x]

            # 如果需要检查表头一致性
            if header and y > 0:
                for i in range(target[0]):
                    if not pd.Series.equals(matrices[0].iloc[:, i], matrix.iloc[:, i]):
                        raise ValueError("表头不一致")

            # # 如果需要检查索引列
            # if index and x > 0:
            #     if not pd.Series.equals(matrices[0].iloc[:, 0], matrix.iloc[:, 0]):
            #         raise ValueError("索引列不一致")

            matrices.append(matrix.iloc[:target[0], :target[1]])

    # 将所有矩阵纵向拼接
    result = pd.concat(matrices, axis=0)
    return result



# 示例使用
# 创建一个示例DataFrame
data = {
    'A': range(10),
    'B': range(10, 20),
    'C': range(20, 30),
    'D': range(30, 40)
}
df = pd.DataFrame(data)
# save
df.to_csv("test.csv", index=False)

# 调用函数
result = MatrixArrayRead(df, offset=(1, 1), target=(2, 2), delta=(1, 1), header=False, index=False)
print(result)



if __name__ == '__main__':
    ...






# if __name__ == '__main__':
#     dlst = [
#         {"name": "board.leds.0", "pin": "A1", "direction": Direction.OUT, "iotype": IoType.LV33, "pull": Pull.FLOAT},
#         {"name": "board.leds.1", "pin": "A2", "direction": Direction.OUT, "iotype": IoType.LV33, "pull": Pull.FLOAT},
#         {"name": "board.leds.2", "pin": "A3", "direction": Direction.OUT, "iotype": IoType.LV33, "pull": Pull.FLOAT},
#         {"name": "board.leds.3", "pin": "A4", "direction": Direction.OUT, "iotype": IoType.LV33, "pull": Pull.FLOAT},
#         {"name": "board.leds.4", "pin": "A5", "direction": Direction.OUT, "iotype": IoType.LV33, "pull": Pull.FLOAT},
#         {"name": "board.leds.5", "pin": "A6", "direction": Direction.OUT, "iotype": IoType.LV33, "pull": Pull.FLOAT},
#         {"name": "board.leds.6", "pin": "A7", "direction": Direction.OUT, "iotype": IoType.LV33, "pull": Pull.FLOAT},
#         {"name": "board.leds.7", "pin": "A8", "direction": Direction.OUT, "iotype": IoType.LV33, "pull": Pull.FLOAT},
#     ]
#     pios = LogicIoDef.FromTableDict(dlst)
#
#     for pio in pios:
#         print(pio)
