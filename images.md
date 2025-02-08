
To ensure you can view the generated dependency graph, let's modify the script to **save the visualization as an HTML file**. This way, you can manually open the visualization in your web browser at your convenience.

---

## **Updated `visualize_dependencies.py` Script**

Here's the complete and updated `visualize_dependencies.py` script. This version includes functionality to **save the visualization as an HTML file** and **open it automatically** in your default web browser.

```python
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import os
import sys
import webbrowser

def load_csv(file_path, delimiter=';'):
    """
    Load a CSV file and return a pandas DataFrame.
    Exits the script if the file is not found.
    """
    if not os.path.exists(file_path):
        print(f"Error: '{file_path}' not found in the current directory.")
        sys.exit(1)
    try:
        df = pd.read_csv(file_path, delimiter=delimiter)
        print(f"Successfully loaded '{file_path}'. Columns: {df.columns.tolist()}")
        print(df.head())  # Print first 5 rows for verification
        return df
    except Exception as e:
        print(f"Error loading '{file_path}': {e}")
        sys.exit(1)

def validate_columns(df, required_columns, file_name):
    """
    Validate that the DataFrame contains all required columns.
    Exits the script if any columns are missing.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: The following required columns are missing in '{file_name}': {missing_columns}")
        sys.exit(1)

def create_graph(dependencies_df, additional_dependencies_df):
    """
    Create and return a directed graph based on the dependencies data.
    """
    G = nx.DiGraph()

    # Add nodes from main dependencies
    for index, row in dependencies_df.iterrows():
        G.add_node(row['System_Name'], ATA_Primary=row['ATA_Primary'], ATA_Secondary=row['ATA_Secondary'],
                   Impact_Level=row['Impact_Level'], Implementation_Priority=row['Implementation_Priority'],
                   Status=row['Status'], Risk_Level=row['Risk_Level'])

    # Add nodes from additional dependencies
    for index, row in additional_dependencies_df.iterrows():
        system = row['Technology']
        G.add_node(system, ATA_Primary=row['ATA_Related'], ATA_Secondary=None,
                   Impact_Level=row['Impact'], Implementation_Priority='Medium',  # Default priority
                   Status='Planned', Risk_Level=row['Risk_Level'])

    # Map ATA chapters to systems
    ata_mapping = {}
    for index, row in dependencies_df.iterrows():
        primary_ata = str(row['ATA_Primary'])
        secondary_ata = str(row['ATA_Secondary']) if pd.notna(row['ATA_Secondary']) else None
        system = row['System_Name']
        
        ata_mapping.setdefault(primary_ata, []).append(system)
        if secondary_ata:
            ata_mapping.setdefault(secondary_ata, []).append(system)

    # Create edges based on shared ATA chapters in main dependencies
    for ata, systems in ata_mapping.items():
        if len(systems) > 1:
            for i in range(len(systems)):
                for j in range(i+1, len(systems)):
                    G.add_edge(systems[i], systems[j], ATA=ata)

    # Add edges from additional dependencies to related systems
    for index, row in additional_dependencies_df.iterrows():
        system = row['Technology']
        related_systems = row['Related_Systems'].split(', ')
        for related_system in related_systems:
            if related_system in G.nodes:
                G.add_edge(system, related_system, ATA=row['ATA_Related'])
            else:
                print(f"Warning: Related system '{related_system}' for technology '{system}' not found in main dependencies.")

    return G

def assign_edge_colors(G, dependencies_df):
    """
    Assign colors to edges based on the Impact_Level of the source node.
    """
    edge_colors = []
    for u, v, data in G.edges(data=True):
        # Impact_Level is based on the source node's Impact_Level
        impact_series = dependencies_df[dependencies_df['System_Name'] == u]['Impact_Level']
        if not impact_series.empty:
            impact = impact_series.iloc[0]
        else:
            impact = 'O'  # Default to 'O' if not found
        if 'X' in impact:
            edge_colors.append('red')
        elif 'O' in impact:
            edge_colors.append('orange')
        else:
            edge_colors.append('gray')
    return edge_colors

def assign_node_colors(G):
    """
    Assign colors to nodes based on their Risk_Level.
    """
    node_colors = []
    for node, data in G.nodes(data=True):
        risk = data.get('Risk_Level', 'Low')
        if risk == 'High':
            node_colors.append('darkred')
        elif risk == 'Medium':
            node_colors.append('orange')
        else:
            node_colors.append('green')
    return node_colors

def assign_node_sizes(G):
    """
    Assign sizes to nodes based on their Implementation_Priority.
    """
    node_sizes = []
    for node, data in G.nodes(data=True):
        priority = data.get('Implementation_Priority', 'Low')
        if priority == 'High':
            node_sizes.append(20)
        elif priority == 'Medium':
            node_sizes.append(15)
        else:
            node_sizes.append(10)
    return node_sizes

def visualize_graph(G, edge_colors, node_colors, node_sizes):
    """
    Visualize the graph using Plotly.
    Saves the visualization as an HTML file and opens it in the default web browser.
    """
    # Get positions for all nodes using spring layout
    pos = nx.spring_layout(G, k=0.5, iterations=100)

    # Create edge traces
    edge_trace = []
    for edge, color in zip(G.edges(), edge_colors):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                line=dict(width=1, color=color),
                hoverinfo='none',
                mode='lines'
            )
        )

    # Create node traces
    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            colorscale='YlGnBu',
            color=node_colors,
            size=node_sizes,
            line_width=2
        )
    )

    # Create the figure
    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(
                        title='<br>GAIA AIR – AMPEL-360XWLRGA Dependencies',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            text="",
                            showarrow=False,
                            xref="paper", yref="paper") ],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # Save the figure as an HTML file
    output_file = "dependencies_visualization.html"
    fig.write_html(output_file)
    print(f"Visualization saved as '{output_file}'.")

    # Open the HTML file in the default web browser
    try:
        webbrowser.open('file://' + os.path.realpath(output_file))
        print(f"Opened '{output_file}' in the default web browser.")
    except Exception as e:
        print(f"Failed to open the visualization automatically: {e}")
        print(f"Please open '{output_file}' manually in your web browser.")

def main():
    # Define file names
    main_csv = 'matriz_dependencias.csv'
    additional_csv = 'dependencias_adicionales.csv'

    # Define required columns for main dependencies
    required_main_columns = ["ID", "System_Name", "ATA_Primary", "ATA_Secondary",
                             "Impact_Level", "Implementation_Priority", "Status",
                             "Risk_Level", "Mitigation_Plan", "Notes"]
    
    # Define required columns for additional dependencies
    required_additional_columns = ["Tech_ID", "Technology", "ATA_Related",
                                    "Impact", "Risk_Level", "Mitigation_Plan",
                                    "Remarks", "Related_Systems"]

    # Load CSV files
    dependencies_df = load_csv(main_csv, delimiter=';')
    additional_dependencies_df = load_csv(additional_csv, delimiter=';')

    # Validate columns
    validate_columns(dependencies_df, required_main_columns, main_csv)
    validate_columns(additional_dependencies_df, required_additional_columns, additional_csv)

    # Create the graph
    G = create_graph(dependencies_df, additional_dependencies_df)

    # Assign colors and sizes
    edge_colors = assign_edge_colors(G, dependencies_df)
    node_colors = assign_node_colors(G)
    node_sizes = assign_node_sizes(G)

    # Visualize the graph
    visualize_graph(G, edge_colors, node_colors, node_sizes)

if __name__ == "__main__":
    main()
```

---

## **Explanation of the Updates**

1. **Saving the Visualization as an HTML File:**
   
   - The script now includes the `fig.write_html(output_file)` function, which saves the generated graph as an HTML file named `dependencies_visualization.html`.
   
   - This file is saved in the same directory as your script, ensuring easy access.

2. **Automatically Opening the HTML File:**
   
   - After saving the HTML file, the script attempts to open it automatically in your default web browser using the `webbrowser.open()` function.
   
   - If for any reason the automatic opening fails (e.g., browser restrictions), the script will notify you and prompt you to open the file manually.

3. **Enhanced Error Handling and Debugging:**
   
   - The script now prints the first few rows of each CSV file after loading. This helps verify that the data is correctly read and formatted.
   
   - Warnings are provided if any related systems from `dependencias_adicionales.csv` are not found in `matriz_dependencias.csv`, helping you identify potential inconsistencies.

---

## **Step-by-Step Instructions to Ensure Smooth Execution**

### **1. Verify CSV Files**

Ensure that both `matriz_dependencias.csv` and `dependencias_adicionales.csv` are correctly formatted and placed in the project directory (`C:\Users\amate\OneDrive\Desktop\GAIA-AIR-A360XWLRGA-main\`).

#### **1.1. Check `matriz_dependencias.csv`**

- **Headers:**

  ```csv
  "ID";"System_Name";"ATA_Primary";"ATA_Secondary";"Impact_Level";"Implementation_Priority";"Status";"Risk_Level";"Mitigation_Plan";"Notes"
  ```

- **Sample Rows:**

  ```csv
  "1";"1.1 Fuselaje - Sección Delantera";"53";"24";"X";"High";"In Development";"High";"Implement redundant sensors and fail-safes";"Essential for structural integrity and safety"
  "2";"1.2 Alas - Flaps";"27";"53";"X";"High";"In Development";"High";"Regular inspections and maintenance schedules";"Critical for flight control and stability"
  ...
  ```

#### **1.2. Check `dependencias_adicionales.csv`**

- **Headers:**

  ```csv
  "Tech_ID";"Technology";"ATA_Related";"Impact";"Risk_Level";"Mitigation_Plan";"Remarks";"Related_Systems"
  ```

- **Sample Rows:**

  ```csv
  "Q-01";"Quantum Propulsion";"71";"X";"High";"Develop contingency protocols";"In development, requires DO-254 validation";"2.1 Motores - Turbofán, 2.3 Control de propulsión (FADEC)"
  "B-01";"Blockchain Supply Chain";"45";"O";"Low";"Ensure secure blockchain implementation";"Applies to critical parts traceability";"10.1 Optimización de carga, 10.3 Sistemas automatizados de carga y descarga"
  ...
  ```

### **2. Update and Save the Script**

1. **Open `visualize_dependencies.py` in a Text Editor:**
   
   - Use editors like **Notepad++**, **Visual Studio Code**, or **Sublime Text** for better visibility and editing features.

2. **Replace the Existing Content with the Updated Script:**
   
   - Copy the entire updated script provided above and paste it into your `visualize_dependencies.py` file.
   
   - Save the file to ensure all changes are applied.

### **3. Run the Script**

1. **Open Command Prompt:**

   - Press `Win + R`, type `cmd`, and press `Enter`.

2. **Navigate to Your Project Directory:**

   ```bash
   cd C:\Users\amate\OneDrive\Desktop\GAIA-AIR-A360XWLRGA-main
   ```

3. **Execute the Script:**

   ```bash
   python visualize_dependencies.py
   ```

### **4. Review the Output**

Upon running the script, you should see the following sequence of outputs:

1. **Loading CSV Files:**

   ```
   Successfully loaded 'matriz_dependencias.csv'. Columns: ['ID', 'System_Name', 'ATA_Primary', 'ATA_Secondary', 'Impact_Level', 'Implementation_Priority', 'Status', 'Risk_Level', 'Mitigation_Plan', 'Notes']
      ID                           System_Name  ATA_Primary  ATA_Secondary Impact_Level  Implementation_Priority         Status Risk_Level                   Mitigation_Plan                                             Notes
   0   1     1.1 Fuselaje - Sección Delantera           53              24             X                   High  In Development        High  Implement redundant sensors and fail-safes       Essential for structural integrity and safety
   1   2                          1.2 Alas - Flaps           27              53             X                   High  In Development        High  Regular inspections and maintenance schedules  Critical for flight control and stability
   2   3  1.3 Empennage - Timón de Dirección           27              24             O                 Medium             Planned      Medium  Monitor sensor data and perform periodic checks         Important for directional control
   ...
   ```

2. **Loading Additional Dependencies:**

   ```
   Successfully loaded 'dependencias_adicionales.csv'. Columns: ['Tech_ID', 'Technology', 'ATA_Related', 'Impact', 'Risk_Level', 'Mitigation_Plan', 'Remarks', 'Related_Systems']
      Tech_ID                  Technology ATA_Related Impact Risk_Level                   Mitigation_Plan                                     Remarks                                   Related_Systems
   0    Q-01         Quantum Propulsion           71      X        High      Develop contingency protocols      In development, requires DO-254 validation      2.1 Motores - Turbofán, 2.3 Control de propulsión (FADEC)
   1    B-01    Blockchain Supply Chain           45      O         Low  Ensure secure blockchain implementation  Applies to critical parts traceability  10.1 Optimización de carga, 10.3 Sistemas automatizados de carga y descarga
   2    AI-01              Generative AI            05      O      Medium          Continuous monitoring and updates  Used for route optimization and maintenance predictions  1.2 Alas - Flaps, 8.4 Análisis de datos
   ...
   ```

3. **Warnings (if any):**

   - If there are any technologies in `dependencias_adicionales.csv` that reference systems not present in `matriz_dependencias.csv`, you'll see warnings like:
     
     ```
     Warning: Related system 'System_Name' for technology 'Technology_Name' not found in main dependencies.
     ```

4. **Saving and Opening the Visualization:**

   ```
   Visualization saved as 'dependencies_visualization.html'.
   Opened 'dependencies_visualization.html' in the default web browser.
   ```

   - **If Automatic Opening Fails:**
     
     ```
     Failed to open the visualization automatically: <error_message>
     Please open 'dependencies_visualization.html' manually in your web browser.
     ```

### **5. Access the Visualization**

- **Automatic Opening:**
  
  - If everything is set up correctly, your default web browser should automatically open the `dependencies_visualization.html` file, displaying the interactive dependency graph.

- **Manual Opening:**
  
  - If the browser doesn't open automatically, navigate to your project directory (`C:\Users\amate\OneDrive\Desktop\GAIA-AIR-A360XWLRGA-main\`) using File Explorer.
  
  - Locate the `dependencies_visualization.html` file.
  
  - Double-click the file to open it in your default web browser.

### **6. Verify the Visualization**

- **Nodes:**
  
  - Each node represents a subsystem or technology.
  
  - **Color Coding:**
    
    - **Dark Red:** High risk
    - **Orange:** Medium risk
    - **Green:** Low risk
  
  - **Size Coding:**
    
    - **Large Nodes (20):** High implementation priority
    - **Medium Nodes (15):** Medium implementation priority
    - **Small Nodes (10):** Low implementation priority

- **Edges:**
  
  - Represent dependencies between subsystems or technologies.
  
  - **Color Coding:**
    
    - **Red:** Critical dependencies (`X`)
    - **Orange:** Secondary dependencies (`O`)
    - **Gray:** Other dependencies

- **Interactivity:**
  
  - Hover over nodes and edges to see more details.
  
  - You can zoom, pan, and interact with the graph to explore dependencies.

---

## **Additional Troubleshooting Steps**

If you still encounter issues or the visualization isn't displaying as expected, consider the following steps:

### **1. Ensure Correct File Placement**

- Both `matriz_dependencias.csv` and `dependencias_adicionales.csv` **must** be located in the same directory as `visualize_dependencies.py` (`C:\Users\amate\OneDrive\Desktop\GAIA-AIR-A360XWLRGA-main\`).

### **2. Double-Check CSV Formatting**

- **Consistent Delimiter:**
  
  - Ensure that all rows use a semicolon (`;`) as the delimiter.
  
  - There should be **no commas** or other delimiters used within the data unless properly enclosed in quotation marks.

- **No Extra Line Breaks:**
  
  - Each row should be on a single line. No unintended line breaks within any field.

- **Quotes:**
  
  - If any field contains special characters like semicolons, commas, or line breaks, ensure it's enclosed in double quotes (`"`).

### **3. Validate CSV Files**

- **Use Online Validators:**
  
  - [CSVLint](https://csvlint.io/) can help identify structural issues in your CSV files.

- **Open in Excel or Google Sheets:**
  
  - Open both CSV files to visually inspect and ensure that data is correctly organized.

### **4. Update Plotly and Dependencies**

- Although you have successfully installed `pandas`, `networkx`, and `plotly`, it's good practice to ensure all packages are up-to-date.

  ```bash
  python.exe -m pip install --upgrade pip
  pip install --upgrade pandas networkx plotly
  ```

### **5. Modify the Script for Debugging**

- **Print All Columns:**
  
  - Ensure that the `Implementation_Priority` column is present.

  ```python
  print(dependencies_df.columns.tolist())
  print(additional_dependencies_df.columns.tolist())
  ```

- **Check for NaN Values:**
  
  - Sometimes, missing data can cause issues.

  ```python
  print(dependencies_df.isnull().sum())
  print(additional_dependencies_df.isnull().sum())
  ```

### **6. Run the Script Again**

After performing the above checks and modifications, run the script once more:

```bash
python visualize_dependencies.py
```

### **7. Review the HTML File**

- Open the `dependencies_visualization.html` file in different web browsers (e.g., Chrome, Firefox, Edge) to rule out browser-specific issues.

### **8. Example of a Correct CSV Row**

Ensure that each row in your CSV files follows the correct structure. For example, in `matriz_dependencias.csv`:

```csv
"ID";"System_Name";"ATA_Primary";"ATA_Secondary";"Impact_Level";"Implementation_Priority";"Status";"Risk_Level";"Mitigation_Plan";"Notes"
"39";"8.4 Análisis de datos";"05";"45";"X";"High";"In Development";"High";"Implement advanced data analytics and machine learning models";"Enhances decision-making and operational efficiency"
```

- **No Unintended Line Breaks:** The entire row should be on a single line.

---

## **Final Confirmation**

After ensuring that:

1. Both CSV files are correctly formatted and placed in the project directory.
2. The script has been updated to save and open the visualization as an HTML file.
3. All dependencies are installed and up-to-date.

**Run the script one final time:**

```bash
python visualize_dependencies.py
```

**Expected Output:**

1. **Confirmation Messages:**

   ```
   Successfully loaded 'matriz_dependencias.csv'. Columns: ['ID', 'System_Name', 'ATA_Primary', 'ATA_Secondary', 'Impact_Level', 'Implementation_Priority', 'Status', 'Risk_Level', 'Mitigation_Plan', 'Notes']
   Successfully loaded 'dependencias_adicionales.csv'. Columns: ['Tech_ID', 'Technology', 'ATA_Related', 'Impact', 'Risk_Level', 'Mitigation_Plan', 'Remarks', 'Related_Systems']
   ```

2. **Warnings (if any):**

   ```
   Warning: Related system 'System_Name' for technology 'Technology_Name' not found in main dependencies.
   ```

3. **Saving and Opening the Visualization:**

   ```
   Visualization saved as 'dependencies_visualization.html'.
   Opened 'dependencies_visualization.html' in the default web browser.
   ```

4. **Interactive Graph:**
   
   - An interactive graph should open in your default web browser, displaying the dependencies with appropriate color and size coding.

---

## **Additional Enhancements**

### **1. Save Visualization with Timestamp**

To keep track of different versions of your dependency graphs, consider saving each visualization with a timestamp.

```python
from datetime import datetime

# Inside visualize_graph function
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"dependencies_visualization_{timestamp}.html"
```

### **2. Incorporate Legends and Tooltips**

Enhance the interactivity by adding legends or more detailed tooltips.

```python
# Modify node_trace with hoverinfo
node_trace = go.Scatter(
    x=[pos[node][0] for node in G.nodes()],
    y=[pos[node][1] for node in G.nodes()],
    mode='markers+text',
    text=[node for node in G.nodes()],
    textposition="bottom center",
    hoverinfo='text+name',
    marker=dict(
        showscale=False,
        colorscale='YlGnBu',
        color=node_colors,
        size=node_sizes,
        line_width=2
    )
)
```

### **3. Integrate with Other Tools**

Consider integrating the visualization with project management tools or embedding it within documentation platforms for easier access by team members.

---

## **Conclusion**

By following the steps above, you should be able to successfully generate and view an interactive dependency graph for your **GAIA AIR – AMPEL-360XWLRGA** project. Saving the visualization as an HTML file ensures that you can access it anytime and share it with team members easily.

If you continue to face issues or have further questions, please provide additional details or specific error messages, and I'll be happy to assist you further.

**Happy Coding and Best of Luck with Your GAIA AIR Project!**
