# DataFrame Viewer

A Python module to display large pandas DataFrames with auto-adjusted column widths in a web browser with filtering capability and search option.

## Overview

DataFrame Viewer is a Python module designed to enhance the visualization of large pandas DataFrames by rendering them as interactive HTML tables in your default web browser. With features like auto-adjusted column widths, filtering capability with search option and cell highlighting, this tool significantly improves the readability and accessibility of your data.

## Features

- **Filtering Capabilities**: Easily filter data within the DataFrame for targeted analysis, with the option to clear filters, with search box.
- **Auto-Adjusted Column Widths**: Automatically adjusts column widths for better readability, making it easier to analyze large datasets.
- **Cell Highlighting**: Highlights the selected cell's entire row and column, improving data visibility and navigation.
- **HTML Rendering**: Displays DataFrames in a beautifully formatted HTML table, enhancing user experience.
- **No Disk Writes**: Operates using temporary files that are automatically deleted after viewing, ensuring your data remains secure.
## Installation

1. **Install directly**:
    ```bash
    pip install view_df
    ```
### or
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/TheKola/dataframe-viewer.git
   ```
2. **Navigate to the Project Directory**:
    ```bash
    cd dataframe-viewer
    ```
3. **Copy the file `view_df.py` to your project folder**
## Usage

1. Import the Module:
    ```bash
    from view_df import view_df
2. Create a DataFrame and view it:
    ```bash
    import pandas as pd
    from view_df import view_df

    # Example DataFrame
     data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Gender':['Female','Male','Male'],
    'Occupation': ['Engineer', 'Doctor', 'Artist'],
    'Location': ['New York', 'Los Angeles', 'Chicago']
    }
    df = pd.DataFrame(data)

    # View the DataFrame in a web browser
    view_df(df)

## Output
   <p align="center">
  <img src="example_output.png" width="100%" title="hover text">
</p>

## Release Notes
**v 0.2.8** Added button to clear filters in individual columns.\
v 0.2.7 Resolved issues with filter menu overflowing out of the screen for last column in case of large tables.\
v 0.2.6 Added search box in the filter menu to help easily search from a lot of data.\
v 0.2.3 Sorted the issue with filter menu, was not able to differentiate between list and tuple data types.\
v 0.2.2: Sorted the issue with "None" datatypes, was causing issue when creating filters.\
v 0.2.1: Sorted the issue with cells containing lists, dictonary, sets.\
v 0.2: Introduced filtering capabilities and the option to clear filters for a more interactive experience.\
v 0.1.3: Implemented minor formatting changes for improved aesthetics.\
v 0.1.2: Added cell highlighting feature to enhance data visibility.\
v 0.1: Initial release - Displaying DataFrame in web browser.

## Contributing
Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more details.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
