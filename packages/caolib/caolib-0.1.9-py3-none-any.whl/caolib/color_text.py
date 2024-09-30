# Description: This file contains the class color and the function colorTxt.
class color:
    def __init__(self, red, green=None, blue=None):
        if green is None and blue is None:
            hex_color = red.lstrip("#")
            self.red = int(hex_color[0:2], 16)
            self.green = int(hex_color[2:4], 16)
            self.blue = int(hex_color[4:6], 16)
        else:
            self.red = red
            self.green = green
            self.blue = blue

    def __str__(self):
        return f"{self.red};{self.green};{self.blue}"

# 生成颜色代码
def colorTxt(txt, fg=None, bg=None):
    if txt:
        color_code = ""
        if fg:
            color_code += f"\033[38;2;{fg}m"
        if bg:
            color_code += f"\033[48;2;{bg}m"
        color_code += f"{txt}\033[0m"
        return color_code