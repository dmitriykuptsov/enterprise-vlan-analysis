set PATH=%PATH%;C:\Program Files\R\R-3.3.1\bin
call R --slave --args scanned_ports_cleaned_file.csv < plot_ports_histogram.R
call R --slave --args scanned_ports_cleaned_file.csv < open_ports_per_host_plot.R
call R --slave --args scanned_ports_cleaned_file.csv < bubble_plot.R