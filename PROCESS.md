# Process

## Tools

I used VS Code and its terminal to edit and run Python scripts, uv to run scripts with their declared dependencies, and Git/GitHub to record and publish the stages. Requests saved the Hong Kong Observatory CSV, while Python's csv and datetime modules read dates and times. Matplotlib produced the image.

ChatGPT helped me choose a machine-readable source, write most of the first plotting code, and understand terminal and Git messages. Codex helped revise the plot and draft these documents. I selected the scatter-plot direction and dark palette. The code was checked against the actual CSV: the columns are `YYYY-MM-DD`, `RISE`, `TRAN.` and `SET`, rather than the initially suggested year/month/day columns.

## Kept

I kept daily scatter points because joining the times across midnight would create misleading long lines. Missing events stay as gaps rather than being replaced with zero or guessed. The final version keeps the original data and gives each event a separate colour. Month labels and clock labels make the chart easier to read, and the dark background supports the night-sky direction I chose.

## Rejected

I originally wanted moon-phase data. The downloaded HKO moon-phase HTML contained the page shell rather than the desired table, and an attempted large almanac PDF download ended before completion. I rejected that route and used HKO's small, machine-readable moonrise/transit/moonset CSV instead. This changed the phenomenon being plotted, so the final description avoids calling event-time data moon phases.

I also replaced the first plot's numeric day-of-year labels and default styling with months and the chosen dark palette. The revised script saves and closes the figure rather than waiting at `plt.show()`, which previously kept the terminal occupied until the chart window was closed.
