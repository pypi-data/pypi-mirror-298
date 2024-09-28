import math


def find_points_on_line(k, b, x0, length):
    y0 = k * x0 + b
    # 计算判别式
    discriminant = (length * length - (y0 - b) ** 2) / (1 + k ** 2)

    # 计算两个解
    x1 = (x0 + length * k - (y0 - b) * k) / (1 + k ** 2)
    x2 = (x0 - length * k - (y0 - b) * k) / (1 + k ** 2)

    # 计算对应的y值
    y1 = k * x1 + b
    y2 = k * x2 + b

    return (x1, y1), (x2, y2)


# 示例使用
k = 1  # 斜率
b = 0  # y轴截距
x0 = 0  # 点的x坐标
length = 5  # 距离

points = find_points_on_line(k, b, x0, length)
print("Points on the line:", points)