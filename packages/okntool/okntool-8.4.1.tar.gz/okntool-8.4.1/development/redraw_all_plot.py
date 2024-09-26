import json
import os
from ehdg_tools.ehdg_plotter import summary_plot, trial_plot

if __name__ == '__main__':
    main_dir = r"C:\Users\zawli\Desktop\ABI\zkou_right_eye_v_2_0_DELL-S2716DG-11-06-2024_kids_long_screener\trials"
    plot_con = r"C:\Users\zawli\Documents\GitHub\okntool\okntool\oknserver_graph_plot_config.json"
    with open(plot_con) as f:
        pi = json.load(f)
    ti = pi["trial_plot"]
    si = pi["summary_plot"]
    folder_array = os.listdir(main_dir)
    for folder in folder_array:
        trial_dir = os.path.join(main_dir, folder)
        if os.path.isdir(trial_dir):
            signal_dir = os.path.join(trial_dir, "result", "signal.csv")
            trial_plot(ti, signal_dir)
    summary_plot(main_dir, si, is_sweep=False)
