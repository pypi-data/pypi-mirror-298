from caolib.color_text import colorTxt, color

# rgb颜色示例
print(colorTxt("666"))
print(colorTxt("666", fg=color(255, 0, 80)))
print(colorTxt("666", bg=color(255, 100, 0)))
print(colorTxt("666", fg=color(0, 255, 0)))
print(colorTxt("666", bg=color(0, 0, 255)))
print(colorTxt("666", fg=color(255, 255, 0), bg=color(0, 255, 255)))
print()
# 16进制颜色示例
print(colorTxt("666", fg=color("#FF0050")))
print(colorTxt("666", bg=color("#FF6400")))
print(colorTxt("666", fg=color("#00FF00")))
print(colorTxt("666", bg=color("#0000FF")))
print(colorTxt("666", fg=color("#FFFF00"), bg=color("#00FFFF")))