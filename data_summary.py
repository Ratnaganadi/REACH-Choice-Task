import pandas
import glob
path = "data/complete_data/"

main_data = []
for filename in glob.glob(path + "*.xls"):
    if ("conflicted copy" not in filename) and ("test" not in filename):
        in_data = pandas.read_excel(filename, "Main")
        out_data = {}

        out_data["subject_id"] = filename.split("/")[-1].split("_")[0]

        if out_data["subject_id"]:

            # Compute number of trials for threshold, per task, and total
            try:
                out_data["spatial_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Spatial"))
            except AttributeError:
                out_data["spatial_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Spatial"))
            try:
                out_data["phon_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Phonology"))
            except AttributeError:
                out_data["phon_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Phonology"))
            try:
                out_data["math_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Math"))
            except AttributeError:
                out_data["math_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Math"))
            try:
                out_data["music_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Music"))
            except AttributeError:
                out_data["music_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Music"))
            try:
                out_data["read_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Reading"))
            except AttributeError:
                out_data["read_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Reading"))
            try:
                out_data["dots_trials_threshold"] = sum((in_data.type=="threshold") & (in_data.task=="Dots"))
            except AttributeError:
                out_data["dots_trials_threshold"] = sum((in_data.Type=="threshold") & (in_data.Game=="Dots"))
            try:
                out_data["total_trials_threshold"] = sum(in_data.type=="threshold")
            except AttributeError:
                out_data["total_trials_threshold"] = sum(in_data.Type=="threshold")
            
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
                    out_data["spatial_final_level_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Spatial")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Spatial")].Difficulty):
                    out_data["spatial_final_level_threshold"] = in_data[(in_data.Type=="threshold")&(in_data.Game=="Spatial")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Phonology")].threshold_var):
                    out_data["phon_final_level_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Phonology")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Phonology")].Difficulty):
                    out_data["phon_final_level_threshold"] = in_data[(in_data.Type=="threshold")&(in_data.Game=="Phonology")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Math")].threshold_var):
                    out_data["math_final_level_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Math")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Math")].Difficulty):
                    out_data["math_final_level_threshold"] = in_data[(in_data.Type=="threshold")&(in_data.Game=="Math")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Music")].threshold_var):
                    out_data["music_final_level_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Music")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Music")].Difficulty):
                    out_data["music_final_level_threshold"] = in_data[(in_data.Type=="threshold")&(in_data.Game=="Music")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Reading")].threshold_var):
                    out_data["read_final_level_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Reading")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Reading")].Difficulty):
                    out_data["read_final_level_threshold"] = in_data[(in_data.Type=="threshold")&(in_data.Game=="Reading")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="threshold")&(in_data.task=="Dots")].threshold_var):
                    out_data["dots_final_level_threshold"] = in_data[(in_data.type=="threshold")&(in_data.task=="Dots")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="threshold")&(in_data.Game=="Dots")].Difficulty):
                    out_data["dots_final_level_threshold"] = in_data[(in_data.Type=="threshold")&(in_data.Game=="Dots")].Difficulty.iloc[-1]

            # Compute number of trials for choice, per task, and total
            try:
                out_data["spatial_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Spatial"))
            except AttributeError:
                out_data["spatial_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Spatial"))
            try:
                out_data["phon_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Phonology"))
            except AttributeError:
                out_data["phon_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Phonology"))
            try:
                out_data["math_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Math"))
            except AttributeError:
                out_data["math_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Math"))
            try:
                out_data["music_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Music"))
            except AttributeError:
                out_data["music_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Music"))
            try:
                out_data["read_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Reading"))
            except AttributeError:
                out_data["read_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Reading"))
            try:
                out_data["dots_trials_choice"] = sum((in_data.type=="choice") & (in_data.task=="Dots"))
            except AttributeError:
                out_data["dots_trials_choice"] = sum((in_data.Type=="choice") & (in_data.Game=="Dots"))
            try:
                out_data["total_trials_choice"] = sum(in_data.type=="choice")
            except AttributeError:
                out_data["total_trials_choice"] = sum(in_data.Type=="choice")
            
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
                out_data["spatial_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].score)
            except AttributeError:
                out_data["spatial_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Spatial")].Score)
            try:
                out_data["phon_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].score)
            except AttributeError:
                out_data["phon_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Phonology")].Score)
            try:
                out_data["math_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Math")].score)
            except AttributeError:
                out_data["math_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Math")].Score)
            try:
                out_data["music_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Music")].score)
            except AttributeError:
                out_data["music_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Music")].Score)
            try:
                out_data["read_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Reading")].score)
            except AttributeError:
                out_data["read_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Reading")].Score)
            try:
                out_data["dots_chosen_trials_choice"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Dots")].score)
            except AttributeError:
                out_data["dots_chosen_trials_choice"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Dots")].Score)


            # Compute frequency of choice, per task
            try:
                out_data["spatial_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].score)/float(sum(in_data[(in_data.type=="choice")].score))
            except AttributeError:
                out_data["spatial_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Spatial")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score))
            try:
                out_data["phon_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].score)/float(sum(in_data[(in_data.type=="choice")].score))
            except AttributeError:
                out_data["phon_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Phonology")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score))
            try:
                out_data["math_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Math")].score)/float(sum(in_data[(in_data.type=="choice")].score))
            except AttributeError:
                out_data["math_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Math")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score))
            try:
                out_data["music_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Music")].score)/float(sum(in_data[(in_data.type=="choice")].score))
            except AttributeError:
                out_data["music_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Music")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score))
            try:
                out_data["read_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Reading")].score)/float(sum(in_data[(in_data.type=="choice")].score))
            except AttributeError:
                out_data["read_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Reading")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score))
            try:
                out_data["dots_chosen_frequency"] = sum(in_data[(in_data.type=="choice")&(in_data.task=="Dots")].score)/float(sum(in_data[(in_data.type=="choice")].score))
            except AttributeError:
                out_data["dots_chosen_frequency"] = sum(in_data[(in_data.Type=="choice")&(in_data.Game=="Dots")].Score)/float(sum(in_data[(in_data.Type=="choice")].Score))

            # Compute final level for choice, per task
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].threshold_var):
                    out_data["spatial_final_level_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Spatial")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Spatial")].Difficulty):
                    out_data["spatial_final_level_choice"] = in_data[(in_data.Type=="choice")&(in_data.Game=="Spatial")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].threshold_var):
                    out_data["phon_final_level_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Phonology")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Phonology")].Difficulty):
                    out_data["phon_final_level_choice"] = in_data[(in_data.Type=="choice")&(in_data.Game=="Phonology")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Math")].threshold_var):
                    out_data["math_final_level_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Math")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Math")].Difficulty):
                    out_data["math_final_level_choice"] = in_data[(in_data.Type=="choice")&(in_data.Game=="Math")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Music")].threshold_var):
                    out_data["music_final_level_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Music")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Music")].Difficulty):
                    out_data["music_final_level_choice"] = in_data[(in_data.Type=="choice")&(in_data.Game=="Music")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Reading")].threshold_var):
                    out_data["read_final_level_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Reading")].threshold_var.iloc[-1]
            except AttributeError:
                if len(in_data[(in_data.Type=="choice")&(in_data.Game=="Reading")].Difficulty):
                    out_data["read_final_level_choice"] = in_data[(in_data.Type=="choice")&(in_data.Game=="Reading")].Difficulty.iloc[-1]
            try:
                if len(in_data[(in_data.type=="choice")&(in_data.task=="Dots")].threshold_var):
                    out_data["dots_final_level_choice"] = in_data[(in_data.type=="choice")&(in_data.task=="Dots")].threshold_var.iloc[-1]
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
    "phon_final_level_threshold",
    "math_final_level_threshold",
    "music_final_level_threshold",
    "read_final_level_threshold",
    "dots_final_level_threshold",
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
    "phon_final_level_choice",
    "math_final_level_choice",
    "music_final_level_choice",
    "read_final_level_choice",
    "dots_final_level_choice",
]


main_data.to_excel("REACH_summary.xls", sheet_name="REACH_SUMMARY", columns=column_headers, index=False)