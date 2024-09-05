import pdfplumber
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import timedelta

# Folder path containing the PDF files
pdf_folder = 'timetables'

# Order of days for sorting purposes
days_order = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]

# List to store program names
programs_included = []


def extract_data_from_pdf(pdf_path):
    """
    Extracts time block data from a given PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: A list of lists containing the day and time block.
    """
    data = []
    day = None
    with pdfplumber.open(pdf_path) as pdf:
        # Add the program name to the list (from the file name or from the PDF)
        program_name = os.path.basename(pdf_path).replace('.pdf', '')
        programs_included.append(program_name)

        for page in pdf.pages:
            text = page.extract_text().split('\n')
            for line in text:
                # Check if the line contains a day of the week
                if any(day_str in line for day_str in days_order):
                    day = line.split()[0]
                # Check if the line contains time information
                elif any(time_keyword in line for time_keyword in ["am", "pm"]):
                    if day:
                        time_data = line.split()
                        start_time = time_data[0] + ' ' + time_data[1]
                        end_time = time_data[2] + ' ' + time_data[3]
                        start_dt = pd.to_datetime(start_time, format='%I:%M %p')
                        end_dt = pd.to_datetime(end_time, format='%I:%M %p')
                        # Append time blocks in 30-minute intervals
                        while start_dt < end_dt:
                            data.append([day, start_dt.strftime('%H:%M')])
                            start_dt += timedelta(minutes=30)
    return data


# List to hold all extracted data
all_data = []

# Iterate over all PDF files in the specified folder
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        all_data.extend(extract_data_from_pdf(pdf_path))

# Calculate the total number of programs
total_programs = len(programs_included)

# Create a DataFrame from the extracted data
df = pd.DataFrame(all_data, columns=['Day', 'Time Block'])

# Set the 'Day' column as a categorical type with a specific order
df['Day'] = pd.Categorical(df['Day'], categories=days_order, ordered=True)

# Generate a list of time blocks in 30-minute intervals from 08:30 to 22:30
time_blocks = pd.date_range("08:30", "22:30", freq="30min").strftime('%H:%M').tolist()

# Set the 'Time Block' column as a categorical type with a specific order
df['Time Block'] = pd.Categorical(df['Time Block'], categories=time_blocks, ordered=True)

# Create a pivot table for the heatmap data
heatmap_data = df.groupby(['Time Block', 'Day'], observed=True).size().unstack(fill_value=0)

# Set the figure size for the heatmap
plt.figure(figsize=(18, 20))

# Create the heatmap
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

# Set y-ticks and labels
ax.set_yticks(np.arange(len(time_blocks)))
ax.set_yticklabels(time_blocks, rotation=0)

# Set the title and labels for the heatmap
plt.title('Classes Heatmap', fontweight='bold', fontsize='24', pad=36)
plt.ylabel('Time Block', fontsize=16, labelpad=24)
plt.xlabel('Day of the Week', fontsize=16, labelpad=24)

# Add annotations for colorbar
cbar = ax.collections[0].colorbar
cbar.ax.set_ylabel('Number of Programs having Classes', fontsize=12, labelpad=12)


# Add population sample size at the bottom of the heatmap
plt.text(
    1.1, -0.05, f"Population sample: {total_programs} programs",
    horizontalalignment='center',
    verticalalignment='center',
    fontsize=12,
    transform=ax.transAxes
)

# Save the heatmap as a PNG file
plt.savefig('heatmap_example.png')

# Display the heatmap
plt.show()

# Save the heatmap data to an Excel file
with pd.ExcelWriter('weekly_schedule_heatmap_example.xlsx') as writer:
    heatmap_data.to_excel(writer, sheet_name='Heatmap Data')
    # Write the list of programs included
    pd.DataFrame(programs_included, columns=['Included Programs']).to_excel(writer, sheet_name='Programs Included')

print(f"Heatmap and Excel file saved successfully. Total programs: {total_programs}")
