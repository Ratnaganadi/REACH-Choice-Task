import pandas
import glob
import numpy as np
from dir_function import get_homepath

dir_hierarchy = 1
homepath = get_homepath(dir_hierarchy,go_home='')
path = "data/complete_data/"

main_data = []
for filename in glob.glob(path + "*.xls"):
    if ("conflicted copy" not in filename) and ("test" not in filename):
        in_data = pandas.read_excel(filename, "Main")
        math_data = pandas.read_excel(filename, "Math")
        out_data = {}

        out_data["subject_id"] = filename.split("/")[-1].split("_")[0]

        if out_data["subject_id"]:

            # Compute number of trials for threshold, per task, and total
            try:
                out_data["spatial_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Spatial")) or np.nan
            except AttributeError:
                out_data["spatial_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Spatial")) or np.nan
            try:
                out_data["phon_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Phonology")) or np.nan
            except AttributeError:
                out_data["phon_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Phonology")) or np.nan
            try:
                out_data["math_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Math")) or np.nan
            except AttributeError:
                out_data["math_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Math")) or np.nan
            try:
                out_data["music_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Music")) or np.nan
            except AttributeError:
                out_data["music_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Music")) or np.nan
            try:
                out_data["read_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Reading")) or np.nan
            except AttributeError:
                out_data["read_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Reading")) or np.nan
            try:
                out_data["dots_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Dots")) or np.nan
            except AttributeError:
                out_data["dots_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Dots")) or np.nan
            try:
                out_data["total_trials_threshold"] = sum(in_data.type=="threshold") or np.nan
            except AttributeError:
                out_data["total_trials_threshold"] = sum(in_data.Type=="threshold") or np.nan
            
            # Compute accuracy for threshold, per task, and total
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Spatial")].score):
                    out_data["spatial_acc_threshold"] = sum(in_data[(in_data.type=="threshold")&(in_data.task=="Spatial")].score)/float(len(in_data[(in_data.type=="threshold")&(in_data.task=="Spatial")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Spatial")].Score):
                    out_data["spatial_acc_threshold"] = sum(in_data[(in_data.Type=="threshold")&(in_data.Game=="Spatial")].Score)/float(len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Spatial")].Score))
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Phonology")].score):
                    out_data["phon_acc_threshold"] = sum(in_data[(in_data.type=="threshold")&(in_data.task=="Phonology")].score)/float(len(in_data[(in_data.type=="threshold")&(in_data.task=="Phonology")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Phonology")].Score):
                    out_data["phon_acc_threshold"] = sum(in_data[(in_data.Type=="threshold")&(in_data.Game=="Phonology")].Score)/float(len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Phonology")].Score))
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Math")].score):
                    out_data["math_acc_threshold"] = sum(in_data[(in_data.type=="threshold")&(in_data.task=="Math")].score)/float(len(in_data[(in_data.type=="threshold")&(in_data.task=="Math")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Math")].Score):
                    out_data["math_acc_threshold"] = sum(in_data[(in_data.Type=="threshold")&(in_data.Game=="Math")].Score)/float(len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Math")].Score))
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Music")].score):
                    out_data["music_acc_threshold"] = sum(in_data[(in_data.type=="threshold")&(in_data.task=="Music")].score)/float(len(in_data[(in_data.type=="threshold")&(in_data.task=="Music")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Music")].Score):
                    out_data["music_acc_threshold"] = sum(in_data[(in_data.Type=="threshold")&(in_data.Game=="Music")].Score)/float(len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Music")].Score))
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Reading")].score):
                    out_data["read_acc_threshold"] = sum(in_data[(in_data.type=="threshold")&(in_data.task=="Reading")].score)/float(len(in_data[(in_data.type=="threshold")&(in_data.task=="Reading")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Reading")].Score):
                    out_data["read_acc_threshold"] = sum(in_data[(in_data.Type=="threshold")&(in_data.Game=="Reading")].Score)/float(len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Reading")].Score))
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Dots")].score):
                    out_data["dots_acc_threshold"] = sum(in_data[(in_data.type=="threshold")&(in_data.task=="Dots")].score)/float(len(in_data[(in_data.type=="threshold")&(in_data.task=="Dots")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Dots")].Score):
                    out_data["dots_acc_threshold"] = sum(in_data[(in_data.Type=="threshold")&(in_data.Game=="Dots")].Score)/float(len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Dots")].Score))
            try:
                if len(in_data[(in_data.type=="threshold")].score):
                    out_data["total_acc_threshold"] = sum(in_data[(in_data.type=="threshold")].score)/float(len(in_data[(in_data.type=="threshold")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")].Score):
                    out_data["total_acc_threshold"] = sum(in_data[(in_data.Type=="threshold")].Score)/float(len(in_data[(in_data.Type=="threshold")].Score))

            # Compute final level for threshold, per task
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Spatial")].threshold_var):
                    out_data["spatial_final_level_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Spatial")].level.iloc[-1]
                    out_data["spatial_final_level_exp_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Spatial")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Spatial")].Difficulty):
                    out_data["spatial_final_level_threshold"] = in_data[(in_data.Type=="threshold")&(in_data.Game=="Spatial")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Phonology")].threshold_var):
                    out_data["phon_final_level_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Phonology")].level.iloc[-1]
                    out_data["phon_final_level_exp_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Phonology")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Phonology")].Difficulty):
                    out_data["phon_final_level_threshold"] = in_data[(in_data.Type=="threshold")&(in_data.Game=="Phonology")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Math")].threshold_var):
                    if len(in_data[(in_data.type=="threshold")&(in_data.task=="Math")&(in_data.threshold_var=="addition")].threshold_var):
                        out_data["math_final_level_threshold_addition"] = in_data[(in_data.type=="threshold")&(in_data.task=="Math")&(in_data.threshold_var=="addition")].level.iloc[-1]
                    if len(in_data[(in_data.type=="threshold")&(in_data.task=="Math")&(in_data.threshold_var=="subtraction")].threshold_var):
                        out_data["math_final_level_threshold_subtraction"] = in_data[(in_data.type=="threshold")&(in_data.task=="Math")&(in_data.threshold_var=="subtraction")].level.iloc[-1]
                    if len(in_data[(in_data.type=="threshold")&(in_data.task=="Math")&(in_data.threshold_var=="multiplication")].threshold_var):
                        out_data["math_final_level_threshold_multiplication"] = in_data[(in_data.type=="threshold")&(in_data.task=="Math")&(in_data.threshold_var=="multiplication")].level.iloc[-1]
                    if len(in_data[(in_data.type=="threshold")&(in_data.task=="Math")&(in_data.threshold_var=="division")].threshold_var):
                        out_data["math_final_level_threshold_division"] = in_data[(in_data.type=="threshold")&(in_data.task=="Math")&(in_data.threshold_var=="division")].level.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Math")].Difficulty):
                    math_thresh_trial_number = in_data[(in_data.Type=="threshold")&(in_data.Game=="Math")]["Trial Number"].iloc[-1]
                    threshold_math_data = math_data[math_data["Trial Number"]<=math_thresh_trial_number]
                    if len(threshold_math_data[(threshold_math_data.Game=="Math")&(threshold_math_data.Operation=="addition")].Operation):
                        out_data["math_final_level_threshold_addition"] = threshold_math_data[(threshold_math_data.Game=="Math")&(threshold_math_data.Operation=="addition")].Difficulty.iloc[-1]
                    if len(threshold_math_data[(threshold_math_data.Game=="Math")&(threshold_math_data.Operation=="subtraction")].Operation):
                        out_data["math_final_level_threshold_subtraction"] = threshold_math_data[(threshold_math_data.Game=="Math")&(threshold_math_data.Operation=="subtraction")].Difficulty.iloc[-1]
                    if len(threshold_math_data[(threshold_math_data.Game=="Math")&(threshold_math_data.Operation=="multiplication")].Operation):
                        out_data["math_final_level_threshold_multiplication"] = threshold_math_data[(threshold_math_data.Game=="Math")&(threshold_math_data.Operation=="multiplication")].Difficulty.iloc[-1]
                    if len(threshold_math_data[(threshold_math_data.Game=="Math")&(threshold_math_data.Operation=="division")].Operation):
                        out_data["math_final_level_threshold_division"] = threshold_math_data[(threshold_math_data.Game=="Math")&(threshold_math_data.Operation=="division")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Music")].threshold_var):
                    out_data["music_final_level_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Music")].level.iloc[-1]
                    out_data["music_final_level_exp_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Music")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Music")].Difficulty):
                    out_data["music_final_level_threshold"] = in_data[(in_data.Type=="threshold")&(in_data.Game=="Music")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Reading")].threshold_var):
                    out_data["read_final_level_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Reading")].level.iloc[-1]
                    out_data["read_final_level_exp_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Reading")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Reading")].Difficulty):
                    out_data["read_final_level_threshold"] = in_data[(in_data.Type=="threshold")&(in_data.Game=="Reading")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Dots")].threshold_var):
                    out_data["dots_final_level_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Dots")].level.iloc[-1]
                    out_data["dots_final_level_exp_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Dots")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Dots")].Difficulty):
                    out_data["dots_final_level_threshold"] = in_data[(in_data.Type=="threshold")&(in_data.Game=="Dots")].Difficulty.iloc[-1]

            # Compute number of trials for choice, per task, and total
            try:
                out_data["spatial_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Spatial")) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["spatial_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Spatial")) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["phon_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Phonology")) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["phon_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Phonology")) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["math_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Math")) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["math_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Math")) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["music_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Music")) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["music_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Music")) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["read_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Reading")) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["read_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Reading")) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["dots_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Dots")) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["dots_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Dots")) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["total_trials_choice"] = sum(in_data.type=="choice") or np.nan
            except AttributeError:
                out_data["total_trials_choice"] = sum(in_data.Type=="choice") or np.nan
            
            # Compute accuracy for choice, per task, and total
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].score):
                    out_data["spatial_acc_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].score)/float(len(in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Spatial")].Score):
                    out_data["spatial_acc_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Spatial")].Score)/float(len(in_data[(in_data.Type=="choice")&(in_data.Game=="Spatial")].Score))
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].score):
                    out_data["phon_acc_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].score)/float(len(in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Phonology")].Score):
                    out_data["phon_acc_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Phonology")].Score)/float(len(in_data[(in_data.Type=="choice")&(in_data.Game=="Phonology")].Score))
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Math")].score):
                    out_data["math_acc_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Math")].score)/float(len(in_data[(in_data.type=="choice")&(in_data.task=="Math")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Math")].Score):
                    out_data["math_acc_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Math")].Score)/float(len(in_data[(in_data.Type=="choice")&(in_data.Game=="Math")].Score))
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Music")].score):
                    out_data["music_acc_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Music")].score)/float(len(in_data[(in_data.type=="choice")&(in_data.task=="Music")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Music")].Score):
                    out_data["music_acc_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Music")].Score)/float(len(in_data[(in_data.Type=="choice")&(in_data.Game=="Music")].Score))
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Reading")].score):
                    out_data["read_acc_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Reading")].score)/float(len(in_data[(in_data.type=="choice")&(in_data.task=="Reading")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Reading")].Score):
                    out_data["read_acc_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Reading")].Score)/float(len(in_data[(in_data.Type=="choice")&(in_data.Game=="Reading")].Score))
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Dots")].score):
                    out_data["dots_acc_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Dots")].score)/float(len(in_data[(in_data.type=="choice")&(in_data.task=="Dots")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Dots")].Score):
                    out_data["dots_acc_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Dots")].Score)/float(len(in_data[(in_data.Type=="choice")&(in_data.Game=="Dots")].Score))
            try:
                if len(in_data[(in_data.type=="choice")].score):
                    out_data["total_acc_choice"] = sum(in_data[(in_data.type=="choice")].score)/float(len(in_data[(in_data.type=="choice")].score))
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")].Score):
                    out_data["total_acc_choice"] = sum(in_data[(in_data.Type=="choice")].Score)/float(len(in_data[(in_data.Type=="choice")].Score))

            # Compute number of times chosen for choice, per task
            try:
                out_data["spatial_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].score) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["spatial_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Spatial")].Score) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["phon_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].score) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["phon_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Phonology")].Score) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["math_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Math")].score) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["math_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Math")].Score) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["music_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Music")].score) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["music_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Music")].Score) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["read_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Reading")].score) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["read_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Reading")].Score) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["dots_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Dots")].score) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["dots_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Dots")].Score) if sum(in_data.Type=="choice") else np.nan


            # Compute frequency of choice, per task
            try:
                out_data["spatial_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].score)/float(sum(in_data[(in_data.type=="choice")].score)) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["spatial_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Spatial")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score)) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["phon_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].score)/float(sum(in_data[(in_data.type=="choice")].score)) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["phon_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Phonology")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score)) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["math_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Math")].score)/float(sum(in_data[(in_data.type=="choice")].score)) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["math_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Math")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score)) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["music_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Music")].score)/float(sum(in_data[(in_data.type=="choice")].score)) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["music_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Music")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score)) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["read_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Reading")].score)/float(sum(in_data[(in_data.type=="choice")].score)) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["read_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Reading")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score)) if sum(in_data.Type=="choice") else np.nan
            try:
                out_data["dots_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Dots")].score)/float(sum(in_data[(in_data.type=="choice")].score)) if sum(in_data.type=="choice") else np.nan
            except AttributeError:
                out_data["dots_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Dots")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score)) if sum(in_data.Type=="choice") else np.nan

            # Compute final level for choice, per task
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].threshold_var):
                    out_data["spatial_final_level_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].level.iloc[-1]
                    out_data["spatial_final_level_exp_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Spatial")].Difficulty):
                    out_data["spatial_final_level_choice"] = in_data[(in_data.Type=="choice")&(in_data.Game=="Spatial")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].threshold_var):
                    out_data["phon_final_level_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].level.iloc[-1]
                    out_data["phon_final_level_exp_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Phonology")].Difficulty):
                    out_data["phon_final_level_choice"] = in_data[(in_data.Type=="choice")&(in_data.Game=="Phonology")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Math")].threshold_var):
                    if len(in_data[(in_data.type=="choice")&(in_data.task=="Math")&(in_data.threshold_var=="addition")].threshold_var):
                        out_data["math_final_level_choice_addition"] = in_data[(in_data.type=="choice")&(in_data.task=="Math")&(in_data.threshold_var=="addition")].level.iloc[-1]
                    if len(in_data[(in_data.type=="choice")&(in_data.task=="Math")&(in_data.threshold_var=="subtraction")].threshold_var):
                        out_data["math_final_level_choice_subtraction"] = in_data[(in_data.type=="choice")&(in_data.task=="Math")&(in_data.threshold_var=="subtraction")].level.iloc[-1]
                    if len(in_data[(in_data.type=="choice")&(in_data.task=="Math")&(in_data.threshold_var=="multiplication")].threshold_var):
                        out_data["math_final_level_choice_multiplication"] = in_data[(in_data.type=="choice")&(in_data.task=="Math")&(in_data.threshold_var=="multiplication")].level.iloc[-1]
                    if len(in_data[(in_data.type=="choice")&(in_data.task=="Math")&(in_data.threshold_var=="division")].threshold_var):
                        out_data["math_final_level_choice_division"] = in_data[(in_data.type=="choice")&(in_data.task=="Math")&(in_data.threshold_var=="division")].level.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Math")].Difficulty):
                    math_choice_trial_number = in_data[(in_data.Type=="choice")&(in_data.Game=="Math")]["Trial Number"].iloc[0]
                    choice_math_data = math_data[math_data["Trial Number"]>=math_thresh_trial_number]
                    if len(choice_math_data[(choice_math_data.Game=="Math")&(choice_math_data.Operation=="addition")].Operation):
                        out_data["math_final_level_choice_addition"] = choice_math_data[(choice_math_data.Game=="Math")&(choice_math_data.Operation=="addition")].Difficulty.iloc[-1]
                    if len(choice_math_data[(choice_math_data.Game=="Math")&(choice_math_data.Operation=="subtraction")].Operation):
                        out_data["math_final_level_choice_subtraction"] = choice_math_data[(choice_math_data.Game=="Math")&(choice_math_data.Operation=="subtraction")].Difficulty.iloc[-1]
                    if len(choice_math_data[(choice_math_data.Game=="Math")&(choice_math_data.Operation=="multiplication")].Operation):
                        out_data["math_final_level_choice_multiplication"] = choice_math_data[(choice_math_data.Game=="Math")&(choice_math_data.Operation=="multiplication")].Difficulty.iloc[-1]
                    if len(choice_math_data[(choice_math_data.Game=="Math")&(choice_math_data.Operation=="division")].Operation):
                        out_data["math_final_level_choice_division"] = choice_math_data[(choice_math_data.Game=="Math")&(choice_math_data.Operation=="division")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Music")].threshold_var):
                    out_data["music_final_level_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Music")].level.iloc[-1]
                    out_data["music_final_level_exp_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Music")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Music")].Difficulty):
                    out_data["music_final_level_choice"] = in_data[(in_data.Type=="choice")&(in_data.Game=="Music")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Reading")].threshold_var):
                    out_data["read_final_level_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Reading")].level.iloc[-1]
                    out_data["read_final_level_exp_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Reading")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Reading")].Difficulty):
                    out_data["read_final_level_choice"] = in_data[(in_data.Type=="choice")&(in_data.Game=="Reading")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Dots")].threshold_var):
                    out_data["dots_final_level_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Dots")].level.iloc[-1]
                    out_data["dots_final_level_exp_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Dots")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Dots")].Difficulty):
                    out_data["dots_final_level_choice"] = in_data[(in_data.Type=="choice")&(in_data.Game=="Dots")].Difficulty.iloc[-1]


            main_data.append(out_data)

main_data = pandas.DataFrame(main_data)

column_headers = [
    "subject_id",
    "spatial_trials_threshold",
    "phon_trials_threshold",
    "math_trials_threshold",
    "music_trials_threshold",
    "read_trials_threshold",
    "dots_trials_threshold",
    "total_trials_threshold",
    "spatial_acc_threshold",
    "phon_acc_threshold",
    "math_acc_threshold",
    "music_acc_threshold",
    "read_acc_threshold",
    "dots_acc_threshold",
    "total_acc_threshold",
    "spatial_final_level_threshold",
    "spatial_final_level_exp_threshold",
    "phon_final_level_threshold",
    "phon_final_level_exp_threshold",
    "math_final_level_threshold_addition",
    "math_final_level_threshold_subtraction",
    "math_final_level_threshold_multiplication",
    "math_final_level_threshold_division", 
    "music_final_level_threshold",
    "music_final_level_exp_threshold",
    "read_final_level_threshold",
    "read_final_level_exp_threshold",
    "dots_final_level_threshold",
    "dots_final_level_exp_threshold",
    "spatial_trials_choice",
    "phon_trials_choice",
    "math_trials_choice",
    "music_trials_choice",
    "read_trials_choice",
    "dots_trials_choice",
    "total_trials_choice",
    "spatial_acc_choice",
    "phon_acc_choice",
    "math_acc_choice",
    "music_acc_choice",
    "read_acc_choice",
    "dots_acc_choice",
    "total_acc_choice",
    "spatial_chosen_trials_choice",
    "phon_chosen_trials_choice",
    "math_chosen_trials_choice",
    "music_chosen_trials_choice",
    "read_chosen_trials_choice",
    "dots_chosen_trials_choice",
    "spatial_chosen_frequency",
    "phon_chosen_frequency",
    "math_chosen_frequency",
    "music_chosen_frequency",
    "read_chosen_frequency",
    "dots_chosen_frequency",
    "spatial_final_level_choice",
    "spatial_final_level_exp_choice",
    "phon_final_level_choice",
    "phon_final_level_exp_choice",
    "math_final_level_choice_addition",
    "math_final_level_choice_subtraction",
    "math_final_level_choice_multiplication",
    "math_final_level_choice_division", 
    "music_final_level_choice",
    "music_final_level_exp_choice",
    "read_final_level_choice",
    "read_final_level_exp_choice",
    "dots_final_level_choice",
    "dots_final_level_exp_choice",
]

os.chdir('data_analysis')
main_data.to_excel("REACH_summary.xls", sheet_name="REACH_SUMMARY", columns=column_headers, index=False)