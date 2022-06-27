import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkwidgets import CheckboxTreeview
import re
import requests
from bs4 import BeautifulSoup
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('550x400')
        self.title('تحميل صور')
        tkvar = dict()
        def download():
            links = plst.get()
            dir = dirr.get()

            response = requests.get(links)
            children = tree.get_children()
            soup = BeautifulSoup(response.text, 'html.parser')
            image_tags = soup.find_all('img')
            urls = [img['src'] for img in image_tags]
            count = 0
            cunt=0
            for child in children:
                tkvar[cunt]=child
                cunt+=1
            for url in urls:
                filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
                if not filename:
                    continue
                full_path = os.path.join(dir, filename.group(1))
                with open(full_path, 'wb') as f:
                    if str(tree.item(tkvar[count], 'tags')) == "('checked',)":
                        if 'http' not in url:
                            url = '{}{}'.format(links, url)
                        response = requests.get(url)
                        f.write(response.content)
                        count+=1
            messagebox.showinfo('',f'تم تحميل'
                                   f'{count} صور بنجاح')
        def search():
            links = plst.get()
            response = requests.get(links)
            soup = BeautifulSoup(response.text, 'html.parser')
            image_tags = soup.find_all('img')
            urls = [img['src'] for img in image_tags]
            count = 0
            for url in urls:
                filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
                if not filename:
                    continue
                if 'http' not in url:
                    url = '{}{}'.format(links, url)
                response = requests.get(url)
                title = response.url.split('/')
                tree.insert('', count, values={title[-1]})
                count += 1
        frame=tk.LabelFrame(self, text='', padx=10, pady=10)
        frame.grid(pady=10, padx=10)
        frame2=tk.LabelFrame(self, text='', padx=10, pady=10)
        frame2.grid(column=0,pady=10, padx=10,sticky=tk.W)
        plst = ttk.Entry(frame,width=50)
        plst.grid(row=0, padx=20 , pady=5)
        dirr = ttk.Entry(frame,width=50)
        dirr.grid(row=1, padx=20, pady=5)
        ttk.Button(frame,
                   text='بحث', width=20,
                   command=lambda: (search())).grid(row=0, column=1, padx=20, pady=5)
        ttk.Button(frame,
                   text='تحميل', width=20,
                   command=lambda: (download())).grid(row=1, column=1, padx=20, pady=5)
        tree=CheckboxTreeview(frame2,columns='IMG')
        tree.heading('IMG',text='Images')
        tree.column("#0", width=50)
        tree.column("#1", width=300)
        tree.grid(row=0,column=0,sticky=tk.W)
App().mainloop()