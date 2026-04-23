import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import re
import jieba

# 英文文字處理
def count_words(str1):

    # 放處理好句子的 單詞:出現次數
    dict_words = {}

    # 存句子中的單詞
    words = []

    # 文字雲不用，要去掉的代名詞、冠詞...
    drop_words = [
        "a", "A", "an", "An", "the", "The",

        "i", "I", "me", "Me", "my", "My", "mine", "Mine", "myself", "Myself",
        "you", "You", "your", "Your", "yours", "Yours", "yourself", "Yourself", "yourselves", "Yourselves",
        "he", "He", "him", "Him", "his", "His", "himself", "Himself",
        "she", "She", "her", "Her", "hers", "Hers", "herself", "Herself",
        "it", "It", "its", "Its", "itself", "Itself",
        "we", "We", "us", "Us", "our", "Our", "ours", "Ours", "ourselves", "Ourselves",
        "they", "They", "them", "Them", "their", "Their", "theirs", "Theirs", "themselves", "Themselves",

        "am", "Am", "is", "Is", "are", "Are", "was", "Was", "were", "Were", "be", "Be", "being", "Being", "been", "Been",
        "do", "Do", "does", "Does", "did", "Did", "doing", "Doing", "done", "Done",
        "have", "Have", "has", "Has", "had", "Had", "having", "Having",
        "can", "Can", "could", "Could", "may", "May", "might", "Might", "must", "Must",
        "shall", "Shall", "should", "Should", "will", "Will", "would", "Would",

        "and", "And", "but", "But", "or", "Or", "so", "So",
        "because", "Because", "although", "Although", "though", "Though",
        "if", "If", "while", "While", "when", "When", "before", "Before", "after", "After",
        "since", "Since", "unless", "Unless",

        "in", "In", "on", "On", "at", "At", "by", "By", "for", "For", "with", "With",
        "about", "About", "from", "From", "to", "To", "of", "Of", "into", "Into",
        "onto", "Onto", "over", "Over", "under", "Under", "between", "Between",
        "among", "Among", "through", "Through", "during", "During", "without", "Without",
        "within", "Within", "against", "Against", "toward", "Toward", "towards", "Towards",
        "around", "Around", "near", "Near", "off", "Off", "up", "Up", "down", "Down", "out", "Out",

        "this", "This", "that", "That", "these", "These", "those", "Those",
        "some", "Some", "any", "Any", "many", "Many", "much", "Much", "few", "Few",
        "more", "More", "most", "Most", "each", "Each", "every", "Every", "all", "All",
        "both", "Both", "either", "Either", "neither", "Neither", "another", "Another",
        "other", "Other", "such", "Such",

        "very", "Very", "really", "Really", "just", "Just", "also", "Also",
        "only", "Only", "even", "Even", "still", "Still", "quite", "Quite",
        "rather", "Rather", "too", "Too", "well", "Well", "then", "Then",
        "than", "Than", "here", "Here", "there", "There",

        "what", "What", "which", "Which", "who", "Who", "whom", "Whom",
        "whose", "Whose", "where", "Where", "when", "When", "why", "Why", "how", "How",

        "not", "Not", "no", "No", "nor", "Nor", "yes", "Yes",

        "however", "However", "therefore", "Therefore", "thus", "Thus", "moreover", "Moreover",
        "furthermore", "Furthermore", "meanwhile", "Meanwhile", "otherwise", "Otherwise", "besides", 
        "Besides", "instead", "Instead", "indeed", "Indeed", "perhaps", "Perhaps", "maybe", "Maybe", 
        "certainly", "Certainly", "probably", "Probably", "actually", "Actually", "especially", "Especially", 
        "generally", "Generally", "usually", "Usually", "simply", "Simply", "finally", "Finally", "first", "First", 
        "second", "Second", "third", "Third", "last", "Last", "again", "Again", "once", "Once", "ever", "Ever", "never", 
        "Never", "already", "Already", "yet", "Yet", "today", "Today", "tomorrow", "Tomorrow", "yesterday", "Yesterday",

        "as", "As", "et", "Et", "al", "Al", "et al", "Et al", "via", "Via", "per", "Per",

        "according", "According", "based", "Based", "using", "Using", "used", "Used", "use", "Use", "shown", "Shown", "show", 
        "Show", "result", "Result", "results", "Results", "study", "Study", "studies", "Studies", "paper", "Paper", "papers", "Papers"
    ]

    # 以空格分割出句子中的單詞
    while True:
        found_space = False

        for i in range(len(str1)):
            if str1[i] == " ":
                words.append(str1[0:i])
                str1 = str1[i+1:]
                found_space = True
                break

        if found_space == False:
            if str1[-1] == ".":
                words.append(str1[:-1])
            else:
                words.append(str1)
            break
    
    # 將單詞放入 words = [] 
    for word in words:

        # 單詞尾巴接標點符號的話去掉
        word = word.replace(".", "").replace(",", "").replace("!", "").replace("?", "")

        if word in drop_words:
            continue

        if word in dict_words:
            dict_words[word] += 1
        else:
            dict_words[word] = 1

    return dict_words

# 中文文字處理
def count_words_chinese(str2):

    # 用 jieba 分割句子中的中文單詞
    words = [w for w in jieba.lcut(str2)]

    # 放要進文字雲的單詞
    dict_words = {}

    # 中文不用進文字雲的詞
    stopwords = [
        "的", "了", "著", "過", "呢", "嗎", "吧", "啊", "呀", "哦", "喔", "啦",
        "嘛", "罷了", "而已",

        "我", "你", "他", "她", "它", "我們", "你們", "他們", "她們", "它們",
        "自己", "人家", "大家", "彼此",

        "這", "那", "這個", "那個", "這些", "那些", "這樣", "那樣", "這邊", "那邊",
        "這裡", "那裡", "此", "其", "其中", "其實", "其他", "其它",
        "什麼", "為什麼", "怎麼", "怎樣", "如何", "哪裡", "哪個", "哪些", "多少",

        "在", "對", "把", "被", "從", "向", "往", "朝", "跟", "和", "與", "於",
        "比", "依", "依照", "按照", "根據", "透過", "藉由", "關於", "至於", "對於",
        "為", "為了", "以", "以便", "以免", "自", "自從", "沿著", "除", "除了",

        "和", "與", "及", "以及", "或", "或者", "還是", "而", "而且", "並", "並且",
        "但是", "但", "不過", "然而", "可是", "只是", "因為", "所以", "因此", "因而",
        "如果", "若", "假如", "假設", "雖然", "儘管", "即使", "並非", "不但", "不僅",
        "甚至", "此外", "另外", "再者", "同時", "然後", "接著", "最後", "於是",

        "很", "非常", "十分", "相當", "尤其", "特別", "更加", "更", "最", "太",
        "都", "也", "又", "再", "還", "仍", "仍然", "就", "才", "只", "只是",
        "已經", "曾經", "正在", "將", "將要", "會", "可能", "可以", "能", "不能",
        "應該", "必須", "需要", "值得", "容易", "不太", "比較", "較", "頗", "極", "挺",

        "是", "不是", "有", "沒有", "無", "並無", "成為", "變成", "算是",
        "做", "做出", "進行", "從事", "加以", "予以", "給予",
        "表示", "認為", "指出", "提到", "說", "說道", "說明", "強調", "覺得", "發現",
        "看見", "看到", "聽到", "聽見", "知道", "了解", "瞭解", "造成", "形成",
        "出現", "發生", "產生", "具有", "包含", "包括", "屬於", "涉及", "影響",
        "使用", "利用", "提供", "增加", "減少", "提升", "降低",

        "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
        "零", "百", "千", "萬", "億", "第一", "第二", "第三",
        "幾", "一些", "一點", "一種", "一個", "一切", "一起", "一直", "一般",
        "每", "每個", "各", "各個", "各種", "多", "很多", "不少", "少", "更多", "最少",

        "個", "種", "次", "些", "份", "位", "名", "項", "點", "類", "批", "組",
        "天", "日", "月", "年", "週", "星期", "小時", "分鐘", "秒",

        "上", "下", "前", "後", "左", "右", "裡", "外", "中", "內", "間",
        "之前", "之後", "以上", "以下", "以內", "以外", "當中",

        "今天", "昨天", "明天", "現在", "目前", "當時", "最近", "近日", "日前",
        "先前", "稍後", "早上", "上午", "中午", "下午", "晚上",

        "內容", "問題", "方面", "情況", "方式", "部分", "相關", "原因", "結果",
        "目標", "方法", "功能", "角色", "影響", "現象", "狀況", "資料", "資訊",
        "系統", "平台", "東西", "事情", "地方", "部分", "種類", "項目",

        "就是", "其實", "真的", "真的很", "有點", "那麼", "這麼", "比如", "例如",
        "像是", "例如說", "基本上", "原則上", "大概", "大致", "大約", "可能是",
        "算是", "等於", "之一", "之一個", "之類", "等等", "等", "某些", "某種",
        "然後", "因為", "所以", "如果", "但是", "覺得", "認為", "表示", "提到", 
        "說", "真的", "有點","這樣", "那樣", "這種", "那種", "東西", "事情", "部分",

        "欸", "嗯", "恩", "哈哈", "呵呵", "啦", "喔", "唉", "嗯嗯",

        "，", "。", "！", "？", "：", "；", "、", "（", "）", "(", ")", "[", "]",
        "{", "}", "「", "」", "『", "』", "《", "》", "〈", "〉", "—", "-", "_",
        "…", ".", ",", "!", "?", ":", ";", "/", "\\", "\"", "'", "“", "”",

        " ", "\n", "\t",

        "想", "用", "去", "來", "讓", "使", "令","要", "要去", "要用", "要做", "想要","能夠", "可以", "會", "會去", "會用",
        "試", "試著", "試圖","弄", "弄成", "搞", "搞成","拿", "帶", "帶來","給", "給出","當", "成", "變", "變得",
        "做", "做到", "做成", "做法","用來", "拿來","開始", "開始做", "開始用","繼續", "持續","停止", "停下","完成", "達成",
        "處理", "進行", "實行", "執行","操作", "運作","幫", "幫助", "協助","問", "回答", "回應","找", "找到", "尋找",
        "看", "看看", "看過","聽", "聽說","講", "談", "談到","寫", "寫出","讀", "讀到","學", "學會","教", "教會","帶", "帶動",
        "放", "放進", "放入","拉", "推","跑", "跑去","走", "走到","坐", "站","吃", "喝","玩","開", "打開", "關", "關掉",
        "按", "點", "點擊","選", "選擇","切", "切換","連", "連接","登", "登入", "登出","傳", "上傳", "下載","改", "修改", "更改",
        "建", "建立", "新增","刪", "刪除","存", "儲存","跑", "執行","叫", "稱為","算", "算出","當作", "視為","希望", "喜歡",
        "還要", "只要", "只會", "只想", "只需", "只是要","還", "還會", "還有", "還能", "還是","只", "只會", "只有", "只需", "只能",
        "要", "要是", "要不是", "要不然","就要", "想要", "需要", "必須", "得要","可以", "能夠", "能", "會", "不會",
        "先", "再", "又", "也", "都", "就", "才", "仍", "仍然","已經", "曾經", "正在", "將要","如果", "假如", "若", "雖然", "但是", 
        "可是", "然而","因為", "所以", "因此", "於是","而已", "而已啦", "而已啊","遇到", "碰到", "碰見", "見到", "看到", "看見", "發現",
        "聽到", "聽見", "想到", "感到", "覺得", "認為","提到", "說到", "談到", "講到","學到", "用到", "做到", "收到",

        "時候", "有時候", "那時候", "這時候","時間", "期間", "當時", "當下", "當初","過程", "途中", "階段", "開始", "最後", "後來"
    ]

    # 將單詞放入字典，並計算出現次數
    for word in words:
        if word in stopwords:
            continue
        if word in dict_words:
            dict_words[word] += 1
        else:
            dict_words[word] = 1

    return dict_words

# GUI
class App(tk.Tk):

    # 初始化GUI
    def __init__(self):
        super().__init__()
        self.title("創建文字雲")
        self.geometry("1000x650")

        # 可以選擇的主題色
        self.themes = {
            "綠色": ["#474A2C", "#636940", "#59A96A", "#9BDEAC", "#B4E7CE"],
            "紫色": ["#A393BF", "#9882AC", "#73648A", "#453750", "#564960"],
            "淺藍色": ["#5BD4D8", "#64E9EE", "#97C8EB", "#A0CDED", "#A9D2EF"],
            "深藍色": ["#9EB7E5","#81A2E5","#648DE5","#4A6DB7","#304C89"],
            "淺紅色": ["#CC444B", "#DA5552", "#DF7373", "#F7A58F", "#E4B1AB"],
            "深紅色": ["#220901","#621708","#941B0C","#BC3908","#F6AA1C"],
            "咖啡色": ["#202030","#978F79","#635C51","#7D7461","#B0A990"]
        }

        self.selected_theme = "綠色"
        self.wordcloud_obj = None

        self.show_home()
    
    # 清除 window
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    # Home 畫面介面
    def show_home(self):
        self.clear_window()

        # 標題
        title = tk.Label(self, text="創建文字雲", font=("Microsoft JhengHei", 50, "bold"))
        title.pack(pady=60)

        # 英文文字雲按鈕
        btn = tk.Button(
            self,
            text="英文文字雲建立",
            font=("Microsoft JhengHei", 20),
            command=self.show_create_page
        )
        btn.pack(pady=20)

        # 中文文字雲按鈕
        btn2 = tk.Button(
            self,
            text="中文文字雲建立",
            font=("Microsoft JhengHei", 20),
            command=self.show_create_page_chinese
        )
        btn2.pack(pady=20)
    
    # 選顏色
    def show_palette(self, theme_name):
        for widget in self.palette_frame.winfo_children():
            widget.destroy()

        for color in self.themes[theme_name]:
            tk.Label(
                self.palette_frame,
                bg=color,
                width=4,
                height=2,
                relief="solid",
                bd=1
            ).pack(side="left", padx=4)
    
    # 試看顏色
    def update_theme_preview(self, selected=None):
        if selected is None:
            selected = self.theme_var.get()

        self.selected_theme = selected
        self.theme_name_label.config(text=f"目前主題：{self.selected_theme}")
        self.show_palette(self.selected_theme)

    # 英文文字雲介面
    def show_create_page(self):
        self.clear_window()

        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", pady=10)

        # 回首頁
        back_btn = tk.Button(top_frame, text="回首頁", command=self.show_home)
        back_btn.pack(side="left", padx=10)

        tk.Label(
            top_frame,
            text="英文文字雲",
            font=("Microsoft JhengHei", 18, "bold")
        ).pack(side="left", padx=10)

        left_frame = tk.Frame(self)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # 選要多少單詞在文字雲中
        tk.Label(left_frame, text="顯示字數").pack(anchor="w")
        self.max_words_var = tk.IntVar(value=10)
        tk.Spinbox(
            left_frame,
            from_=10,
            to=300,
            increment=10,
            textvariable=self.max_words_var
        ).pack(anchor="w", pady=5)

        # 選主題色
        tk.Label(left_frame, text="選擇主題色").pack(anchor="w")
        self.theme_var = tk.StringVar(value=self.selected_theme)

        tk.OptionMenu(
            left_frame,
            self.theme_var,
            *self.themes.keys(),
            command=self.update_theme_preview
        ).pack(anchor="w", pady=5)

        self.theme_name_label = tk.Label(left_frame, text=f"目前主題：{self.selected_theme}")
        self.theme_name_label.pack(anchor="w")

        self.palette_frame = tk.Frame(left_frame)
        self.palette_frame.pack(anchor="w", pady=(5, 10))
        self.show_palette(self.selected_theme)

        # 讀.text
        tk.Button(left_frame, text="讀入 .txt 檔", command=self.load_txt).pack(anchor="w", pady=5)

        # 輸入文字
        tk.Label(left_frame, text="輸入文字").pack(anchor="w", pady=(10, 0))
        self.text_input = tk.Text(left_frame, width=45, height=20)
        self.text_input.pack(fill="both", expand=True)

        button_frame = tk.Frame(left_frame)
        button_frame.pack(pady=20)

        # 按下按鈕產生文字雲
        generate_btn = tk.Button(
            button_frame,
            text="產生文字雲",
            font=("Microsoft JhengHei", 10, "bold"),
            width=12,
            height=10,
            command=lambda: self.generate_wordcloud(right_frame)
        )
        generate_btn.pack(side="left", padx=10)


        # 按下按鈕存成.png
        save_btn = tk.Button(
            button_frame,
            text="存成圖片",
            font=("Microsoft JhengHei", 10, "bold"),
            width=12,
            height=10,
            command=self.save_image
        )
        save_btn.pack(side="left", padx=10)

        # 文字雲預覽
        self.preview_frame = right_frame
        tk.Label(right_frame, text="這裡會顯示文字雲", font=("Microsoft JhengHei", 14)).pack(expand=True)
    
    # 中文文字雲介面
    def show_create_page_chinese(self):
        self.clear_window()

        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", pady=10)

        back_btn = tk.Button(top_frame, text="回首頁", command=self.show_home)
        back_btn.pack(side="left", padx=10)

        tk.Label(
            top_frame,
            text="中文文字雲",
            font=("Microsoft JhengHei", 18, "bold")
        ).pack(side="left", padx=10)

        left_frame = tk.Frame(self)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # 選要多少單詞在文字雲中
        tk.Label(left_frame, text="顯示字數").pack(anchor="w")
        self.max_words_var = tk.IntVar(value=10)
        tk.Spinbox(
            left_frame,
            from_=10,
            to=300,
            increment=10,
            textvariable=self.max_words_var
        ).pack(anchor="w", pady=5)

        # 選主題色
        tk.Label(left_frame, text="選擇主題色").pack(anchor="w")
        self.theme_var = tk.StringVar(value=self.selected_theme)

        tk.OptionMenu(
            left_frame,
            self.theme_var,
            *self.themes.keys(),
            command=self.update_theme_preview
        ).pack(anchor="w", pady=5)

        self.theme_name_label = tk.Label(left_frame, text=f"目前主題：{self.selected_theme}")
        self.theme_name_label.pack(anchor="w")

        self.palette_frame = tk.Frame(left_frame)
        self.palette_frame.pack(anchor="w", pady=(5, 10))
        self.show_palette(self.selected_theme)

        # 讀.text
        tk.Button(left_frame, text="讀入 .txt 檔", command=self.load_txt).pack(anchor="w", pady=5)

        # 輸入文字
        tk.Label(left_frame, text="輸入文字").pack(anchor="w", pady=(10, 0))
        self.text_input = tk.Text(left_frame, width=45, height=20)
        self.text_input.pack(fill="both", expand=True)

        button_frame = tk.Frame(left_frame)
        button_frame.pack(pady=20)

        # 按下按鈕產生文字雲
        generate_btn = tk.Button(
            button_frame,
            text="產生文字雲",
            font=("Microsoft JhengHei", 10, "bold"),
            width=12,
            height=10,
            command=lambda: self.generate_wordcloud_chinese(right_frame)
        )
        generate_btn.pack(side="left", padx=10)


        # 按下按鈕存成.png
        save_btn = tk.Button(
            button_frame,
            text="存成圖片",
            font=("Microsoft JhengHei", 10, "bold"),
            width=12,
            height=10,
            command=self.save_image
        )
        save_btn.pack(side="left", padx=10)

        # 文字雲預覽
        self.preview_frame = right_frame
        tk.Label(right_frame, text="這裡會顯示文字雲", font=("Microsoft JhengHei", 14)).pack(expand=True)

    # 載入 .text
    def load_txt(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            with open(file_path, "r", encoding="cp950") as f:
                content = f.read()

        self.text_input.delete("1.0", tk.END)
        self.text_input.insert(tk.END, content)

    # 英文文字雲生產
    def generate_wordcloud(self, frame):
        text = self.text_input.get("1.0", tk.END).strip()
        
        # 各種以防萬一出錯
        if not text:
            messagebox.showwarning("提醒", "請先輸入文字或讀入 .txt 檔")
            return
        
        # 避免中文存在
        if re.search(r'[\u4e00-\u9fff]', text):
            messagebox.showerror("提醒", "請全部輸入英文")
            return

        word_freq = count_words(text)

        if not word_freq:
            messagebox.showwarning("提醒", "沒有可用的字詞")
            return

        theme_palette = self.themes[self.theme_var.get()]
        self.selected_theme = self.theme_var.get()

        self.wordcloud_obj = WordCloud(
            width=800,
            height=400,
            background_color="white",
            max_words=self.max_words_var.get(),
            color_func=lambda *args, **kwargs: random.choice(theme_palette),
            collocations=False
        ).generate_from_frequencies(word_freq)

        for widget in frame.winfo_children():
            widget.destroy()

        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.imshow(self.wordcloud_obj, interpolation="bilinear")
        ax.axis("off")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # 中文文字雲產生
    def generate_wordcloud_chinese(self, frame):
        text = self.text_input.get("1.0", tk.END).strip()
        
        # 各種以防萬一出錯
        if not text:
            messagebox.showwarning("提醒", "請先輸入文字或讀入 .txt 檔")
            return
        
        # 不要全是英文
        if re.fullmatch(r"[A-Za-z0-9\s.,!?'\"]+", text):
            messagebox.showerror("提醒", "請不要全部輸入英文")
            return

        word_freq = count_words_chinese(text)

        if not word_freq:
            messagebox.showwarning("提醒", "沒有可用的字詞")
            return

        theme_palette = self.themes[self.theme_var.get()]
        self.selected_theme = self.theme_var.get()

        self.wordcloud_obj = WordCloud(
            width=800,
            height=400,
            font_path = "C:/Windows/Fonts/msjh.ttc",   # 中文字型
            background_color="white",
            max_words=self.max_words_var.get(),
            color_func=lambda *args, **kwargs: random.choice(theme_palette),
            collocations=False
        ).generate_from_frequencies(word_freq)

        for widget in frame.winfo_children():
            widget.destroy()

        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.imshow(self.wordcloud_obj, interpolation="bilinear")
        ax.axis("off")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # 存圖片
    def save_image(self):
        if self.wordcloud_obj is None:
            messagebox.showwarning("提醒", "請先產生文字雲")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )
        if file_path:
            self.wordcloud_obj.to_file(file_path)
            messagebox.showinfo("完成", "圖片已儲存")


app = App()
app.mainloop()

# python "HW2_wordcloud.py"