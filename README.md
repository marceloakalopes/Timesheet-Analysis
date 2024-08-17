# Student Presence Heatmap Analysis

## Problem Statement

The goal of this project was to analyze timesheet data from various programs at Sault College to determine the peak hours when the most students are present on campus simultaneously. The timesheets are provided in PDF format and contain varying structures. The final output should be a heatmap that visually represents student presence across different time blocks throughout the week, with color coding to indicate low, medium, and high student density.

## Approach

### 1. **Data Extraction:**
   - The timesheets are provided in PDF format, each containing the schedule for different programs at the college.
   - We used `pdfplumber` to extract relevant data such as day of the week, start time, end time, and course information from the PDFs.
   - The data extraction function loops through each PDF, identifying the day of the week and the time intervals during which classes are held.

### 2. **Data Processing:**
   - The extracted data is structured into a pandas DataFrame with columns for `Day` and `Time Block`.
   - To accurately reflect student presence, every 30-minute interval between the start and end times of each class is recorded.
   - A categorical column is used to ensure the days of the week and time blocks are ordered correctly.

### 3. **Heatmap Generation:**
   - We created a list of all possible 30-minute time blocks in a day (e.g., from 08:00 to 22:30).
   - The data is then grouped and counted to generate a heatmap, where each cell represents a 30-minute interval for a specific day.
   - A heatmap is generated using `seaborn`, with color coding to represent the density of students during each interval.

### 4. **Alignment Issues:**
   - A key challenge was ensuring that the Y-axis labels (time blocks) were correctly aligned with the start of each cell on the heatmap.
   - By setting precise Y-tick positions using `np.arange(len(time_blocks))`, we ensured that the time labels align perfectly with the start of each corresponding cell.

### 5. **Final Output:**
   - The final heatmap clearly shows the distribution of student presence across the week.
   - The output is saved as a PNG image and also exported to an Excel file for further analysis.

## How to Run the Code

### Prerequisites

Ensure you have the following Python packages installed:

```bash
pip install pdfplumber pandas seaborn matplotlib numpy
```

### Running the Code

1. **Place the Timesheets in the Folder:**
   - Place all the timesheet PDFs in a folder named `timesheets`.

2. **Run the Script:**
   - Use the provided script to extract data and generate the heatmap.

   ```python
   python your_script_name.py
   ```

3. **View the Results:**
   - The script will generate a `heatmap.png` file and save it in the working directory.
   - An Excel file `weekly_schedule_heatmap.xlsx` will also be created with the heatmap data.

### Code Explanation

The key components of the code are:

- **Data Extraction:**
  - The `extract_data_from_pdf` function processes each PDF file and extracts the relevant schedule data.

- **Data Structuring:**
  - The extracted data is stored in a pandas DataFrame, where each row represents a 30-minute interval during which a class is in session.

- **Heatmap Generation:**
  - The data is aggregated and visualized using a heatmap, with adjustments to ensure that time blocks align correctly with the cells.

- **Y-Axis Alignment:**
  - Special care is taken to ensure that the time labels on the Y-axis align with the start of each cell, enhancing readability.

## Example Output

The generated heatmap visually represents student presence, with the time blocks aligned correctly on the Y-axis and days on the X-axis. Each cell corresponds to a 30-minute interval, color-coded to reflect the number of students present.
g this `README.md`, users can understand the problem, the steps taken to solve it, and how to run the code to replicate the analysis. Feel free to customize the content further based on your needs!