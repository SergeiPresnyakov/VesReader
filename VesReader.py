﻿from math import pi
import os


# полное имя папки, в которой лежат исходники .ipd или .dat
# кроме этой строки больше ничего не меняйте
folder = r'D:\2020\Малмыж\Исходники\Главный корпус\Главный корпус рядовые (IPD)'


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


def main():
    files = os.listdir(folder)
    files = [file for file in files if file.endswith('.ipd') or file.endswith('.dat')]

    for file in files:
        ves = VesReader()
        ves.read(f'{folder}\\{file}')
        ves.calc_K()
        ves.write_to_file(f'{folder}\\Databaze.csv', file)
    print('Все файлы в папке обработаны')


if __name__ == '__main__':
    main()
