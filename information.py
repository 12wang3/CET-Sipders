# -*- coding: utf-8 -*-
__author__ = '12wang3'

import xlrd
import numpy as np
import matplotlib.pyplot as plt

stuType = np.dtype([
    ('no', 'U5'),
    ('cet', 'U10'),
    ('schoolZone', 'U10'),
    ('room', 'U10'),
    ('seat', 'U10'),
    ('examNum', 'U50'),
    ('name', 'U50'),
    ('sex', 'U50'),
    ('papers', 'U50'),
    ('department', 'U50'),
    ('grade', 'U10'),
    ('class', 'U50'),
    ('stuID', 'U50'),
    ('baoNum', 'U50'),
    ('location', 'U50'),
])

sheetData = xlrd.open_workbook('C:\\Users\\12wang3\\Desktop\\s.xls')
sheet = sheetData.sheet_by_index(1)
stu = np.empty(sheet.nrows, dtype=stuType)
stuScore = np.empty((sheet.nrows,4),dtype = 'int32')
for i in range(sheet.nrows):
    stu[i] = np.array(tuple(sheet.row_values(i)), dtype=stuType)

