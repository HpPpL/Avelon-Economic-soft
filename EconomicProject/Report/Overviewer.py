from ExcelOverview import ExcelRecorder
from WordOverview import WordRecorder
import os
import time

if __name__ == "__main__":
    t = time.time()
    # Отберем файлы, название которых начинается на Report
    LOF = [file for file in os.listdir("../Examples") if file[:6] == "Report"]
    # После чего скорректируем путь до нужной папки:
    LOF = list(map(lambda x: "../Examples/" + x, LOF))

    # Переходим к обработке
    for file in LOF[:]:
        word_path = f'Results/Overview_{file.split("_")[1]}'
        ExcelRecorder(file).record()
        WordRecorder(word_path).record()

    print(f"\nОбработка {len(LOF)} файлов заняла {round(time.time() - t, 2)} с.")
