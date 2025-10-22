import pandas as pd
import json


def generate_property_form(df):
    """
    Generate an HTML form for selecting propertyaltlabel and displaying filtered results in a styled DataTable.

    Parameters:
        df (pd.DataFrame): DataFrame with SPARQL query results.

    Returns:
        str: HTML string for the form and DataTable.
    """
    # Prepare data for JavaScript
    data = df.to_dict(orient="records")  # List of row dictionaries
    unique_properties = sorted(df["propertyaltlabel"].dropna().unique().tolist())

    # Generate HTML with embedded data using str.format
    html_template = """
<link rel='stylesheet' type='text/css' href='https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css'>
<link rel='stylesheet' type='text/css' href='https://cdn.datatables.net/buttons/2.2.2/css/buttons.dataTables.min.css'>
<script src='https://code.jquery.com/jquery-3.5.1.js'></script>
<script src='https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js'></script>
<script src='https://cdn.datatables.net/buttons/2.2.2/js/dataTables.buttons.min.js'></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js'></script>
<script src='https://cdn.datatables.net/buttons/2.2.2/js/buttons.html5.min.js'></script>

<div class="form-container">
    <h3>Select Property</h3>
    <select class="property-select" id="property-select" onchange="updateTable()">
        <option value="">-- Select a property --</option>
        <!-- Populated dynamically -->
    </select>
    <div id="table-output" style="margin-top: 20px;">
        <table id="observations_table" class="display" style="width:100%">
            <thead><tr></tr></thead>
            <tbody></tbody>
        </table>
    </div>
</div>

<style>
    .form-container {{
        max-width: 1000px;
        margin: 20px auto;
        font-family: Arial, sans-serif;
    }}
    .property-select {{
        width: 100%;
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 4px;
        margin-bottom: 20px;
    }}
    table.display {{
        width: 100% !important;
        border-collapse: collapse;
    }}
    div.dt-buttons {{
        margin-bottom: 15px;
    }}
    #observations_table th, #observations_table td {{
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
        font-size: 14px;
        word-wrap: break-word;
        max-width: 200px;
    }}
    #observations_table th {{
        background-color: #f5f5f5;
        font-weight: bold;
    }}
    #observations_table td {{
        background-color: #fff;
    }}
    .dataTables_wrapper .dataTables_filter input {{
        border: 1px solid #ccc;
        padding: 5px;
        margin-bottom: 10px;
    }}
    .dataTables_wrapper .dataTables_paginate .paginate_button {{
        padding: 5px 10px;
        margin: 0 2px;
        border: 1px solid #ccc;
        border-radius: 3px;
    }}
</style>

<script>
    // Data from Python
    const data = {data_json};
    const uniqueProperties = {properties_json};

    // Populate the select options
    const select = document.getElementById('property-select');
    uniqueProperties.forEach(prop => {{
        const option = document.createElement('option');
        option.value = prop;
        option.text = prop;
        select.appendChild(option);
    }});

    // Initialize DataTable
    let dataTable;
    function initializeDataTable() {{
        if (dataTable) {{
            dataTable.clear().destroy();
        }}
        dataTable = $('#observations_table').DataTable({{
            dom: 'Bfrtip',
            buttons: ['csv', 'excel'],
            pageLength: 10,
            searching: true,
            ordering: true,
            destroy: true,
            scrollX: true,
            language: {{
                emptyTable: "No data available. Select a property to display data."
            }}
        }});
        // Debug: Verify table ID
        console.log('DataTable initialized for:', document.getElementById('observations_table'));
    }}

    // Call initializeDataTable after document is ready
    $(document).ready(function() {{
        console.log('Document ready, initializing DataTable');
        initializeDataTable();
    }});

    // Update table based on selection
    function updateTable() {{
        const selectedProperty = select.value;
        const output = document.getElementById('table-output');
        console.log('Updating table for property:', selectedProperty);

        // Clear and reinitialize table if no property selected
        if (!selectedProperty) {{
            output.innerHTML = '<table id="observations_table" class="display" style="width:100%"><thead><tr></tr></thead><tbody></tbody></table>';
            console.log('No property selected, set empty table with ID observations_table');
            initializeDataTable();
            return;
        }}

        // Filter data
        const filteredData = data.filter(row => row.propertyaltlabel === selectedProperty);
        
        // Store selection
        window.selectedProperty = selectedProperty;
        window.filteredData = filteredData;
        localStorage.setItem('selectedProperty', selectedProperty);
        localStorage.setItem('filteredData', JSON.stringify(filteredData));
        console.log('Selected property and data stored:', selectedProperty, filteredData);

        // Generate table HTML with observations_table ID
        if (filteredData.length === 0) {{
            output.innerHTML = '<table id="observations_table" class="display" style="width:100%"><thead><tr></tr></thead><tbody></tbody></table>';
            console.log('No data for selected property, set empty table with ID observations_table');
            initializeDataTable();
            return;
        }}

        const headers = Object.keys(filteredData[0]);
        let tableHTML = '<table id="observations_table" class="display" style="width:100%"><thead><tr>';
        headers.forEach(header => {{
            tableHTML += `<th>${{header}}</th>`;
        }});
        tableHTML += '</tr></thead><tbody>';
        filteredData.forEach(row => {{
            tableHTML += '<tr>';
            headers.forEach(header => {{
                tableHTML += `<td>${{row[header] || ''}}</td>`;
            }});
            tableHTML += '</tr>';
        }});
        tableHTML += '</tbody></table>';
        output.innerHTML = tableHTML;
        console.log('Table HTML set with ID observations_table:', tableHTML);

        // Reinitialize DataTable
        initializeDataTable();

        // Notify other scripts
        window.dispatchEvent(new Event('filteredDataUpdated'));
    }}
</script>
    """
    return html_template.format(
        data_json=json.dumps(data), properties_json=json.dumps(unique_properties)
    )
