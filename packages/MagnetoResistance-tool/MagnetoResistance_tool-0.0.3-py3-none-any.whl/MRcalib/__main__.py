#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fit magneto-resistance data and create calibration matrix.

Created on Mon Dec  5 10:32:25 2022

@author: Andrew Ammerlaan
@contact: andrew.ammerlaan@ru.nl
@organization: High Field Magnet Laboratory, Radboud University, Nijmegen
@copyright: High Field Magnet Laboratory, Radboud University, Nijmegen
@license: GPL-3+
@version: 0.0.3
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
from MRcalib import MRcorrect


def prompt_continue():
    """Ask to coninue after showing plots."""
    while True:
        response = input("Do you want to continue? [y/n]")

        if response == "n" or response == "N":
            sys.exit(0)
        elif response == "y" or response == "Y":
            return
        else:
            print("Invalid response")


def __main__():
    # Initialize parser and read arguments
    parser = argparse.ArgumentParser(
        prog='MRcalib',
        description='Fit magneto-resistance data and create calibration matrix.',
        epilog='')

    parser.add_argument('file_in', type=str,
                        help="input file defining the measurement data")
    parser.add_argument('-o', '--out', default='calib.txt', dest='file_out', type=str,
                        help="calibration matrix output file")
    parser.add_argument('-p', '--plot', action='store_true', help="plot the data and fits")
    parser.add_argument('-B', '--field', default=3, dest="field_order", type=int,
                        help="order of polynomial to use for fitting with respect to the magnetic field")
    parser.add_argument('-T', '--temperature', default=1, dest='temp_order', type=int,
                        help="order of polynomial to use for fitting with respect to the measured temperature")
    parser.add_argument('-v', '--verbose', action='store_true', help="print values while calculating")

    args = parser.parse_args()

    # Read the input file
    try:
        input_file = pd.read_csv(args.file_in, delimiter='\t', header=None, on_bad_lines="warn",
                                 names=["File", "Field Column", "Temperature Column",
                                        "Rolling Median Window (field)", "Outlier Reject (field)",
                                        "Rolling Median Window (temperature)",
                                        "Outlier Reject (temperature)"],
                                 dtype={"File": str, "Field Column": str, "Temperature Column": str,
                                        "Rolling Median Window (field)": int, "Outlier Reject (field)": float,
                                        "Rolling Median Window (temperature)": int,
                                        "Outlier Reject (temperature)": float})
    except FileNotFoundError:
        print(f"Input file {args.file_in} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Exception {e} occured while trying to read {args.file_in}.")
        sys.exit(1)
    else:
        print("Input file read:")
        print(input_file)
        print("")

    if input_file.shape[0] - 1 <= args.temp_order:
        print(f"The number of temperature data points ({input_file.shape[0]}) must exceed the order of the temperature fitting polynomial ({args.temp_order}).")
        sys.exit(1)

    # Change working dir to where the input file is so we can use relative paths in the input file
    abs_path = os.path.abspath(args.file_in)
    abs_dir = os.path.dirname(abs_path)
    os.chdir(abs_dir)

    # This is where we will collect all the data we read
    all_data = []

    # Later we will want to make a linspace from the lowest to highest field
    lowest_field = None
    highest_field = None
    # We also want to know the length of the shortest file, we use this to determine the size of the field linspace
    field_linspace_size = None

    fit_params = pd.DataFrame()
    fit_params_err = pd.DataFrame()
    fit_fits_params = pd.DataFrame()
    fit_fits_params_err = pd.DataFrame()

    for index, file in enumerate(input_file["File"]):
        # Read the specified data file
        field_column_name = input_file["Field Column"][index]
        temp_column_name = input_file["Temperature Column"][index]
        data = pd.read_csv(file, delimiter='\t',
                           usecols=[field_column_name, temp_column_name],
                           dtype={field_column_name: float, temp_column_name: float})

        # Take the rolling median of this many points
        rol_med_window_temp = input_file["Rolling Median Window (temperature)"][index]
        # Reject a point if it differs by more than this from the rolling median
        reject_temp = input_file["Outlier Reject (temperature)"][index]

        # 0 disables rejection
        if rol_med_window_temp > 0 and reject_temp > 0:
            # Take the rolling median for all temperatures to check for spikes
            median_temp = data[temp_column_name].rolling(rol_med_window_temp
                                                         ).median().bfill().ffill()
            difference_temp = np.abs(data[temp_column_name] - median_temp)
            # This will produce an array of True/False defining which points are outliers
            not_outlier_temp = difference_temp < reject_temp
        else:
            not_outlier_temp = None

        # Take the rolling median of this many points
        rol_med_window_field = input_file["Rolling Median Window (field)"][index]
        # Reject a point if it differs by more than this from the rolling median
        reject_field = input_file["Outlier Reject (field)"][index]

        # 0 disables rejection
        if rol_med_window_field > 0 and reject_field > 0:
            # And now do the same for field
            median_field = data[field_column_name].rolling(rol_med_window_field
                                                           ).median().bfill().ffill()
            difference_field = np.abs(data[field_column_name] - median_field)
            # This will produce an array of True/False defining which points are outliers
            not_outlier_field = difference_field < reject_field
        else:
            not_outlier_field = None

        # Only keep the points that are not outliers (True)
        if not_outlier_field is not None and not_outlier_temp is not None:
            # A point is not an outlier if it is not an outlier in terms of field AND if not in terms of temperature
            not_outlier = not_outlier_temp & not_outlier_field
            data_corr = data[not_outlier]
            data_rej = data[~not_outlier]
        elif not_outlier_field is None and not_outlier_temp is not None:
            # Only temperature correction
            data_corr = data[not_outlier_temp]
            data_rej = data[~not_outlier_temp]
        elif not_outlier_field is not None and not_outlier_temp is None:
            # Only field correction
            data_corr = data[not_outlier_field]
            data_rej = data[~not_outlier_field]
        else:
            # If both are None, then we are not rejecting any points
            data_corr = data
            data_rej = None

        # Find the actual temperature, i.e. the temperature at 0 field
        zero_field_data = data_corr[temp_column_name][data_corr[field_column_name] == 0]
        actual_temp = zero_field_data.mean()
        actual_temp_std = zero_field_data.sem()

        # Set a sensible lower limit for the error, otherwise we get nonsense when we use this as weights for fitting
        # This converts the float to a string, and counts the number of characters after the decimal point
        # Minimum error is half the last non-zero decimal in the original data
        temp_err = []
        for temp in zero_field_data.to_numpy():
            temp_err.append(float('0.' + '0' * len(str(temp).split('.')[1]) + '5'))
        lower_limit = min(temp_err)
        if actual_temp_std < lower_limit:
            actual_temp_std = lower_limit

        if args.verbose:
            print("Found data for the following temperature:")
            print(f"T = {actual_temp} \u00B1 {actual_temp_std} K\n")

        # Find the highest and lowest field that is common to all datasets
        if highest_field is None:
            highest_field = data_corr[field_column_name].max()
        else:
            highest_field = max(highest_field, data_corr[field_column_name].max())
        if lowest_field is None:
            lowest_field = data_corr[field_column_name].min()
        else:
            lowest_field = min(lowest_field, data_corr[field_column_name].min())
        # And find the lenght of the shortest dataset
        if field_linspace_size is None:
            field_linspace_size = data_corr.shape[0]
        else:
            field_linspace_size = min(field_linspace_size, data_corr.shape[0])

        # And write all the data into a list of dictionaries
        all_data.append({
            "Actual Temperature": actual_temp,
            "Actual Temperature Error": actual_temp_std,
            "Accepted Data Points": data_corr,
            "Rejected Data Points": data_rej
            })

        if args.plot:
            from matplotlib.ticker import AutoMinorLocator
            import matplotlib.pyplot as plt

            plt.figure(file)
            plt.title(f"T = {actual_temp} \u00B1 {actual_temp_std} K")
            plt.xlabel("Field (T)")
            plt.ylabel("Measured Temperature (K)")
            ax = plt.gca()
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.yaxis.set_minor_locator(AutoMinorLocator())
            plt.grid(axis='both', which='both')
            plt.tick_params(axis='both', which='both')
            if data_rej is not None:
                plt.scatter(data_rej[field_column_name], data_rej[temp_column_name],
                            label="Rejected points", marker='.', color='r')
            plt.scatter(data_corr[field_column_name], data_corr[temp_column_name],
                        label="Accepted points", marker='.', color='b')
            plt.legend()
            plt.tight_layout()
            plt.draw()

    if args.plot:
        plt.show()
        prompt_continue()

    # Initialize a linear field space for fitting, the size of the smallest dataset seems reasonable
    fields = np.linspace(lowest_field, highest_field, num=field_linspace_size)
    if fields.shape[0] - 1 <= args.field_order:
        print(f"The number of field data points ({fields.shape[0]}) must exceed the order of the field fitting polynomial ({args.field_order}).")
        sys.exit(1)
    if args.plot:
        # We don't want to plot every single field, plot maximum 10 different fields
        to_plot_indices = np.unique(np.linspace(0, fields.size - 1, num=10).round())

    # Perform TvT fitting
    for to_plot, field in enumerate(fields):
        points = pd.DataFrame()
        for index, data in enumerate(all_data):
            field_column_name = input_file["Field Column"][index]
            temp_column_name = input_file["Temperature Column"][index]

            # Find the closest point in the dataset
            if field in all_data[index]["Accepted Data Points"][field_column_name]:
                # If there is an exact match, use the average of those exact matches
                field_err = 0
                matching_data = all_data[index]["Accepted Data Points"][temp_column_name][all_data[index]["Accepted Data Points"][field_column_name] == field]
                meas_temp = matching_data.mean()
                meas_temp_err = matching_data.sem()
            else:
                # If there is no exact match, take the average of the closest points over and under
                difference_from_set_field = all_data[index]["Accepted Data Points"][field_column_name] - field
                closest_under = difference_from_set_field[difference_from_set_field <= 0].abs(
                    ).sort_values().iloc[:1]
                closest_over = difference_from_set_field[difference_from_set_field >= 0].abs(
                    ).sort_values().iloc[:1]

                # This will be empty if the selected field is out of the range of the dataset
                if not closest_over.empty and not closest_under.empty:
                    field_point_under = all_data[index]["Accepted Data Points"].loc[closest_under.index]
                    field_point_over = all_data[index]["Accepted Data Points"].loc[closest_over.index]

                    field_err = np.average([closest_under.to_numpy()[0], closest_over.to_numpy()[0]])
                    meas_temp = np.average([field_point_under[temp_column_name].to_numpy()[0],
                                            field_point_over[temp_column_name].to_numpy()[0]])
                    meas_temp_err = np.std([field_point_under[temp_column_name].to_numpy()[0],
                                            field_point_over[temp_column_name].to_numpy()[0]], ddof=1) / (
                                                np.sqrt(np.size([field_point_under[temp_column_name].to_numpy()[0],
                                                                field_point_over[temp_column_name].to_numpy()[0]])))
                else:
                    # The series was empty, point does not exist
                    meas_temp = None
                    meas_temp_err = None

            if meas_temp is not None:
                # Also set a sensible lower limit for the measured temperature error
                if meas_temp_err < all_data[index]["Actual Temperature Error"]:
                    meas_temp_err = all_data[index]["Actual Temperature Error"]

                # Store this in a dataframe for easy access later
                point = pd.DataFrame()
                point["Field"] = [field]
                point["Field Error"] = field_err
                point["Measured Temperature"] = meas_temp
                point["Measured Temperature Error"] = meas_temp_err
                point["Actual Temperature"] = all_data[index]["Actual Temperature"]
                point["Actual Temperature Error"] = all_data[index]["Actual Temperature Error"]
                points = pd.concat([points, point], ignore_index=True)

        if args.verbose:
            print("Found data for the following field:")
            print(points)
            print("")

        # Before fitting, check if we have enough data at each field for the fitting, if not drop that point
        if points.shape[0] - 1 <= args.temp_order:
            if args.verbose:
                print(f"Field {field} skipped, not enough data to fit with order {args.temp_order}.")
                print("")
            continue

        # To avoid problems we need to normalize the weights
        error_inverse = 1 / points["Actual Temperature Error"]
        weights = error_inverse / np.linalg.norm(error_inverse)
        # Fit the T vs T data with a polynomial of the specified degree
        fit, fit_cov = np.polyfit(points["Measured Temperature"], points["Actual Temperature"],
                                  args.temp_order, cov=True, w=weights)

        fit_err = np.sqrt(np.diag(fit_cov))

        # Write this into a new dataframe
        fit_pd = pd.DataFrame([{"Field": field}])
        fit_pd_err = pd.DataFrame([{"Field": field}])
        for index_param, parameter in enumerate(fit):
            fit_pd[f"T^{index_param}"] = parameter
        for index_param, parameter in enumerate(fit_err):
            fit_pd_err[f"T^{index_param}"] = fit_err[index_param]

        # And then append the dataframe to our main fitting frame
        fit_params = pd.concat([fit_params, fit_pd])
        fit_params_err = pd.concat([fit_params_err, fit_pd_err])

        if args.plot:
            # Only plot 10 fields
            if to_plot in to_plot_indices:
                fit_max = max(points["Measured Temperature"].max(), points["Actual Temperature"].max())
                fit_min = min(points["Measured Temperature"].min(), points["Actual Temperature"].min())

                # Populate the space using fit
                fit_poly = np.polynomial.polynomial.Polynomial(fit)
                fit_poly_err = np.polynomial.polynomial.Polynomial(fit_err)
                x_fit = np.linspace(fit_min, fit_max, num=len(fields))
                y_fit = np.polyval(fit, x_fit)

                # And plot
                plt.figure(f"{field:.2f} T")
                plt.title(f"Fit polynomial: {fit_poly} \u00B1 {fit_poly_err}")
                plt.xlabel("Measured Temperature (K)")
                plt.ylabel("Actual Temperature (K)")
                ax = plt.gca()
                ax.xaxis.set_minor_locator(AutoMinorLocator())
                ax.yaxis.set_minor_locator(AutoMinorLocator())
                plt.grid(axis='both', which='both')
                plt.tick_params(axis='both', which='both')
                plt.errorbar(points["Measured Temperature"], points["Actual Temperature"],
                             xerr=points["Measured Temperature Error"], yerr=points["Actual Temperature Error"],
                             fmt='.', label=f"Data {field:.2f} T")
                plt.plot(x_fit, y_fit, linestyle="dotted", label=f"Fit {field:.2f} T")
                plt.legend()
                plt.tight_layout()
                plt.draw()

    if args.verbose:
        print("Fitted measured temperature versus actual temperature for each field, found paramters:")
        print(fit_params)
        print("")
        print("With uncertainty:")
        print(fit_params_err)
        print("")

    if args.plot:
        plt.show()
        prompt_continue()

    # Now fit the fits to get the field dependence
    to_fit_x = fit_params["Field"]
    for index_param in range(0, fit_params.shape[1] - 1):
        # Get the name of the column we are fitting: T^0 .... T^(size - 2)
        column_name = f"T^{index_param}"
        to_fit_y = fit_params[column_name]
        # To avoid problems we need to normalize the weights
        error_inverse = 1 / fit_params_err[column_name]
        weights = error_inverse / np.linalg.norm(error_inverse)

        fit_fit, fit_fit_cov = np.polyfit(to_fit_x, to_fit_y, args.field_order,
                                          w=weights, cov=True)

        fit_fit_err = np.sqrt(np.diag(fit_fit_cov))

        # Write this into a nice dictionary
        index_names = []
        for index_param, parameter in enumerate(fit_fit):
            index_names += [f"B^{index_param}"]
        fit_fit_pd = pd.DataFrame(data=fit_fit, index=index_names, columns=[column_name])
        fit_fit_pd_err = pd.DataFrame(data=fit_fit_err, index=index_names, columns=[column_name])

        # And then append the dictionary to our main fitting frame
        fit_fits_params[column_name] = fit_fit_pd
        fit_fits_params_err[column_name] = fit_fit_pd_err

    if args.verbose:
        print("Fitted temperature fit paramters versus field, found paramters:")
        print(fit_fits_params)
        print("")
        print("With uncertainty:")
        print(fit_fits_params_err)
        print("")

    # Write these params to file so we can use them elsewhere
    with open(args.file_out, 'w') as f:
        f.write("Calibration Parameters:\n")
        f.close()
    fit_fits_params.to_csv(args.file_out, sep='\t', mode='a')
    with open(args.file_out, 'a') as f:
        f.write("Calibration Parameter Uncertainty:\n")
        f.close()
    fit_fits_params_err.to_csv(args.file_out, sep='\t', mode='a')

    if args.plot:
        # Preform sanity check, do we get the correct actual temperature if we
        # run the correction function on our input data files
        plt.figure("Sanity check")
        plt.title("Sanity check: MR correction applied to input files, curves should be relatively flat")
        plt.xlabel("Field (T)")
        plt.ylabel("Actual Temperature (K)")
        ax = plt.gca()
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        plt.grid(axis='both', which='both')
        plt.tick_params(axis='both', which='both')

        for index, data in enumerate(all_data):
            field_column_name = input_file["Field Column"][index]
            temp_column_name = input_file["Temperature Column"][index]
            field_data = data["Accepted Data Points"][field_column_name]
            temp_data = data["Accepted Data Points"][temp_column_name]
            actual_T = data["Actual Temperature"]

            actual_T_fit, actual_T_fit_err = MRcorrect(args.file_out, field_data, temp_data, verbose=args.verbose)
            plt.errorbar(field_data, actual_T_fit, yerr=actual_T_fit_err, fmt='.', label=f"{actual_T} K")
            plt.hlines(actual_T, fields.min(), fields.max(), color="grey")

        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    __main__()
