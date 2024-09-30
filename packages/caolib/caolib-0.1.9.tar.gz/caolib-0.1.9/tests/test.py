from bin_color_text.color_text import colorTxt, color

# rgb颜色示例
print(colorTxt("666"))
print(colorTxt("666", foreground=color(255, 0, 80)))
print(colorTxt("666", background=color(255, 100, 0)))
print(colorTxt("666", foreground=color(0, 255, 0)))
print(colorTxt("666", background=color(0, 0, 255)))
print(colorTxt("666", foreground=color(255, 255, 0), background=color(0, 255, 255)))
print()
# 16进制颜色示例
print(colorTxt("666", foreground=color("#FF0050")))
print(colorTxt("666", background=color("#FF6400")))
print(colorTxt("666", foreground=color("#00FF00")))
print(colorTxt("666", background=color("#0000FF")))
print(colorTxt("666", foreground=color("#FFFF00"), background=color("#00FFFF")))