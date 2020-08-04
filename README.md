# VesReader
Useful script to work with lot of VES.ipd or .dat files (for ММПГ-1 magnetometer only)

1. Для пользования скриптом VesReader на компьютере должен быть установлен язык Python версии не ниже 3.8

2. Откройте файл VesReader.py с помощью IDLE (правая кнопка мыши и пункт Edit with IDLE, если в меню 2 таких пункта, выберите Edit with IDLE 3.8 (32-bit))

3. Одна из верхних строк файла будет иметь такой вид:
folder = r'D:\2019\Исходники'
это имя папки, в которой лежат ваши исходники ВЭЗ в dat или ipd формате.
Измените имя папки на нужную вам, отделяя названия подпапок с помощью \
например:
folder = r'D:\2020\Малмыж\Исходники\Главный корпус'
ничего больше не меняйте
Сохраните файл с помощью File -> Save или сочетания Ctrl + S

4. Запустите VesReader.py из IDLE с помощью Run -> Run Module или клавиши F5.
Откроется окно Python Shell, где и будет выполняться программа.
В пункт "Файл исходников: " вводите название файла с исходниками ВЭЗ вместе с расширением. Например вэз_01.dat или вэз45.ipd (можно вводить имена с помощью Ctrl + C, Ctrl + V, выделив имя файла с помощью пункта "Переименовать" или клавиши F2)
Осторожно!: Если нажать Ctrl + C в окне Python Shell это прервёт выполнение программы. Ничего страшного, просто нужно будет снова запустить VesReader c помощью F5

5. Будут создаваться текстовые файлы с именами файлов исходников вида вэз 01_output.txt или вэз45_output.txt в папке с исходниками. Оттуда уже можно копировать информацию в Excel

6. Когда закончите, введите exit вместо имени файла, чтобы выйти из программы.