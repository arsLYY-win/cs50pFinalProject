import csv
import pandas as pd
from docx import Document
import pdfplumber
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tkinter as tk


def main():
    # read the file provided by the user
    while True:
        filename = input("Enter the filename: ").strip()
        if isValid(filename):
            break
    wordList = readList(filename)
    d = input(
        "Do you want to recite the words in an alphabetical order? (yes/no): "
    ).strip()
    if d.lower() == "yes":
        wordList = sortAlphabetical(wordList)
    # create a trainer, check the goal first
    while True:
        goal = input("set your goal: finish in ? days ")
        pt = input("from which day on? ")
        try:
            if int(goal) > 0 and (int(pt) > 0 and int(pt) <= int(goal)):
                break
        except:
            print("Invalid input, please enter again!")
            continue
    # initialize the trainer
    trainer = Trainer(wordList, int(goal), pointer=int(pt))
    # start the reciting process
    trainer.start_Training()
    b = input("do you want to save wordlist? yes/no: ")
    # save the pdf of wordlist
    if b.strip() == "yes":
        trainer.saveList_by_day()

    # get an vocab-reciting machine named trainer(object),
    # attributes: the whole wordlist, toRecite n-words list,goal x days,pointer
    # methods: start_Training, getWordListByDay,getWordList, resetGoals


# trainer, you give it the word(list) that you want to recite today,
# it will train you by repeating the meaning and the original words again and again in random order
# 10 rounds altogether.
class Trainer(object):
    def __init__(self, wordList, goal: int, pointer: int):
        self._word_list = wordList
        self._goal = goal
        self._pointer = pointer - 1
        self._word_list_by_day = wordList[
            self._pointer
            * (len(wordList) // goal + 1) : (pointer)
            * (len(wordList) // goal + 1)
        ]

    @property
    def word_list(self):
        return self._word_list

    @property
    def goal(self):
        return self._goal

    @property
    def word_list_by_day(self):
        return self._word_list_by_day

    @property
    def pointer(self):
        return self._pointer

    @property
    def set_pointer(self, pointer):
        self._pointer = pointer

    def start_Training(self):
        wl = self._word_list_by_day

        class PageOne(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent, bg="AliceBlue")
                title_label = tk.Label(
                    self, text="单词列表", font=("Arial", 20), bg="AliceBlue"
                )
                title_label.grid(row=0, column=0, columnspan=2, pady=10)

        class PageTwo(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent, bg="AliceBlue")
                title_label = tk.Label(
                    self, text="单词列表", font=("Arial", 20), bg="AliceBlue"
                )
                title_label.grid(row=0, column=0, columnspan=2, pady=10)

        class PageThree(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent, bg="AliceBlue")
                title_label = tk.Label(
                    self, text="单词列表", font=("Arial", 20), bg="AliceBlue"
                )
                title_label.grid(row=0, column=0, columnspan=2, pady=10)

        class PageFour(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent, bg="AliceBlue")
                title_label = tk.Label(
                    self, text="单词列表", font=("Arial", 20), bg="AliceBlue"
                )
                title_label.grid(row=0, column=0, columnspan=2, pady=10)

        class PageFive(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent, bg="AliceBlue")
                title_label = tk.Label(
                    self, text="单词列表", font=("Arial", 20), bg="AliceBlue"
                )
                title_label.grid(row=0, column=0, columnspan=2, pady=10)

        root = tk.Tk()
        root.configure(bg="White")  # AliceBlue,MintCream,Azure
        root.title("trainer")
        root.geometry("640x600")

        # 侧边栏 - 步骤按钮
        step_frame = tk.Frame(root, bg="AliceBlue")  # LightSteelBlue
        step_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # 主界面区域
        main_frame = tk.Frame(root, bg="AliceBlue")  # LightCyan,AliceBlue
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 实例化页面
        pages = [
            PageOne(main_frame),
            PageTwo(main_frame),
            PageThree(main_frame),
            PageFour(main_frame),
            PageFive(main_frame),
        ]

        for page in pages:
            page.place(in_=main_frame, relx=0, rely=0, relwidth=1, relheight=1)
        pages[0].lift()

        # 切换页面
        def show_page(n: int):
            page = pages[n]
            page.lift()

        steps = ["1", "2", "3", "4", "5"]  # , "↻"

        for s in steps:
            btn = tk.Button(
                step_frame,
                text=s,
                width=3,
                height=1,
                command=lambda idx=int(s) - 1: show_page(
                    idx
                ),  # show_page((int(s) - 1))
                font=("Arial", 18),
                relief="flat",
                bg="AliceBlue",
            )
            btn.pack(pady=5)
        # 界面中内容自动响应拉伸缩小，用.pack(expand=True,...)来实现

        features = wl
        buttons_left = []
        buttons_right = []  # 两个列表分别存储左边和右边的按钮

        def create_toggle_button(parent, content, row, column):
            visible = False

            def toggle():
                nonlocal visible
                if visible:
                    btn.config(text="")
                else:
                    btn.config(text=content)
                visible = not visible

            btn = tk.Button(
                parent,
                text=content,
                font=("Arial", 22),
                width=12,
                command=toggle,
                relief=tk.GROOVE,
                bg="White",
            )
            btn.grid(row=row, column=column, padx=20, pady=8)
            return btn

        for i in range(len(wl)):
            (j, k) = (i // 5, i % 5)
            btn_left = create_toggle_button(pages[j], wl[i][0], k + 1, 0)
            buttons_left.append(btn_left)
            btn_right = create_toggle_button(pages[j], wl[i][1], k + 1, 1)
            buttons_right.append(btn_right)

            # 定义wipe和擦除列
            def wipeLeft():
                for btn in buttons_left:
                    btn.invoke()  # 清空按钮的文字

            def wipeRight():
                for btn in buttons_right:
                    btn.invoke()  # 清空按钮的文字

            # 底部左右箭头
            for i in range(len(wl) // 5):
                nav_frame = tk.Frame(pages[i], bg="AliceBlue")
                nav_frame.grid(row=7, column=0, columnspan=2, pady=20)
                btn_clearleft = tk.Button(
                    nav_frame,
                    text="wipe",
                    font=("Arial", 12),
                    command=wipeLeft,
                    width=5,
                    bg="white",
                    relief=tk.FLAT,
                )
                btn_prev = tk.Button(
                    nav_frame,
                    text="←",
                    command=lambda idx=0 if i == 0 else i - 1: show_page(idx),
                    font=("Arial", 16),
                    width=5,
                )
                btn_next = tk.Button(
                    nav_frame,
                    text="→",
                    command=lambda idx=4 if i == 4 else i + 1: show_page(idx),
                    font=("Arial", 16),
                    width=5,
                )
                btn_clearright = tk.Button(
                    nav_frame,
                    text="擦除列",
                    font=("Arial", 12),
                    command=wipeRight,
                    width=5,
                    bg="white",
                    relief=tk.FLAT,
                )
                btn_clearleft.pack(side=tk.LEFT, padx=10)
                btn_prev.pack(side=tk.LEFT, padx=10)
                btn_next.pack(side=tk.LEFT, padx=10)
                btn_clearright.pack(side=tk.LEFT, padx=10)

                # 生成每个页面的内容
        root.mainloop()

    # wirte list by day to a pdf file so that can print out and review
    def saveList_by_day(self):
        pdfmetrics.registerFont(TTFont("font_1", "font_1.ttf"))
        pdf_file = f"vocab_day{self._pointer+1}.pdf"
        margin = 2.5 * cm
        w, h = A4
        usable_width = w - 2 * margin
        pdf = SimpleDocTemplate(
            pdf_file,
            pagesize=A4,
            leftMargin=2 * margin,
            rightMargin=2 * margin,
            topMargin=margin,
            bottomMargin=margin,
        )
        l = [["english", "词意"]]
        l.extend(self._word_list_by_day)
        max_rows_per_page = 30
        table = Table(
            l,
            colWidths=[usable_width / 2, usable_width / 2],
            rowHeights=[1.2 * cm] * len(l),
            repeatRows=1,
        )
        style = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.white),  # 表头背景
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),  # 表头文字颜色
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # 居中
                ("FONTNAME", (0, 0), (-1, -1), "font_1"),  # 字体
                ("FONTSIZE", (0, 0), (-1, -1), 22),  # 字号
                ("LEADING", (0, 0), (-1, -1), 18),  # 增加行间距
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),  # 网格线
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),  # 内容背景
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
        table.setStyle(style)
        pdf.build([table])
        print(f"save to {pdf_file} successfully")


# create a new vocabulary list
# (which is an object contains lists divided into groups
# and a pointer shows which next to recite
# and a attribute of the progress's percentage)
# the user give text file and goal(how many days to recite) as input
# return an object of vocabulary list with progress percentage
def sortAlphabetical(wl: list):
    return sorted(wl, key=lambda x: x[0].lower())


# check the validity of filename
def isValid(filename: str):
    if (
        filename.endswith(".csv")
        or filename.endswith(".txt")
        or filename.endswith(".xlsx")
        or filename.endswith(".xls")
        or filename.endswith(".pdf")
        or filename.endswith(".docx")
    ):
        return True
    else:
        return False


# return a vocabulary list
def readList(filename: str):
    try:
        vocab = []
        if filename.endswith(".txt"):
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    vocab.append(line.strip().split(","))
        elif filename.endswith(".csv"):
            with open(filename, "r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    vocab.append(row)
        elif filename.endswith(".docx"):  # or filename.endswith(".doc")
            with open(filename, "rb") as file:
                doc = Document(filename)
                for table in doc.tables:
                    for row in table.rows:
                        vocab.append([cell.text.strip() for cell in row.cells])
        elif filename.endswith(".pdf"):
            with pdfplumber.open(filename) as file:
                for page in file.pages:
                    vocab.append(page.extract_table())
        elif filename.endswith(".xls") or filename.endswith(".xlsx"):
            df = pd.read_excel(filename, sheet_name="..")
            vocab = (
                df.values.tolist()
            )  # get all values in the dataframe as a list of lists
        return vocab
    except FileNotFoundError:
        exit("file doesn't exist!")
    except:
        exit("invalid file format")


if __name__ == "__main__":
    main()
