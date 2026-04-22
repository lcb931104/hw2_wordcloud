import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

def count_words(str1):

    dict_words = {}
    words = []

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

        "not", "Not", "no", "No", "nor", "Nor", "yes", "Yes"
    ]

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

    for word in words:
        word = word.replace(".", "").replace(",", "").replace("!", "").replace("?", "")

        if word in drop_words:
            continue

        if word in dict_words:
            dict_words[word] += 1
        else:
            dict_words[word] = 1

    return dict_words


# GUI
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("創建文字雲")
        self.geometry("1000x650")

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

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_window()

        title = tk.Label(self, text="創建文字雲", font=("Microsoft JhengHei", 50, "bold"))
        title.pack(pady=60)

        btn = tk.Button(
            self,
            text="英文文字雲建立",
            font=("Microsoft JhengHei", 20),
            command=self.show_create_page
        )
        btn.pack(pady=20)

    def show_home(self):
        self.clear_window()

        title = tk.Label(self, text="創建文字雲", font=("Microsoft JhengHei", 50, "bold"))
        title.pack(pady=60)

        btn = tk.Button(self, text="英文文字雲建立", font=("Microsoft JhengHei", 20), command=self.show_create_page)
        btn.pack(pady=20)

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

    def update_theme_preview(self, selected=None):
        if selected is None:
            selected = self.theme_var.get()

        self.selected_theme = selected
        self.theme_name_label.config(text=f"目前主題：{self.selected_theme}")
        self.show_palette(self.selected_theme)

    def show_create_page(self):
        self.clear_window()

        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", pady=10)

        back_btn = tk.Button(top_frame, text="回首頁", command=self.show_home)
        back_btn.pack(side="left", padx=10)

        tk.Label(
            top_frame,
            text="創建文字雲",
            font=("Microsoft JhengHei", 18, "bold")
        ).pack(side="left", padx=10)

        left_frame = tk.Frame(self)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(left_frame, text="顯示字數").pack(anchor="w")
        self.max_words_var = tk.IntVar(value=10)
        tk.Spinbox(
            left_frame,
            from_=10,
            to=300,
            increment=10,
            textvariable=self.max_words_var
        ).pack(anchor="w", pady=5)

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

        tk.Button(left_frame, text="讀入 .txt 檔", command=self.load_txt).pack(anchor="w", pady=5)

        tk.Label(left_frame, text="輸入文字").pack(anchor="w", pady=(10, 0))
        self.text_input = tk.Text(left_frame, width=45, height=20)
        self.text_input.pack(fill="both", expand=True)

        button_frame = tk.Frame(left_frame)
        button_frame.pack(pady=20)

        generate_btn = tk.Button(
            button_frame,
            text="產生文字雲",
            font=("Microsoft JhengHei", 10, "bold"),
            width=12,
            height=10,
            command=lambda: self.generate_wordcloud(right_frame)
        )
        generate_btn.pack(side="left", padx=10)

        save_btn = tk.Button(
            button_frame,
            text="存成圖片",
            font=("Microsoft JhengHei", 10, "bold"),
            width=12,
            height=10,
            command=self.save_image
        )
        save_btn.pack(side="left", padx=10)

        self.preview_frame = right_frame
        tk.Label(right_frame, text="這裡會顯示文字雲", font=("Microsoft JhengHei", 14)).pack(expand=True)

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

    def generate_wordcloud(self, frame):
        text = self.text_input.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning("提醒", "請先輸入文字或讀入 .txt 檔")
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