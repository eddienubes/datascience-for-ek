# ----------------------------- Decision Support System (DSS) -------------------------------------

'''

Завдання:
   сформувати обгрунтоване рішення щодо впровадження нового товару на ринок з множини альтернатив
   за багатокритеріальною / багатофакторною оптимізаційною моделлю для Decision Support System: ERP,CRM систем.

Склад етапів:
1. Формалізація задачі як багатофакторної / багатокритеріальної;
2. Формування сегменту даних та парсінг *.xls файлу;
3. Нормалізація даних;
4. Розрахунок інтегрованої оцінки - scor - оцінювання альтернатив - scoring;
   спосіб розрахунку інтегрованої оцінки - нелінійна схема компромісів
   http://sci-gems.math.bas.bg/jspui/bitstream/10525/49/1/ijita15-2-p02.pdf
5. Обрання найкращіх альтернатив.

Альтернативні галузі:
   Теорія операцій - розподіл ресурсів;
   Теорія розкладів
   Інструментарій оптимізації: Google OR-Tools;
   https://developers.google.com/optimization/examples?hl=en

'''

import pandas as pd
import numpy as np


def file_parsing(Data_name, sample_data):
    for name, values in sample_data[[Data_name]].items():
        values
    n_sample_data = int(len(values))
    S_real = np.zeros((n_sample_data))
    for i in range(n_sample_data):
        S_real[i] = values[i].replace(',', '.')
    return S_real


def matrix_generation(File_name):
    sample_data = pd.read_excel(File_name)
    print(sample_data)
    line_sample_data = int(sample_data.shape[0])
    column_sample_data = int(sample_data.shape[1])
    line_column_matrix = np.zeros(((line_sample_data), (column_sample_data - 2)))
    Title_sample_data = sample_data.columns
    for i in range(1, (column_sample_data - 1), 1):
        column_matrix = file_parsing(Title_sample_data[i], sample_data)
        for j in range(len(column_matrix)):
            line_column_matrix[j, (i - 1)] = column_matrix[j]
    return line_column_matrix


def matrix_adapter(line_column_matrix, line):
    column_sample_matrix = np.shape(line_column_matrix)
    line_matrix = np.zeros((column_sample_matrix[1]))
    for j in range(column_sample_matrix[1]):
        line_matrix[j] = line_column_matrix[line, j]
    return line_matrix


def Voronin(File_name, G1, G2, G3, G4, G5, G6, G7, G8, G9):
    # --------------------- вхідні дані -------------------------
    line_column_matrix = matrix_generation(File_name)
    column_matrix = np.shape(line_column_matrix)
    Integro = np.zeros((column_matrix[1]))

    F1 = matrix_adapter(line_column_matrix, 0)
    F2 = matrix_adapter(line_column_matrix, 1)
    F3 = matrix_adapter(line_column_matrix, 2)
    F4 = matrix_adapter(line_column_matrix, 3)
    F5 = matrix_adapter(line_column_matrix, 4)
    F6 = matrix_adapter(line_column_matrix, 5)
    F7 = matrix_adapter(line_column_matrix, 6)
    F8 = matrix_adapter(line_column_matrix, 7)
    F9 = matrix_adapter(line_column_matrix, 8)

    # --------------- нормалізація вхідних даних ------------------
    F10 = np.zeros((column_matrix[1]))
    F20 = np.zeros((column_matrix[1]))
    F30 = np.zeros((column_matrix[1]))
    F40 = np.zeros((column_matrix[1]))
    F50 = np.zeros((column_matrix[1]))
    F60 = np.zeros((column_matrix[1]))
    F70 = np.zeros((column_matrix[1]))
    F80 = np.zeros((column_matrix[1]))
    F90 = np.zeros((column_matrix[1]))

    GNorm = G1 + G2 + G3 + G4 + G5 + G6 + G6 + G7 + G8 + G9
    G10 = G1 / GNorm
    G20 = G2 / GNorm
    G30 = G3 / GNorm
    G40 = G4 / GNorm
    G50 = G5 / GNorm
    G60 = G6 / GNorm
    G70 = G7 / GNorm
    G80 = G8 / GNorm
    G90 = G9 / GNorm

    sum_F1 = sum_F2 = sum_F3 = sum_F4 = sum_F5 = sum_F6 = sum_F7 = sum_F8 = sum_F9 = 0

    for i in range(column_matrix[1]):
        sum_F1 = sum_F1 + F1[i]
        sum_F2 = sum_F2 + F2[i]
        sum_F3 = sum_F3 + F3[i]
        sum_F4 = sum_F4 + F4[i]
        sum_F5 = sum_F5 + F5[i]
        sum_F6 = sum_F6 + (1 / F6[i])  # максимізований критерії
        sum_F7 = sum_F7 + F7[i]
        sum_F8 = sum_F8 + F8[i]
        sum_F9 = sum_F9 + F9[i]

    for i in range(column_matrix[1]):
        # --------------- нормалізація критеріїв ------------------
        F10[i] = F1[i] / sum_F1
        F20[i] = F2[i] / sum_F2
        F30[i] = F3[i] / sum_F3
        F40[i] = F4[i] / sum_F4
        F50[i] = F5[i] / sum_F5
        F60[i] = (1 / F6[i]) / sum_F6  # максимізований критерії
        F70[i] = F7[i] / sum_F7
        F80[i] = F8[i] / sum_F8
        F90[i] = F9[i] / sum_F9

        Integro[i] = (G10 * (1 - F10[i]) ** (-1)) + (G20 * (1 - F20[i]) ** (-1)) + (G30 * (1 - F30[i]) ** (-1))
        + (G40 * (1 - F40[i]) ** (-1)) + (G50 * (1 - F50[i]) ** (-1)) + (G60 * (1 - F60[i]) ** (-1))
        + (G70 * (1 - F70[i]) ** (-1)) + (G80 * (1 - F80[i]) ** (-1)) + (G90 * (1 - F90[i]) ** (-1))

    # --------------- генерація оптимального рішення ----------------
    min = 10000
    opt = 0
    for i in range(column_matrix[1]):
        if min > Integro[i]:
            min = Integro[i]
            opt = i
    print('Інтегрована оцінка (scor):')
    print(Integro)
    print('Номер_оптимального_товару:', opt)

    return


# -------------------------------- БЛОК ГОЛОВНИХ ВИКЛИКІВ ------------------------------
if __name__ == '__main__':
    File_name = 'Pr1.xls'

    # ---------------- коефіціенти переваги критеріїв -----------------
    G1 = G2 = G3 = G4 = G5 = G6 = G7 = G8 = G9 = 1
    G1 = 1  # коефіціент домінування критерію

    Voronin(File_name, G1, G2, G3, G4, G5, G6, G7, G8, G9)
