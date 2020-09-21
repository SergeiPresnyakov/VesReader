from math import pi
import os
import tkinter as tk
from tkinter import filedialog as fd


class VesReader:
    def __init__(self):
        self.read_list = []
        self.content = []

    def read(self, name):
        # read and choose useful data
        with open(name) as file:
            self.read_list = file.readlines()
            self.read_list = [row.strip().split() for row in self.read_list][4:]
            self.content = [
                {
                    'pka': i[2],
                    'pkb': i[4],
                    'pkm': i[6],
                    'pkn': i[7],
                    'ares': i[9],
                    'chr': i[10],
                    'voltage': i[8]
                }
                for i in self.read_list
            ]

            # str -> float
            for _dict in self.content:
                for key in _dict:
                    _dict[key] = float(_dict[key])
            
            # sort
            self.content = sorted(self.content, key=lambda x: (max(x['pka'], x['pkb']), max(x['pkm'], x['pkn'])))

    # calculate setup coefficient (standard 4-electrodes)
    def calc_K(self):
        for _dict in self.content:
            am = _dict['pka'] - _dict['pkm']
            bm = _dict['pka'] + _dict['pkm']
            an = bm
            bn = am
            K = round((2 * pi) / abs(1/am - 1/bm - 1/an + 1/bn), 2)
            _dict['K'] = K

    def write_to_file(self, name, ves_no):
        # prepare and format
        for _dict in self.content:
            for key in _dict:
                _dict[key] = str(_dict[key])

                # PK number must be integer 
                if key in {'pka', 'pkb', 'pkm', 'pkn'} and _dict[key].endswith('.0'):
                    _dict[key] = _dict[key][:-2]

        # write to file
        with open(name, 'a') as output:
            output.write(ves_no + '\n')
            output.write('AB/2, м;MN/2, м;K;Uпр, мВ;I, мА;Res, Ом.м;ВП, %;Voltage\n')
            for row in self.content:
                a = max(row['pka'], row['pkb'])
                b = max(row['pkm'], row['pkn'])
                output.write(f"{a};{b};{row['K']};;;{row['ares']};{row['chr']};{row['voltage']}\n")
            output.write('\n\n')

    def __str__(self):
        for el in self.content:
            print(el)
        return ''


class Window:
    def __init__(self, parent):
        parent.title('Закинуть все ВЭЗы в базу')
        parent.geometry('900x300')
        parent.resizable(False, False)
        parent.config(bg='#D5F5E3')
        self.foldername = ''

        self.open_folder_button = tk.Button(parent, text='Папка с исходниками', command=self.get_foldername, bg='#67CE95', fg='black', font="Verdana 20", relief=tk.FLAT)
        self.process_button = tk.Button(parent, text='Создать базу ВЭЗ', command=self.create_databaze, bg='#67CE95', fg='black', font="Verdana 20", relief=tk.FLAT)
        self.foldername_label = tk.Label(parent, width=80, font="Verdana 16", bg='#C1F7D9', fg='black')
        self.result_label = tk.Label(parent, width=30, font="Verdana 30", bg='#C1F7D9', fg='black')

        self.open_folder_button.place(relx=0.5, rely=0.15, anchor='center')
        self.foldername_label.place(relx=0.5, rely=0.35, anchor='center')
        self.process_button.place(relx=0.5, rely=0.55, anchor='center')
        self.result_label.place(relx=0.5, rely=0.8, anchor='center')

        self.open_folder_button.bind('<Enter>', self.set_color)
        self.open_folder_button.bind('<Leave>', self.restore_color)
        self.process_button.bind('<Enter>', self.set_color)
        self.process_button.bind('<Leave>', self.restore_color)
    
    def set_color(self, event):
        event.widget.config(bg="#8EE6B5", activebackground='#68D598')
    
    def restore_color(self, event):
        event.widget.config(bg='#67CE95', fg='black')

    def get_foldername(self):
        self.foldername = fd.askdirectory()
        self.foldername_label.config(text=self.foldername)
        self.result_label.config(text='')
    
    def create_databaze(self):
        if self.foldername:
            files = os.listdir(self.foldername)
            files = [file for file in files if file.endswith('.ipd') or file.endswith('.dat')]

            for file in files:
                ves = VesReader()
                ves.read(f'{self.foldername}\\{file}')
                ves.calc_K()
                ves.write_to_file(f'{self.foldername}\\Databaze.csv', file)
            self.result_label.config(text='Все файлы в папке обработаны')
        else:
            self.result_label.config(text='Сначала выберите папку')


def main():
    root = tk.Tk()
    Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
