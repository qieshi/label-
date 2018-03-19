#======================  
# imports  
#======================
import os
import tkinter as tk  
from tkinter import ttk  
from tkinter import scrolledtext  
from tkinter import Menu  
from tkinter import Spinbox  
from tkinter import messagebox as mBox
from PIL import Image, ImageFont, ImageDraw
import re
from barcode.writer import ImageWriter
from barcode.codex import Code39

###################################################################
#           功能：写入文字
#           2018年3月11日14:59:59
###################################################################
def Command_WriteText(drawObject, line):
    if (re.search("\^A0N\,([0-9]+)\,([0-9]+)\^FD", line) != None):
        # 写入的位置
        position = re.search("(^\^F[A-Z])([-0-9]+)\,([-0-9]+)\^", line)
        position = [int(position.group(2)), int(position.group(3))]
        # 设置字体
        FontSize = re.search("\^A0N\,([0-9]+)\,([0-9]+)\^FD", line)  # 字体大小
        FontSize = int(FontSize.group(1))
        FontPath = r"C:\Windows\Fonts\simhei.ttf"  # 字体路径
        Font = ImageFont.truetype(FontPath, FontSize)
        # 写入白纸的内容
        text = re.search("(\^FD)([\w*!@#$.%^&()\s]+)(\^FS$)", line)
        text = text.group(2)
        # 开始写入
        drawObject.text(position, text, font=Font)

###################################################################
#           功能：生成条形码图片
#           2018年3月11日16:18:34
###################################################################
def generagteBarCode(blank, line):
    if(re.search("\^B[\w*!@#$,.%^&()\s]+\^FS", line)):
        imagewriter = ImageWriter()
        text = re.search("\^FD([\w*!@#$.%^&()\s]+)\^FS",line)
        text = text.group(1)
        position = re.search("\^F[A-Z]([-0-9]+),([-0-9]+)\^", line)
        position = (int(position.group(1)), int(position.group(2)))
        #保存到图片中
        ean = Code39(text, writer=imagewriter, add_checksum=False)
        ean.save('.\IMAGE\BARCODE\image2',options={'font_size':0, 'module_width':0.14, 'module_height':8})
        #粘贴到空白图片上
        filename = ".\IMAGE\BARCODE\image2.png"
        Imagepaste(blank, filename, position)

###################################################################
#           功能：将图片粘贴到指定位置
#           2018年3月11日16:23:01
###################################################################
def Imagepaste(srcimage, filename, imageposition):
    im = Image.open(filename)
    srcimage.paste(im, imageposition)

def Command_WriteImage(srcimage, drawObject, line):
    if(re.search("\^IM([\w*!@#$.%^&()\s]+)\^FS",line) != None):
        # 写入的位置
        position = re.search("\^F[A-Z]([-0-9]+),([-0-9]+)\^", line)
        #print(position, "   ", line)
        position = [int(position.group(1)), int(position.group(2))+15]
        # 写入的文件名
        filename = re.search("\^IM([\w*!@#$.%^&()\s]+)\^FS",line)
        filename = r".\\IMAGE\\" + filename.group(1) + r".BMP"
        try:
            Imagepaste(srcimage, filename, tuple(position))
        except:
            pass
    elif(re.search("\^GB([\w*!@#$,.%^&()\s]+)\^FS",line) != None):
        rect_position = re.search("(^\^F[A-Z])([-0-9]+)\,([-0-9]+),\^", line)
        offset = re.search("\^GB([0-9]+),([0-9]+),([0-9]+)",line)
        #print(rect_position.group(0))
        rect_position = [int(rect_position.group(2)), int(rect_position.group(3))+17,
                         int(rect_position.group(2))+int(offset.group(1)), int(rect_position.group(3))+int(offset.group(2))+17]
        drawObject.rectangle(rect_position, outline = 'black')
  
######################################################################
#
#       Label整体移动
#
######################################################################
def label_move():
    lines = scr.get("0.0","end")
    lines = lines.split('\n')
    lines = lines[:-1]
    try:
        juli1 = int(name.get())
    except:
        _msgBox2()
        return
    scr.delete("1.0", "end") # 使用 delete
    if(bookChosen.get() == '左移'):
        for index, text in enumerate(lines):
            if(re.search('\^F[A-Z]([-0-9]+)\,([-0-9]+)', text) != None):
                text = re.split(',',text)
                temp = text[0][:3]
                text[0] = text[0][3:]
                text[0] = str(int(text[0])-juli1)
                text[0] = temp + text[0]
                text = ','.join(text)
                scr.insert('insert', text+'\n')
            else:
                scr.insert('insert', text+'\n')
    elif(bookChosen.get() == '右移'):
        
        for index, text in enumerate(lines):
            if(re.search('\^F[A-Z]([-0-9]+)\,([-0-9]+)', text) != None):
                text = re.split(',',text)
                temp = text[0][:3]
                text[0] = text[0][3:]
                text[0] = str(int(text[0])+juli1)
                text[0] = temp + text[0]
                text = ','.join(text)
                scr.insert('insert', text+'\n')
            else:
                scr.insert('insert', text+'\n')
    elif(bookChosen.get() == '上移'):
        for index, text in enumerate(lines):
            if(re.search('\^F[A-Z]([-0-9]+)\,([-0-9]+)', text) != None):
                text = re.split(',',text)
                text[1] = text[1].split('^')
                text[1][0] = str(int(text[1][0])-juli1)
                text[1] = '^'.join(text[1])
                text = ','.join(text)
                scr.insert('insert', text+'\n')
            else:
                scr.insert('insert', text+'\n')
    elif(bookChosen.get() == '下移'):
        for index, text in enumerate(lines):
            if(re.search('\^F[A-Z]([-0-9]+)\,([-0-9]+)', text) != None):
                text = re.split(',',text)
                text[1] = text[1].split('^')
                text[1][0] = str(int(text[1][0])+juli1)
                text[1] = '^'.join(text[1])
                text = ','.join(text)
                scr.insert('insert', text+'\n')
            else:
                scr.insert('insert', text+'\n')

def label_bat_generate():
    code_len = len(name2.get())
    code_int = int(name2.get())
    code_source = name1.get() + name2.get() + name3.get()
    code_source = code_source.strip('^FS')
    code_source = code_source.split('^FD')
    code_source = code_source[-1]
    
    with open('result.txt', 'w+') as dst:
        for i in range(0, int(name4.get())):
            lines = scr1.get("0.0","end")
            lines = lines.split('\n')
            lines = lines[:-1]
            lines = list(map(lambda x: x+'\n', lines))
            
            code_temp = code_int + i
            code_temp = '{0:0{width}}'.format(code_temp, width=code_len)
            code_full = name1.get() + code_temp + name3.get()
            code_full = code_full.strip('^FS')
            code_full = code_full.split('^FD')
            code_full = code_full[-1]
 
            for index, line in enumerate(lines):     
                lines[index] = line.replace(code_source, code_full)
            lines[-1] = lines[-1] + "\n\n"
            dst.writelines(lines)
    os.system("notepad result.txt")
        
# Create instance  
win = tk.Tk()
  
# Add a title         
win.title("Python 图形用户界面")  
  
# Disable resizing the GUI  
win.resizable(0,0)  
  
# Tab Control introduced here --------------------------------------  
tabControl = ttk.Notebook(win)          # Create Tab Control  
  
tab1 = ttk.Frame(tabControl)            # Create a tab   
tabControl.add(tab1, text='Label 仿真与整体移动')      # Add the tab  
  
tab2 = ttk.Frame(tabControl)            # Add a second tab  
tabControl.add(tab2, text='label批量生成')      # Make second tab visible  
  
tabControl.pack(expand=1, fill="both")  # Pack to make visible  
# ~ Tab Control introduced here -----------------------------------------  
  
#---------------Tab1控件介绍------------------#  
# We are creating a container tab3 to hold all other widgets  
monty = ttk.LabelFrame(tab1, text='工作区')  
monty.grid(column=0, row=0, padx=12, pady=6)

monty2 = ttk.LabelFrame(tab2, text='工作区2')  
monty2.grid(column=0, row=0, padx=12, pady=6)

ttk.Label(monty2, text="    条形码头部").grid(column=0, row=0, sticky='W')
ttk.Label(monty2, text="    条形码中部").grid(column=1, row=0, sticky='W')
ttk.Label(monty2, text="    条形码尾部").grid(column=2, row=0, sticky='W')
  
# Modified Button Click Function  
def clickMe():  
    lines = scr.get("0.0","end")
    lines = lines.split('\n')
    #生成一个空白页
    blanksize = [700,900]
    blank = Image.new("RGB",blanksize, "white")
    #生成画笔工具
    drawObject = ImageDraw.Draw(blank)
    #画笔颜色:黑色
    drawObject.ink = 0
    for index, line in enumerate(lines):
        generagteBarCode(blank, line)
    for index, line in enumerate(lines):
        Command_WriteImage(blank, drawObject, line)
#3.将命令中的文字弄在label上
    for index, line in enumerate(lines):
        Command_WriteText(drawObject, line)
    #显示最终结果
    blank.show()
  
# Changing our Label  
ttk.Label(monty, text="移动距离:").grid(column=0, row=0, sticky='W')  
  
# Adding a Textbox Entry widget  
name = tk.StringVar()  
nameEntered = ttk.Entry(monty, width=12, textvariable=name)  
nameEntered.grid(column=0, row=1)  

name1 = tk.StringVar()  
nameEntered1 = ttk.Entry(monty2, width=8, textvariable=name1)  
nameEntered1.grid(column=0, row=1)

name2 = tk.StringVar()
nameEntered2 = ttk.Entry(monty2, width=8, textvariable=name2)  
nameEntered2.grid(column=1, row=1)

name3 = tk.StringVar()  
nameEntered3 = ttk.Entry(monty2, width=8, textvariable=name3)  
nameEntered3.grid(column=2, row=1)

name4 = tk.StringVar()  
nameEntered4 = ttk.Entry(monty2, width=10, textvariable=name4)  
nameEntered4.grid(column=1, row=4) 

# Adding a Button  
action = ttk.Button(monty,text="仿真",width=10,command=clickMe)     
action.grid(column=2,row=1,rowspan=1,ipady=1)

action1 = ttk.Button(monty,text="移动",width=10,command=label_move)     
action1.grid(column=2,row=0,rowspan=1,ipady=1)  

action2 = ttk.Button(monty2,text="生成",width=10,command=label_bat_generate)     
action2.grid(column=2,row=4,rowspan=1,ipady=1)

ttk.Label(monty, text="设置整体移动方向:").grid(column=1, row=0,sticky='W')
ttk.Label(monty2, text="生成数量：").grid(column=0, row=4,sticky='W')  
  
# Adding a Combobox  
book = tk.StringVar()  
bookChosen = ttk.Combobox(monty, width=12, textvariable=book)  
bookChosen['values'] = ('左移','右移','上移','下移')  
bookChosen.grid(column=1, row=1)  
bookChosen.current(0)  #设置初始显示值，值为元组['values']的下标  
bookChosen.config(state='readonly')  #设为只读模式  
   
# Using a scrolled Text control      
scrolW  = 40; scrolH  =  5  
scr = scrolledtext.ScrolledText(monty, width=scrolW, height=scrolH, wrap=tk.WORD)  
scr.grid(column=0, row=3, sticky='WE', columnspan=3)

scr1 = scrolledtext.ScrolledText(monty2, width=scrolW, height=scrolH, wrap=tk.WORD)  
scr1.grid(column=0, row=3, sticky='WE', columnspan=3)
  
# 一次性控制各控件之间的距离  
for child in monty.winfo_children():   
    child.grid_configure(padx=3,pady=1)  
# 单独控制个别控件之间的距离  
action.grid(column=2,row=1,rowspan=2,padx=6)  
#---------------Tab1控件介绍------------------#   
  
  
  
def _msgBox2():  
    mBox.showwarning('Python Message Warning Box', '请输入数字！')  

  
  
  
# Change the main windows icon  
win.iconbitmap(r'.\label.ico')  
  
# Place cursor into name Entry  
nameEntered.focus()        
#======================  
# Start GUI  
#======================  
win.mainloop()
