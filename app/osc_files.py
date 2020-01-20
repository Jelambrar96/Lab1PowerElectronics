
import os
from abc import ABC

import csv

import numpy as np


def _read_csv(filename):
    v = []
    tv = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(csv_reader):
            if i < 18:
                continue
            v.append(float(row[4]))
            tv.append(float(row[3]))
    return np.array(tv), np.array(v)


def _read_txt(filename):
    v = []
    tv = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            v.append(float(row[1]))
            tv.append(float(row[0]))
    return np.array(tv), np.array(v)

#
#
#
#
#
#
class BasicReader(ABC):

    def __init__(self, filenameVoltage, filenameCurrent):
        pass

    def calcData(self):
        pass

    def getData(self):
        pass

#
#
#
#
#
#
class TXTReader(BasicReader):

    def __init__(self, filenameVoltage, filenameCurrent):
        if not os.path.isfile(filenameVoltage):
            raise Exception("ERROR: File \"%s\" does not exist!".format(filenameVoltage))
        self._file_voltage = filenameVoltage
        if not os.path.isfile(filenameCurrent):
            raise Exception("ERROR: File \"%s\" does not exist!".format(filenameCurrent))
        self._file_current = filenameCurrent
        self._t = None
        self._v = None
        self._i = None

    def calcData(self):
        tv, v = _read_txt(self._file_voltage)
        ti, i = _read_txt(self._file_current)
        if not np.array_equal(ti, tv):
            raise Exception("ERROR: Time vectors are not equals.")
        # return t, v, i
        self._t = tv
        self._i = i
        self._v = v

    def getData(self):
        return self._t, self._v, self._i 

#
#
#
#
#
#
class CSVReader(BasicReader):

    def __init__(self, filenameVoltage, filenameCurrent):
        if not os.path.isfile(filenameVoltage):
            raise Exception("ERROR: File \"%s\" does not exist!".format(filenameVoltage))
        if not os.path.isfile(filenameCurrent):
            raise Exception("ERROR: File \"%s\" does not exist!".format(filenameCurrent))
        self._file_current = filenameCurrent
        self._file_voltage = filenameVoltage
        self._t = None
        self._v = None
        self._i = None

    def calcData(self):
        tv, v = _read_csv(self._file_voltage)
        ti, i = _read_csv(self._file_current)
        if not np.array_equal(ti, tv):
            raise Exception("ERROR: Time vectors are not equals.")
        # return t, v, i
        self._t = tv
        self._i = i
        self._v = v

    def getData(self):
        return self._t, self._v, self._i 




