# -*- coding: utf-8 -*-
"""
    @Copyright (c) 2023 by frostime. All Rights Reserved.
    @Author       : Wang YaoDong
    @Date         : 2023-12-27 21:39:42
    @FilePath     : /zyplib/feature/wyd.py
    @LastEditTime : 2023-12-27 21:43:54
    @Description  : 来自王博的特征提取代码
"""
import csv
from os import listdir
from os.path import isfile, join

import numpy as np
import pyedflib
import pywt
import scipy.stats as sp
from matplotlib import pyplot as plt
from nitime import algorithms as alg
from nitime import utils
from nitime.timeseries import TimeSeries
from nitime.viz import plot_tseries
from spectrum import *

names = [
    'Activity', 'Mobility', 'Complexity', 'Kurtosis', '2nd Difference Mean',
    '2nd Difference Max', 'Coeffiecient of Variation', 'Skewness', '1st Difference Mean',
    '1st Difference Max', 'Wavelet Approximate Mean', 'Wavelet Approximate Std Deviation',
    'Wavelet Detailed Mean', 'Wavelet Detailed Std Deviation',
    'Wavelet Approximate Energy', 'Wavelet Detailed Energy',
    'Wavelet Approximate Entropy', 'Wavelet Detailed Entropy', 'Variance',
    'Mean of Vertex to Vertex Slope', 'FFT Delta MaxPower', 'FFT Theta MaxPower',
    'FFT Alpha MaxPower', 'FFT Beta MaxPower',
    'Autro Regressive Mode Order 3 Coefficients for each channel ->'
]


def hjorth(input):  # function for hjorth
    realinput = input
    hjorth_activity = np.zeros(len(realinput))
    hjorth_mobility = np.zeros(len(realinput))
    hjorth_diffmobility = np.zeros(len(realinput))
    hjorth_complexity = np.zeros(len(realinput))
    diff_input = np.diff(realinput)
    diff_diffinput = np.diff(diff_input)
    k = 0
    for j in realinput:
        hjorth_activity[k] = np.var(j)
        hjorth_mobility[k] = np.sqrt(np.var(diff_input[k]) / hjorth_activity[k])
        hjorth_diffmobility[k] = np.sqrt(
            np.var(diff_diffinput[k]) / np.var(diff_input[k])
        )
        hjorth_complexity[k] = hjorth_diffmobility[k] / hjorth_mobility[k]
        k = k + 1
    return np.sum(hjorth_activity) / 14, np.sum(hjorth_mobility) / 14, np.sum(
        hjorth_complexity
    ) / 14  #returning hjorth activity, hjorth mobility , hjorth complexity


def my_kurtosis(a):
    b = a  # Extracting the data from the 14 channels
    output = np.zeros(len(b))  # Initializing the output array with zeros (length = 14)
    k = 0
    # For counting the current row no.
    for i in b:
        mean_i = np.mean(i)  # Saving the mean of array i
        std_i = np.std(i)  # Saving the standard deviation of array i
        t = 0.0
        for j in i:
            t += (pow((j - mean_i) / std_i, 4) - 3)
        kurtosis_i = t / len(
            i
        )  # Formula: (1/N)*(summation(x_i-mean)/standard_deviation)^4-3
        output[k] = kurtosis_i  # Saving the kurtosis in the array created
        k += 1  # Updating the current row no.
    return np.sum(output) / 14


##----------------------------------------- End Kurtosis Function ----------------------------##

##------------------------------------- Begin 2ndDiffMean(Absolute difference) Function ------##
##-------------------------- [ Input: 2D array (row: Channels, column: Data)] --------------- ##
##-------------------  -- [ Output: 1D array (2ndDiffMean values for each channel)] ----------##


def secDiffMean(a):
    b = a  # Extracting the data of the 14 channels
    output = np.zeros(len(b))  # Initializing the output array with zeros (length = 14)
    temp1 = np.zeros(len(b[0]) - 1)  # To store the 1st Diffs
    k = 0
    # For counting the current row no.
    for i in b:
        t = 0.0
        for j in range(len(i) - 1):
            temp1[j] = abs(i[j + 1] - i[j])  # Obtaining the 1st Diffs
        for j in range(len(i) - 2):
            t += abs(temp1[j + 1] - temp1[j])  # Summing the 2nd Diffs
        output[k] = t / (len(i) - 2)  # Calculating the mean of the 2nd Diffs
        k += 1  # Updating the current row no.
    return np.sum(output) / 14


##------------------------------------- End 2ndDiffMean Function----- -------------------------##

##------------------------------------- Begin 2ndDiffMax Function(Absolute difference) --------##
##-------------------------- [ Input: 2D array (row: Channels, column: Data)] -----------------##
##--------------------- [ Output: 1D array (2ndDiffMax values for each channel)] --------------##


def secDiffMax(a):
    b = a  # Extracting the data from the 14 channels
    output = np.zeros(len(b))  # Initializing the output array with zeros (length = 14)
    temp1 = np.zeros(len(b[0]) - 1)  # To store the 1st Diffs
    k = 0
    # For counting the current row no.
    t = 0.0
    for i in b:
        for j in range(len(i) - 1):
            temp1[j] = abs(i[j + 1] - i[j])  # Obtaining the 1st Diffs
        t = temp1[1] - temp1[0]
        for j in range(len(i) - 2):
            if abs(temp1[j + 1] - temp1[j]) > t:
                t = temp1[j + 1] - temp1[
                    j]  # Comparing current Diff with the last updated Diff Max

        output[k] = t  # Storing the 2nd Diff Max for channel k
        k += 1  # Updating the current row no.
    return np.sum(output) / 14


def wrapper1(a):
    kurtosis = my_kurtosis(a)
    sec_diff_mean = secDiffMean(a)
    sec_diff_max = secDiffMax(a)
    return kurtosis, sec_diff_mean, sec_diff_max


def skewness(arr):
    data = arr
    skew_array = np.zeros(len(data))  #Initialinling the array as all 0s
    index = 0
    #current cell position in the output array

    for i in data:
        skew_array[index] = sp.stats.skew(i, axis=0, bias=True)
        index += 1  #updating the cell position
    return np.sum(skew_array) / 14


def first_diff_mean(arr):
    data = arr
    diff_mean_array = np.zeros(len(data))  #Initialinling the array as all 0s
    index = 0
    #current cell position in the output array

    for i in data:
        sum = 0.0  #initializing the sum at the start of each iteration
        for j in range(len(i) - 1):
            sum += abs(i[j + 1] - i[j])  # Obtaining the 1st Diffs

        diff_mean_array[index] = sum / (len(i) - 1)
        index += 1  #updating the cell position
    return np.sum(diff_mean_array) / 14


def first_diff_max(arr):
    data = arr
    diff_max_array = np.zeros(len(data))  #Initialinling the array as all 0s
    first_diff = np.zeros(len(data[0]) - 1)  #Initialinling the array as all 0s
    index = 0
    #current cell position in the output array

    for i in data:
        max = 0.0  #initializing at the start of each iteration
        for j in range(len(i) - 1):
            first_diff[j] = abs(i[j + 1] - i[j])  # Obtaining the 1st Diffs
            if first_diff[j] > max:
                max = first_diff[j]  # finding the maximum of the first differences
        diff_max_array[index] = max
        index += 1  #updating the cell position
    return np.sum(diff_max_array) / 14


def wrapper2(arr):
    skew = skewness(arr)
    fdmean = first_diff_mean(arr)
    fdmax = first_diff_max(arr)
    return skew, fdmean, fdmax


def wavelet_features(epoch):
    cA_values = []
    cD_values = []
    cA_mean = []
    cA_std = []
    cA_Energy = []
    cD_mean = []
    cD_std = []
    cD_Energy = []
    Entropy_D = []
    Entropy_A = []
    for i in range(14):
        cA, cD = pywt.dwt(epoch[i, :], 'coif1')
        cA_values.append(cA)
        cD_values.append(cD)  #calculating the coefficients of wavelet transform.
    for x in range(14):
        cA_mean.append(np.mean(cA_values[x]))
        cA_std.append(np.std(cA_values[x]))
        cA_Energy.append(np.sum(np.square(cA_values[x])))
        cD_mean.append(
            np.mean(cD_values[x])
        )  # mean and standard deviation values of coefficents of each channel is stored .
        cD_std.append(np.std(cD_values[x]))
        cD_Energy.append(np.sum(np.square(cD_values[x])))
        Entropy_D.append(
            np.sum(np.square(cD_values[x]) * np.log(np.square(cD_values[x])))
        )
        Entropy_A.append(
            np.sum(np.square(cA_values[x]) * np.log(np.square(cA_values[x])))
        )
    return np.sum(cA_mean) / 14, np.sum(cA_std) / 14, np.sum(cD_mean) / 14, np.sum(
        cD_std
    ) / 14, np.sum(cA_Energy) / 14, np.sum(cD_Energy) / 14, np.sum(
        Entropy_A
    ) / 14, np.sum(Entropy_D) / 14


import heapq

from scipy.signal import argrelextrema


def first_diff(i):
    b = i

    out = np.zeros(len(b))

    for j in range(len(i)):
        out[j] = b[j - 1] - b[j]  # Obtaining the 1st Diffs

        j = j + 1
        c = out[1:len(out)]
    return c


#first_diff(s)


def slope_mean(p):
    b = p  #Extracting the data from the 14 channels
    output = np.zeros(len(b))  #Initializing the output array with zeros
    res = np.zeros(len(b) - 1)

    k = 0
    #For counting the current row no.
    for i in b:
        x = i
        amp_max = i[argrelextrema(x, np.greater)[0]]
        t_max = argrelextrema(x, np.greater)[0]
        amp_min = i[argrelextrema(x, np.less)[0]]
        t_min = argrelextrema(x, np.less)[0]
        t = np.concatenate((t_max, t_min), axis=0)
        t.sort()  #sort on the basis of time

        h = 0
        amp = np.zeros(len(t))
        res = np.zeros(len(t) - 1)
        for l in range(len(t)):
            amp[l] = i[t[l]]

        amp_diff = first_diff(amp)

        t_diff = first_diff(t)

        for q in range(len(amp_diff)):
            res[q] = amp_diff[q] / t_diff[q]
        output[k] = np.mean(res)
        k = k + 1
    return np.sum(output) / 14


def first_diff(i):
    b = i

    out = np.zeros(len(b))

    for j in range(len(i)):
        out[j] = b[j - 1] - b[j]  # Obtaining the 1st Diffs

        j = j + 1
        c = out[1:len(out)]
    return c  #returns first diff


def slope_var(p):
    b = p  #Extracting the data from the 14 channels
    output = np.zeros(len(b))  #Initializing the output array with zeros
    res = np.zeros(len(b) - 1)

    k = 0
    #For counting the current row no.
    for i in b:
        x = i
        amp_max = i[argrelextrema(x, np.greater)[0]]  #storing maxima value
        t_max = argrelextrema(x, np.greater)[0]  #storing time for maxima
        amp_min = i[argrelextrema(x, np.less)[0]]  #storing minima value
        t_min = argrelextrema(x, np.less)[0]  #storing time for minima value
        t = np.concatenate((t_max, t_min), axis=0)  #making a single matrix of all matrix
        t.sort()  #sorting according to time

        h = 0
        amp = np.zeros(len(t))
        res = np.zeros(len(t) - 1)
        for l in range(len(t)):
            amp[l] = i[t[l]]

        amp_diff = first_diff(amp)

        t_diff = first_diff(t)

        for q in range(len(amp_diff)):
            res[q] = amp_diff[q] / t_diff[q]  #calculating slope

        output[k] = np.var(res)
        k = k + 1  #counting k
    return np.sum(output) / 14


def wrapper3(epoch):
    var1 = slope_mean(epoch)
    var2 = slope_var(epoch)
    return var1, var2


from scipy import signal


def maxPwelch(data_win, Fs):

    BandF = [0.1, 3, 7, 12, 30]
    PMax = np.zeros([14, (len(BandF) - 1)])

    for j in range(14):
        f, Psd = signal.welch(data_win[j, :], Fs)

        for i in range(len(BandF) - 1):
            fr = np.where((f > BandF[i]) & (f <= BandF[i + 1]))
            PMax[j, i] = np.max(Psd[fr])

    return np.sum(PMax[:, 0]) / 14, np.sum(PMax[:, 1]) / 14, np.sum(
        PMax[:, 2]
    ) / 14, np.sum(PMax[:, 3]) / 14


def entropy(labels):  # Shanon Entropy
    """ Computes entropy of 0-1 vector. """
    n_labels = len(labels)
    counts = np.bincount(labels)
    probs = counts[np.nonzero(counts)] / n_labels
    n_classes = len(probs)

    if n_classes <= 1:
        return 0
    return -np.sum(probs * np.log(probs)) / np.log(n_classes)


def autogressiveModelParameters(labels):
    b_labels = len(labels)
    feature = []
    for i in range(14):
        coeff, sig = alg.AR_est_YW(
            labels[i, :],
            11,
        )
        feature.append(coeff)
    a = []
    for i in range(11):
        a.append(np.sum(feature[:][i]) / 14)

    return a


def autogressiveModelParametersBurg(labels):
    feature = []
    feature1 = []
    model_order = 3
    for i in range(14):
        AR, rho, ref = arburg(labels[i], model_order)
        feature.append(AR)
    for j in range(14):
        for i in range(model_order):
            feature1.append(feature[j][i])

    return feature1


def main():
    lowfiles = [
        f for f in listdir('Training-Data/Low') if isfile(join('Training-Data/Low', f))
    ]
    highfiles = [
        f for f in listdir('Training-Data/High') if isfile(join('Training-Data/High', f))
    ]
    files = []

    for i in lowfiles:
        files.append([i, 'Low'])

    for i in highfiles:
        files.append([i, 'High'])

    mypath = 'Training-Data/'
    csvfile = "Features/features.csv"

    with open(csvfile, "a") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(names)
        for counter in range(len(files)):
            subfolder = files[counter][1]
            tag = files[counter][1]
            data_path = mypath + subfolder + '/' + files[counter][0]
            f = pyedflib.EdfReader(data_path)
            n = f.signals_in_file
            signal_labels = f.getSignalLabels()
            sigbufs = np.zeros((14, f.getNSamples()[3]))
            for i in np.arange(14):
                sigbufs[i, :] = f.readSignal(i + 2)
            for i in np.arange(5, 185, 3):
                features = []
                epoch = sigbufs[:, i * 128:(i + 3) * 128]
                if len(epoch[0]) == 0:
                    break

                # Hjorth Parameters
                feature_list = hjorth(epoch)
                for feat in feature_list:
                    features.append(feat)

                #Kurtosis , 2nd Diff Mean, 2nd Diff Max
                feature_list = wrapper1(epoch)
                for feat in feature_list:
                    features.append(feat)

                #Coeffeicient of Variation
                feat = coeff_var(epoch)
                features.append(feat)

                #Skewness , 1st Difference Mean, 1st Difference Max
                feature_list = wrapper2(epoch)
                for feat in feature_list:
                    features.append(feat)

                # wavelet transform features
                feature_list = wavelet_features(epoch)
                for feat in feature_list:
                    features.append(feat)

                # Variance and mean of Vertex to Vertex Slope
                feature_list = wrapper3(epoch)
                for feat in feature_list:
                    features.append(feat)

                #Fast Fourier Transform features(Max Power)
                feature_list = maxPwelch(epoch, 128)
                for feat in feature_list:
                    features.append(feat)

                #Autoregressive model Coefficients
                feature_list = autogressiveModelParametersBurg(epoch)
                for feat in feature_list:
                    features.append(feat.real)

                features.append(tag)

                writer.writerow(features)
