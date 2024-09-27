#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correct for MagnetoResistance using calibration matrix.

Created on Mon Dec  5 10:32:25 2022

@author: Andrew Ammerlaan
@contact: andrew.ammerlaan@ru.nl
@organization: High Field Magnet Laboratory, Radboud University, Nijmegen
@copyright: High Field Magnet Laboratory, Radboud University, Nijmegen
@license: GPL-3+
@version: 0.0.1
"""

import pandas as pd
import numpy as np
from typing import Union, Tuple
from math import sqrt


def MRcorrect(calib_file: str, fields: Union[int, float, list, np.ndarray, pd.DataFrame],
              measured_temps: Union[int, float, list, np.ndarray, pd.DataFrame],
              verbose: bool = False) -> Union[Tuple[float, float], Tuple[np.ndarray, np.ndarray]]:
    """
    Read calibration file and calculate the actual temperature using field and measured temperature data.

    Takes a single float/int temperature and field point or a list/array/dataframe of multiple points.
    Returns both the actual temperature and the error in the actual temperature in either float or array format.
    Use verbose=True to print read calibration file.
    """
    # Determine number of lines in calibration file
    with open(calib_file, 'r') as f:
        for count, line in enumerate(f):
            pass
    count = count + 1
    if verbose:
        print(f"Number of lines in calibration file: {count }")
        print("")

    if type(fields) is not type(measured_temps):
        raise TypeError(f"Field and temperature data must be of same type: {type(fields)} and {type(measured_temps)}")

    # Number of lines containing calibration paramters (4 Header lines)
    calib_lines = int((count - 4) / 2)
    # Read calibration file
    params = pd.read_csv(calib_file, delimiter='\t', skiprows=1, nrows=calib_lines, index_col=0)
    params_error = pd.read_csv(calib_file, delimiter='\t', skiprows=(3 + calib_lines), nrows=calib_lines, index_col=0)

    if verbose:
        print("Read calibration paramters:")
        print(params)
        print("")
        print("With uncertainty:")
        print(params_error)
        print("")

    # Now calculate the actual temperature using the calibration
    S = params_error**2
    if type(fields) is float or type(fields) is int:
        T_fit_params = []
        T_fit_params_error = []
        for T_order in params:
            T_fit_params += [np.polyval(params[T_order].tolist(), fields)]
            T_fit_params_error += [np.polyval(S[T_order].tolist(), fields)]
        Actual_temp = np.polyval(T_fit_params, measured_temps)
        Actual_temp_err = np.polyval(T_fit_params_error, measured_temps)
        return (Actual_temp, sqrt(Actual_temp_err))

    elif type(fields) is np.ndarray or type(fields) is list or type(fields) is pd.DataFrame or type(fields) is pd.Series:
        if type(fields) is list:
            if len(fields) != len(measured_temps):
                raise TypeError(f"Field and temperature data must be of  same length: {len(fields)} and {len(measured_temps)}")
        else:
            if fields.shape != measured_temps.shape:
                raise TypeError(f"Field and temperature data must be of  same shape: {fields.shape} and {measured_temps.shape}")
            if type(fields) is pd.DataFrame or type(fields) is pd.Series:
                # We need to reset the index to ensure that all indices exist when we try to reference them below
                measured_temps.reset_index(inplace=True, drop=True)
                fields.reset_index(inplace=True, drop=True)

        Actual_temps = np.empty(0)
        Actual_temps_err = np.empty(0)
        for index, field in enumerate(fields):
            T_fit_params = np.empty(0)
            T_fit_params_error = np.empty(0)
            for T_order in params:
                T_fit_params = np.append(T_fit_params, np.polyval(params[T_order].tolist(), field))
                T_fit_params_error = np.append(T_fit_params_error, np.polyval(S[T_order].tolist(), field))
            Actual_temps = np.append(Actual_temps, np.polyval(T_fit_params, measured_temps[index]))
            Actual_temps_err = np.append(Actual_temps_err, np.polyval(T_fit_params_error, measured_temps[index]))
        return (Actual_temps, np.sqrt(Actual_temps_err))

    else:
        raise TypeError(f"Field and temperature data must be of type float, integer, list, numpy array, or pandas dataframe not {type(fields)}")
