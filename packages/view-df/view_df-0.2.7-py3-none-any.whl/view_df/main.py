import pandas as pd
import webbrowser
import tempfile

def view_df(df: pd.DataFrame):
    """
    Converts the given DataFrame to an HTML file with auto-adjusted column widths,
    highlights rows and columns on click, and opens it in the default web browser.
    Includes multiple-column filtering functionality with checkboxes in each column header and a search box in the filter dropdown to search for specific options.
    
    Parameters:
    df (pd.DataFrame): The pandas DataFrame to display.
    """
    # Replace all unnamed columns or blank column names with actual blanks
    df.columns = [
        "" if str(col).startswith("Unnamed") or str(col).strip() == "" else col 
        for col in df.columns
    ]

    # Define custom CSS and JavaScript for filtering and highlighting
    css = """
    <style>
    table {
        border-collapse: collapse;
        border: 1px solid black;
    }
    th, td {
        padding: 8px;
        text-align: left;
        white-space: nowrap;
        border: 1px solid black; /* Cell borders */
    }
    th {
        background-color: #f2f2f2;
        position: sticky;
        top: 0;
        z-index: 1;
    }
    .highlight-row {
        background-color: #d3d3d3; /* Light gray for row highlight */
    }
    .highlight-column {
        background-color: #d3d3d3; /* Light gray for column highlight */
    }
    .filter-container {
        position: relative;
        display: inline-block;
    }
    .filter-dropdown {
        display: none;
        position: absolute;
        background-color: white;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
        overflow-y: auto;
        border: 1px solid black; /* Border for dropdown */
        resize: both; /* Enable resizing */
        min-width: 150px; /* Set a minimum width */
        min-height: 50px; /* Set a minimum height */
        max-height: 50vh; /* Set max height to half the screen height */
        z-index: 10;
        margin-top: 9px;
    }
    .filter-container {
        position: relative;
    }
    .filter-dropdown {
        left: 0;
    }
    .filter-container:hover .filter-dropdown {
        display: block;
    }
    th:last-child .filter-dropdown {
        right: 0;
        left: auto;
    }
    .filter-option {
        padding: 8px;
        cursor: pointer;
        white-space: nowrap;
        font-weight: normal;  /* Make the text normal, not bold */
        color: black;         /* Change the text color to black */
        font-size: 14px;     /* Increase font size for filter options */
    }
    .filter-option input {
        margin-right: 8px;
    }
    .filter-option:hover {
        background-color: #ddd;
    }
    .filter-arrow {
        font-size: 10px;     /* Decrease the font size */
        color: #b0b0b0; /* Lighter color */
        margin-left: 1px;
        cursor: pointer;
    }
    .clear-filters-button {
        margin: 10px 0;
        padding: 8px 12px;
        background-color: #808080;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .clear-filters-button:hover {
        background-color: #D3D3D3;
        color: #808080;
    }
    .search-box {
        padding-left: 10px;
        padding-top: 5px;
        width: 90%;
        border: white;
        border-radius: 4px;
        outline: none;
    }
    </style>

    <script>
    var originalData = [];
    var filters = {};
    var lastClickedRow = null;
    var lastClickedCol = null;

    function initializeTable() {
        var rows = document.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            var rowData = Array.from(row.children).map(function(cell) {
                return cell.innerHTML;
            });
            originalData.push(rowData);
        });
    }

    function applyFilters() {
        var tbody = document.querySelector('tbody');
        tbody.innerHTML= '';

        originalData.forEach(function(rowData, rowIdx) {
            var displayRow = true;

            for (var colIdx in filters) {
                if (filters[colIdx].length > 0 && !filters[colIdx].includes(rowData[colIdx])) {
                    displayRow = false;
                    break;
                }
            }

            if (displayRow) {
                var row = document.createElement('tr');
                rowData.forEach(function(cellData) {
                    var cell = document.createElement('td');
                    cell.innerHTML = cellData;
                    row.appendChild(cell);
                });
                tbody.appendChild(row);
            }
        });

    // Reapply highlights to the last clicked cell if it exists
    if (lastClickedRow !== null && lastClickedCol !== null) {
            highlight(lastClickedRow, lastClickedCol);
        }

    // Reattach event listeners to new table cells
    addClickListeners();
    }

    function updateFilter(colIdx) {
        var checkboxes = document.querySelectorAll('.filter-' + colIdx + ' input');
        filters[colIdx] = Array.from(checkboxes).filter(checkbox => checkbox.checked).map(checkbox => checkbox.value);
        applyFilters();
    }

    function clearFilters() {
        filters = {}; // Reset filters
        var checkboxes = document.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = false; // Uncheck all checkboxes
        });
        applyFilters(); // Reapply filters to show original data
    }

    function highlight(rowIdx, colIdx) {
        var rows = document.querySelectorAll('tr');
        var cols = document.querySelectorAll('td');

        // Reset all highlights
        rows.forEach(function(row) {
            row.classList.remove('highlight-row');
        });
        cols.forEach(function(col) {
            col.classList.remove('highlight-column');
        });

        // Highlight the selected row and column
        if (rowIdx !== null && colIdx !== null) {
            document.querySelectorAll('tr')[rowIdx].classList.add('highlight-row');
            document.querySelectorAll('td:nth-child(' + (colIdx + 1) + ')').forEach(function(cell) {
                cell.classList.add('highlight-column');
            });
        }
    }

    function addClickListeners() {
        // Add event listeners for highlighting
        var cells = document.querySelectorAll('td');
        
        cells.forEach(function(cell) {
            cell.addEventListener('click', function() {
                var rowIdx = cell.parentElement.rowIndex;
                var colIdx = cell.cellIndex;
                highlight(rowIdx, colIdx);
                lastClickedRow = rowIdx;
                lastClickedCol = colIdx;
            });
        });
    }
    
    function searchFilter(colIdx, searchValue) {
        var filterOptions = document.querySelectorAll('.filter-' + colIdx + ' .filter-option');
        searchValue = searchValue.toLowerCase();
        filterOptions.forEach(function(option) {
            var label = option.textContent || option.innerText;
            if (label.toLowerCase().indexOf(searchValue) > -1) {
                option.style.display = '';
            } else {
                option.style.display = 'none';
            }
        });
    }

    function toggleDropdown(colIdx) {
        var dropdown = document.querySelector('.filter-' + colIdx);
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
    }

    document.addEventListener('DOMContentLoaded', function() {
        initializeTable();
        filters = {};  // Initialize filter object for each column

        // Add initial click listeners
        addClickListeners();

        // Remove highlights when clicking outside of a cell
        document.addEventListener('click', function(event) {
            if (!event.target.closest('td')) {
                lastClickedRow = null;
                lastClickedCol = null;
                highlight(null, null); // Clear highlights
            }
        });
    });

    // Function to close all dropdowns
    function closeDropdowns() {
        var dropdowns = document.querySelectorAll('.filter-dropdown');
        dropdowns.forEach(function(dropdown) {
            dropdown.style.display = 'none';
    });
    }

    document.addEventListener('click', function(event) {
        // Close all dropdowns if the click is outside of any filter container
        if (!event.target.closest('.filter-container')) {
            closeDropdowns();
        }
    });

    function toggleDropdown(colIdx) {
        var dropdown = document.querySelector('.filter-' + colIdx);
        var isDisplayed = dropdown.style.display === 'block';
        
        // Close all dropdowns first
        closeDropdowns();
        
        // Toggle the current dropdown
        dropdown.style.display = isDisplayed ? 'none' : 'block';
    }

    // Function to check table width and set dropdown alignment for last column
    function adjustDropdownAlignment() {
        var table = document.querySelector('table');
        var lastColumn = document.querySelector('th:last-child .filter-dropdown');
        if (table.offsetWidth >= window.innerWidth) {
            // Align dropdown to left for the last column if table is 100% width
            lastColumn.style.right = '0';
            lastColumn.style.left = 'auto';
        } else {
            // Reset to default alignment (right)
            lastColumn.style.left = '0';
            lastColumn.style.right = 'auto';
        }
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        // Existing initialization code...
        adjustDropdownAlignment(); // Call the function to adjust alignment on load
    });

    window.addEventListener('resize', function() {
        adjustDropdownAlignment(); // Recheck on window resize
    });

    </script>
    """

    # Function to generate the HTML for filter dropdowns based on unique values in each column
    def generate_filter_html(column_values, col_idx):
        def make_hashable(item):
            """
            Convert unhashable types (like lists, sets, dicts) to hashable and serializable ones (like tuples).
            Handles nested structures like lists of dictionaries.
            """
            if isinstance(item, list):
                # Convert lists to tuples and tag them as lists
                return tuple(make_hashable(i) for i in item), 'list'
            elif isinstance(item, set):
                # Convert sets to tuples and tag them as sets
                return tuple(make_hashable(i) for i in item), 'set'
            elif isinstance(item, dict):
                # Convert dictionaries to sorted tuples of key-value pairs
                return tuple(sorted((k, make_hashable(v)) for k, v in item.items()))
            else:
                # Return the item as is if it's already hashable
                return item

        def safe_to_string(value):
            """
            Safely convert any value to a string for HTML display, handling cases like None, complex objects, etc.
            """
            try:
                if isinstance(value, tuple) and len(value) == 2:
                    # If this is a tagged value, handle it appropriately
                    if value[1] == 'list':
                        return str(list(value[0]))  # Convert back to list for display
                    elif value[1] == 'set':
                        return str(set(value[0]))  # Convert back to set for display
                return str(value) if value is not None else "None"
            except Exception as e:
                return f"Unrepresentable Value ({e})"

        def safe_sort(values):
            """
            Safely sort mixed types by converting non-string types to strings, ensuring that None and
            other uncomparable types do not cause sorting issues.
            """
            return sorted(values, key=lambda x: (x is not None, str(x)))

        try:
            # Filter out None values before sorting and ensure all column values are hashable
            unique_values = safe_sort(set(make_hashable(item) for item in column_values))
        except Exception as e:
            # Log or handle the error if something goes wrong during the uniqueness check
            print(f"Error generating unique values for column {col_idx}: {e}")
            unique_values = safe_sort(item for item in column_values if item is not None)  # Fallback to sorted values without uniqueness

        # Generate the filter HTML, ensuring each value is safely converted to a string for display
        filter_html = f'''
        <div class="filter-container">
            <span class="filter-arrow" onclick="toggleDropdown({col_idx})">&#9660;</span>
            <div class="filter-dropdown filter-{col_idx}">
                <input type="text" class="search-box" placeholder="Search..." onkeyup="searchFilter({col_idx}, this.value)">
        '''
        for value in unique_values:
            value_str = safe_to_string(value)
            filter_html += f'''
            <div class="filter-option">
            <label style="display: block; padding: 1px; cursor: pointer;"> 
        <input type="checkbox" value="{value_str}" onclick="updateFilter({col_idx});"> {value_str}
        </label>
        </div>
        '''
        filter_html += '</div></div>'
        
        return filter_html
    
    # Apply the custom formatting to each element in the DataFrame
    df_formatted = df.map(lambda x: '{:.9f}'.format(x).rstrip('0').rstrip('.') if isinstance(x, float) else x)
    
    # Start building the HTML table with filters
    html = '<button class="clear-filters-button" onclick="clearFilters()">Clear Filters</button><table><thead><tr>'
    
    # Add the column headers with filters
    for col_idx, col_name in enumerate(df_formatted.columns):
        filter_html = generate_filter_html(df_formatted[col_name], col_idx)
        html += f'<th>{col_name}<span class="filter-arrow">{filter_html}</span></th>'
    
    html += '</tr></thead><tbody>'
    
    # Add the rows
    for _, row in df_formatted.iterrows():
        html += '<tr>' + ''.join([f'<td>{cell}</td>' for cell in row]) + '</tr>'
    
    html += '</tbody></table>'
    
    # Combine CSS, JavaScript, and HTML
    html_with_css_js = css + html
    
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as temp_file:
        # Write the HTML with CSS and JavaScript to the temporary file
        temp_file.write(html_with_css_js)
        temp_file.flush()  # Ensure all data is written
        
        # Open the HTML file in the default web browser
        webbrowser.open('file://' + temp_file.name)

# Example usage
if __name__ == "__main__":
    data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Gender': ['Female', 'Male', 'Male'],
    'Occupation': ['Engineer', 'Doctor', 'Artist'],
    'Location': ['New York', 'Los Angeles', 'Chicago']
    }
    df = pd.DataFrame(data)
    view_df(df)