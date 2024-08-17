import pdfplumber
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import timedelta

# Folder path
pdf_folder = 'timetables/'

days_order = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]

def extract_data_from_pdf(pdf_path):
    data = []
    day = None
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text().split('\n')
            for line in text:
                if any(day_str in line for day_str in days_order):
                    day = line.split()[0]
                elif any(time_keyword in line for time_keyword in ["am", "pm"]):
                    if day:
                        time_data = line.split()
                        start_time = time_data[0] + ' ' + time_data[1]
                        end_time = time_data[2] + ' ' + time_data[3]
                        start_dt = pd.to_datetime(start_time, format='%I:%M %p')
                        end_dt = pd.to_datetime(end_time, format='%I:%M %p')
                        while start_dt < end_dt:
                            data.append([day, start_dt.strftime('%H:%M')])
                            start_dt += timedelta(minutes=30)
    return data

all_data = []
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        all_data.extend(extract_data_from_pdf(pdf_path))

df = pd.DataFrame(all_data, columns=['Day', 'Time Block'])

df['Day'] = pd.Categorical(df['Day'], categories=days_order, ordered=True)

time_blocks = pd.date_range("08:30", "22:30", freq="30min").strftime('%H:%M').tolist()

df['Time Block'] = pd.Categorical(df['Time Block'], categories=time_blocks, ordered=True)

heatmap_data = df.groupby(['Time Block', 'Day'], observed=True).size().unstack(fill_value=0)

plt.figure(figsize=(18, 20))

ax = sns.heatmap(
    heatmap_data,
    cmap='RdYlGn_r',
    annot=True,
    fmt="d",
    annot_kws={"size": 12},
    linewidths=.5,
    cbar_kws={"shrink": .75},
    yticklabels=time_blocks
)

ax.set_yticks(np.arange(len(time_blocks)))
ax.set_yticklabels(time_blocks, rotation=0)

plt.title('Student Presence Heatmap', fontweight='bold', fontsize='24', pad=36)
plt.ylabel('Time Block', fontsize=16, labelpad=24)
plt.xlabel('Day of the Week', fontsize=16, labelpad=24)
plt.savefig('heatmap_example.png')
plt.show()

heatmap_data.to_excel('weekly_schedule_heatmap.xlsx')
