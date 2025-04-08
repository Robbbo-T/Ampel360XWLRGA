import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA
import os
import re
from ampel_system import AMPEL360System

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Load the data
df_kpi_extended = pd.read_csv('data/kpi_data_extended.csv')

# Initialize the AMPEL360System
ampel_system = AMPEL360System()

# Define the layout
app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='metric-dropdown',
                options=[
                    {'label': 'Reducción de Fallos Estructurales (%)', 'value': 'Reducción de Fallos Estructurales (%)'},
                    {'label': 'Otro KPI', 'value': 'Otro KPI'}
                ],
                value='Reducción de Fallos Estructurales (%)'
            ),
        ], width=6),
        dbc.Col([
            dbc.Checklist(
                id='graph-type-toggle',
                options=[
                    {'label': 'Mostrar Predicciones', 'value': 'show_predictions'}
                ],
                value=[]
            ),
        ], width=6)
    ]),
    dcc.Graph(id='kpi-graph'),
    html.Div(id='component-structure'),
    html.Button('Optimize Power Distribution', id='optimize-button', n_clicks=0),
    html.Div(id='optimization-result'),
    html.Div(id='ampel-commands'),
    html.Div(id='xai-cycle')
])

# Define the callback to update the graph
@app.callback(
    Output('kpi-graph', 'figure'),
    [Input('metric-dropdown', 'value'),
     Input('graph-type-toggle', 'value')]
)
def update_graph(selected_metric, graph_type_toggle):
    fig = go.Figure()

    if selected_metric == 'Reducción de Fallos Estructurales (%)':
        fig.add_trace(go.Scatter(x=df_kpi_extended['Fecha'], y=df_kpi_extended[selected_metric], mode='lines', name=selected_metric))

        if 'show_predictions' in graph_type_toggle:
            model = ARIMA(df_kpi_extended[selected_metric], order=(5, 1, 0))
            model_fit = model.fit()
            predictions = model_fit.forecast(steps=10)
            fig.add_trace(go.Scatter(x=pd.date_range(start=df_kpi_extended['Fecha'].iloc[-1], periods=10, freq='M'), y=predictions, mode='lines', name='Predicciones'))

    fig.update_layout(title='KPI Graph', xaxis_title='Fecha', yaxis_title=selected_metric)
    return fig

# Define the callback to update the component structure
@app.callback(
    Output('component-structure', 'children'),
    [Input('metric-dropdown', 'value')]
)
def update_component_structure(selected_metric):
    if selected_metric == 'Reducción de Fallos Estructurales (%)':
        with open('data/AMPEL360XWLRGA-Aircraft-assembly-Breakdown.md', 'r') as file:
            component_structure = file.read()
        return html.Pre(component_structure)
    return html.Div()

# Define the callback for power distribution optimization
@app.callback(
    Output('optimization-result', 'children'),
    [Input('optimize-button', 'n_clicks')]
)
def optimize_power_distribution(n_clicks):
    if n_clicks > 0:
        power_demand = [100, 200, 300, 400, 500]
        power_supply = [90, 210, 310, 390, 510]
        optimized_distribution = ampel_system.optimize_power_distribution(power_demand, power_supply)
        return html.Div(f"Optimized Power Distribution: {optimized_distribution}")
    return html.Div()

# Define the callback to display AMPEL commands with XAI annotations
@app.callback(
    Output('ampel-commands', 'children'),
    [Input('metric-dropdown', 'value')]
)
def display_ampel_commands(selected_metric):
    if selected_metric == 'Reducción de Fallos Estructurales (%)':
        ampel_commands = """
        ### AMPEL Command Examples with XAI Annotations

        **Example 1: Quantum Thrust Control**
        ```
        # Activate quantum thrust propulsion at 75% power
        SUBSYS:QUANTUM_THRUST(power=75)

        # XAI:
        # - Ethics: Compliant (Low emissions profile at 75% power)
        # - Performance: Optimal choice (Balanced consumption/efficiency ratio)
        # - Alternatives: power=60 (Energy saving mode, extended operation time, reduced thrust), 
        #                power=90 (High performance mode, increased velocity, higher energy consumption)
        # - Trace: QAO-TRC-0xAA17D34E
        # - Decision basis: Quantum Algorithmic Orchestrator v4.2.1
        ```

        **Example 2: Environmental Control System**
        ```
        # Set cabin temperature to 21°C with 45% humidity
        SUBSYS:ENV_CONTROL(temp=21, humidity=45)

        # XAI:
        # - Ethics: Compliant (Optimal comfort settings within energy efficiency guidelines)
        # - Performance: Efficient operation (45% humidity minimizes energy usage while maintaining comfort)
        # - Health: Recommended (Temperature and humidity within ideal range for passenger wellbeing)
        # - Alternatives: temp=19 (Energy saving, may feel cool to some passengers),
        #                temp=23 (Higher comfort for cold-sensitive passengers, increased energy usage)
        # - Trace: QAO-TRC-0xBF29E71C
        # - Decision basis: Cabin Comfort Optimization Algorithm v3.1.5
        ```

        **Example 3: Navigation System Waypoint**
        ```
        # Set navigation waypoint to KSFO with priority level 2
        SUBSYS:NAVIGATION(waypoint="KSFO", priority=2)

        # XAI:
        # - Ethics: Compliant (Route respects airspace restrictions and noise abatement procedures)
        # - Safety: Verified (Waypoint has been validated against current NOTAMs and weather conditions)
        # - Performance: Fuel-optimized (Route calculated for minimal fuel consumption)
        # - Alternatives: priority=1 (Time-optimized route, higher fuel consumption),
        #                priority=3 (Emissions-optimized route, longer flight time)
        # - Trace: QAO-TRC-0xC7D45A2B
        # - Decision basis: Quantum Route Optimization Engine v2.8.3
        ```

        **Example 4: Power Distribution Management**
        ```
        # Allocate 35% power to life support systems
        SUBSYS:POWER_DIST(life_support=35, propulsion=45, avionics=20)

        # XAI:
        # - Ethics: Compliant (Life support prioritization meets human-centric operation guidelines)
        # - Safety: Critical systems protected (Minimum 30% allocation to life support required)
        # - Performance: Balanced allocation (Sufficient power for all systems with appropriate reserves)
        # - Risk: Low (Current allocation provides 15% buffer for emergency scenarios)
        # - Alternatives: life_support=30 (Minimum safe level, allows more power for propulsion),
        #                life_support=40 (Enhanced comfort, reduced power for non-essential systems)
        # - Trace: QAO-TRC-0xD8E36F1A
        # - Decision basis: Critical Systems Management Protocol v5.0.2
        ```

        **Example 5: Quantum Sensor Array Configuration**
        ```
        # Configure quantum sensor array for atmospheric analysis
        SUBSYS:QUANTUM_SENSORS(mode="atmospheric", resolution=8, scan_rate=2.5)

        # XAI:
        # - Ethics: Compliant (Data collection respects privacy zones and restricted airspace)
        # - Performance: Optimized for atmospheric conditions (Resolution 8 balances detail and processing load)
        # - Resource usage: Moderate (2.5 Hz scan rate requires 18% of available quantum computing capacity)
        # - Alternatives: resolution=6 (Faster processing, lower detail),
        #                resolution=10 (Higher detail, increased power consumption and processing load)
        # - Trace: QAO-TRC-0xE9F47B2D
        # - Decision basis: Quantum Sensing Optimization Framework v1.7.4
        ```

        **Example 6: Cryogenic System Management**
        ```
        # Set cryogenic cooling to maintain quantum core at 4.2K
        SUBSYS:CRYO_CONTROL(target_temp=4.2, flow_rate=12.5)

        # XAI:
        # - Ethics: Compliant (Energy usage within sustainable operation parameters)
        # - Performance: Optimal for quantum coherence (4.2K maintains 99.97% coherence time)
        # - Safety: Monitored (Automatic shutdown triggers if temperature exceeds 4.8K)
        # - Alternatives: target_temp=3.8 (Extended coherence time, 15% higher energy consumption),
        #                target_temp=4.5 (Reduced cooling load, slight decrease in quantum performance)
        # - Trace: QAO-TRC-0xF1A58C3E
        # - Decision basis: Quantum Core Thermal Management System v3.2.7
        ```

        **Example 7: Communication System Configuration**
        ```
        # Establish quantum-encrypted communication channel with ground control
        SUBSYS:COMMS(channel="quantum_secure", bandwidth=50, encryption_level=3)

        # XAI:
        # - Ethics: Compliant (Communication respects data sovereignty and privacy regulations)
        # - Security: Maximum protection (Level 3 encryption provides quantum-resistant security)
        # - Performance: Balanced (50 Mbps bandwidth sufficient for telemetry and command data)
        # - Alternatives: bandwidth=25 (Reduced data rate, lower power consumption),
        #                bandwidth=100 (Higher data rate for enhanced telemetry, increased power usage)
        # - Trace: QAO-TRC-0xG2B69D4F
        # - Decision basis: Secure Communications Protocol v4.5.1
        ```

        These examples demonstrate how the XAI annotations provide transparency and explainability for AMPEL commands across different subsystems. Each annotation includes ethical considerations, performance implications, alternatives, and traceability information, enabling operators to understand the reasoning behind system recommendations and decisions.
        """
        return dcc.Markdown(ampel_commands)
    return html.Div()

# Define the callback to display XAI CYCLE: MASTERING INPUT PROMPTS
@app.callback(
    Output('xai-cycle', 'children'),
    [Input('metric-dropdown', 'value')]
)
def display_xai_cycle(selected_metric):
    if selected_metric == 'Reducción de Fallos Estructurales (%)':
        xai_cycle = """
        ### XAI CYCLE: MASTERING INPUT PROMPTS FOR DESIRED AIRCRAFT BEHAVIOUR

        **Overview:**
        The XAI Cycle concept consists of five main components:
        1. **Input Formulation:** Crafting precise and effective AMPEL commands.
        2. **XAI Processing:** Parsing and interpreting commands using the XAI Interpreter.
        3. **Explanation Generation:** Providing transparent and explainable annotations for each command.
        4. **Execution & Feedback:** Implementing the commands and monitoring outcomes.
        5. **Refinement:** Continuously improving command formulation based on feedback.

        **Master Protocol:**
        The Master Prompt Protocol is a structured methodology for creating effective AMPEL commands. It includes six steps:
        1. **Intent Declaration:** Clearly state the objective of the command.
        2. **Subsystem Selection:** Identify the relevant subsystem(s) for the command.
        3. **Command Specification:** Define the specific action or configuration to be implemented.
        4. **Parameter Definition:** Specify the parameters and their values for the command.
        5. **Constraint Specification:** Outline any constraints or conditions for the command.
        6. **Prevention Planning:** Proactively identify potential issues and define appropriate responses.

        **Prevention Planning:**
        Prevention planning involves a framework for identifying potential issues and defining appropriate responses. It includes:
        1. **Risk Identification:** Identify potential risks and their impact.
        2. **Fallback Definition:** Define fallback actions in case of issues.
        3. **Parameter Constraints:** Set boundaries for parameter values to ensure safe operation.
        4. **Transition Logic:** Define logic for transitioning between different states or modes.
        5. **Command Integration:** Ensure seamless integration of commands with existing systems.

        **Examples:**
        Here are three detailed examples of well-crafted AMPEL commands following the Master Prompt Protocol:

        **Example 1: Precision Hover with Wind and Power Fallbacks**
        ```
        # Intent: Maintain precision hover with wind compensation and power fallbacks
        SUBSYS:FLIGHT_CONTROL(mode="hover", altitude=100, wind_compensation=True)

        # XAI:
        # - Ethics: Compliant (Ensures safety and stability)
        # - Performance: Optimal (Maintains hover with minimal drift)
        # - Alternatives: mode="hover", altitude=90 (Lower altitude, reduced power consumption),
        #                mode="hover", altitude=110 (Higher altitude, increased power consumption)
        # - Trace: QAO-TRC-0xH1A2B3C4
        # - Decision basis: Hover Stability Algorithm v2.3.1
        ```

        **Example 2: Autonomous Navigation with Traffic and Weather Contingencies**
        ```
        # Intent: Navigate autonomously with traffic and weather contingencies
        SUBSYS:NAVIGATION(route="KSFO-KLAX", priority=2, traffic_avoidance=True, weather_monitoring=True)

        # XAI:
        # - Ethics: Compliant (Adheres to airspace regulations and safety protocols)
        # - Safety: Verified (Route validated against current traffic and weather conditions)
        # - Performance: Efficient (Optimized for minimal fuel consumption)
        # - Alternatives: priority=1 (Time-optimized route, higher fuel consumption),
        #                priority=3 (Emissions-optimized route, longer flight time)
        # - Trace: QAO-TRC-0xI2B3C4D5
        # - Decision basis: Autonomous Navigation Engine v4.1.2
        ```

        **Example 3: Quantum Propulsion Management with Thermal and Coherence Safeguards**
        ```
        # Intent: Manage quantum propulsion with thermal and coherence safeguards
        SUBSYS:QUANTUM_PROPULSION(power=75, thermal_monitoring=True, coherence_optimization=True)

        # XAI:
        # - Ethics: Compliant (Ensures safe and efficient propulsion)
        # - Performance: Optimal (Balanced power and thermal management)
        # - Alternatives: power=60 (Energy saving mode, extended operation time, reduced thrust),
        #                power=90 (High performance mode, increased velocity, higher energy consumption)
        # - Trace: QAO-TRC-0xJ3C4D5E6
        # - Decision basis: Quantum Propulsion Control Algorithm v5.0.3
        ```

        This documentation will help operators craft effective input prompts that generate predictable, safe, and optimal aircraft behavior while maintaining ethical compliance and safety standards.
        """
        return dcc.Markdown(xai_cycle)
    return html.Div()

def parse_ata_structure(text):
    lines = text.strip().split('\n')
    structure = {}
    current_section = None
    current_subsection = None
    current_ata_chapter = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith("Back") or line.startswith("Cont"):
            continue
        part_match = re.match(r"Part\s+\w+:", line)
        if part_match:
            continue
        section_match = re.match(r"(\d+\.\d+\.\d+\.[A-Z]+)\s+ATA\s+(\d+) - (.+)", line)
        if section_match:
            current_section = section_match.group(1).replace(".","-")
            ata_number = section_match.group(2)
            ata_title = section_match.group(3)
            current_ata_chapter = f"ATA_{ata_number}"
            structure[current_section] = {
                "title": f"ATA {ata_number} - {ata_title}",
                "documents": {},
            }
            current_subsection = None
            continue

        subsection_match = re.match(r"(\d+\.\d+\.\d+\.[A-Z]+\.\d+)\s+([\d\-]+)\s+(.+)", line)
        if subsection_match:
            current_subsection = subsection_match.group(1).replace(".","-")
            subsection_title = subsection_match.group(3)
            structure[current_section][current_subsection] = {
                "title": subsection_title,
                "documents": {},
            }
            continue

        in_match = re.match(r"IN:\s+(GPAM-AMPEL-\S+)\s+-\s+(.+)(?:\(S1000D\))?", line)
        if in_match:
            in_code = in_match.group(1)
            doc_title = in_match.group(2).strip()

            if current_subsection:
                structure[current_section][current_subsection]['documents']["IN: "+ in_code + " - " + doc_title] = {}
            elif current_section:
                structure[current_section]['documents']["IN: "+ in_code + " - " + doc_title] = {}
            continue

        dmc_match = re.match(r"DMC:\s+(.+)", line)
        if dmc_match:
            continue

    return structure

def create_markdown_file(file_path, in_code, title):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Document: {in_code} - {title}\n\n")
        f.write(f"**Document ID:** {in_code}\n")
        f.write(f"**Version:** 1.0 (Draft)\n")
        f.write(f"**Date:** [Date of Creation]\n")
        f.write(f"**Author:** [Author Name]\n\n")
        f.write("[Placeholder: Document Content]\n")
    print(f"Created file: {file_path}")

def create_directories_and_files(base_path, structure):
    for key, value in structure.items():
        if key.startswith("IN:"):
            match = re.match(r"IN:\s+(.+?)\s+-\s+(.+)", key)
            if match:
                in_code = match.group(1)
                title = match.group(2)
                file_name = f"{in_code}.md"
                file_path = os.path.join(base_path, file_name)
                create_markdown_file(file_path, in_code, title)

        elif isinstance(value, dict):
            dir_path = os.path.join(base_path, key)
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created directory: {dir_path}")
            create_directories_and_files(dir_path, value)

if __name__ == "__main__":
    input_text = """
2.1 AMPEL360XWLRGA (Advanced Aircraft
Systems)
2.1.1 ATA Chapters
2.1.1.A ATA 05 - Time
Limits/Maintenance Checks
IN: GPAM-AMPEL-0201-05-001 - Scheduled Maintenance Program (S1000D)
IN: GPAM-AMPEL-0201-05-002 - Maintenance Time Limits (S1000D)
IN: GPAM-AMPEL-0201-05-003 - Airworthiness Limitations (S1000D)
2.1.1.B ATA 06 - Dimensions and Areas
IN: GPAM-AMPEL-0201-06-001-A - Aircraft Dimensions and Stations (S1000D)
IN: GPAM-AMPEL-0201-06-002-A - Compartment Layout and Dimensions (S1000D)
IN: GPAM-AMPEL-0201-06-003-A - AMPEL360XWLRGA Measurement Point Definitions
2.1.1.C ATA 07 - Lifting and Shoring
IN: GPAM-AMPEL-0201-07-001 - Lifting Procedures and Diagrams (S1000D)
IN: GPAM-AMPEL-0201-07-002 - Shoring Procedures and Diagrams (S1000D)
2.1.1.D ATA 08 - Leveling and Weighing
IN: GPAM-AMPEL-0201-08-001 - Leveling Procedures (S100D)
IN: GPAM-AMPEL-0201-08-002 - Aircraft Weighing Procedures (S1000D)
2.1.1.E ATA 09 - Towing and Taxiing
IN: GPAM-AMPEL-0201-09-001 - Towing Procedures (S1000D)
IN: GPAM-AMPEL-0201-09-002 - Taxiing Procedures (S1000D)
2.1.1.F ATA 10 - Parking, Mooring, Storage and Return to Service
IN: GPAM-AMPEL-0201-10-001 - Parking Procedures (S1000D)
IN: GPAM-AMPEL-0201-10-002 - Mooring Procedures (S1000D)
IN: GPAM-AMPEL-0201-10-003 - Storage Procedures (S1000D)
IN: GPAM-AMPEL-0201-10-004 - Return to Service Procedures (S1000D)
IN: GPAM-AMPEL-0201-10-005 - Return to Service Checklists (S1000D)
2.1.1.G ATA 11 - Placards and Markings
IN: GPAM-AMPEL-0201-11-001 - Exterior Placards and Markings (S1000D)
IN: GPAM-AMPEL-0201-11-002 - Interior Placards and Markings (S1000D)
2.1.1.H ATA 12 - Servicing
IN: GPAM-AMPEL-0201-12-001 - Servicing Procedures (S1000D)
IN: GPAM-AMPEL-0201-12-002 - Servicing Equipment List (S1000D)
IN: GPAM-AMPEL-0201-12-003 - Cold Weather Maintenance Procedures (S100D)
2.1.1.I ATA 20 - Standard Practices -
Airframe systems
IN: GPAM-AMPEL-0201-20-001-A - Torque Values & Procedures (S1000D)
IN: GPAM-AMPEL-0201-20-002-A - Electrical Bonding Procedures (S1000D)
2.1.1.J ATA 21 - Air Conditioning:
IN: GPAM-AMPEL-0201-21-001-A - Air Conditioning System Schematics (S1000D)
IN: GPAM-AMPEL-0201-21-002-A - Cabin Temperature Control System (S100D)
2.1.1.K ATA 22 - Auto Flight:
2.1.1.L ATA 23 - Communications:
2.1.1.M ATA 24 - Electrical Power:
2.1.1.N ATA 25 - Equipment /
Furnishings:
2.1.1.O ATA 26 - Fire Protection:

2.1.1.P ATA 27 - Flight Controls:
2.1.1.Q ATA 28 - Fuel:
2.1.1.Q.1 Alternative Energy Harvesting and Control System (AEHCS)
2.1.1.Q.1.1 AEHCS System Level
Documents
2.1.1.Q.1.2 AEHCS Subcomponents
Integration and Performance
2.1.1.Q.1.3 AEHCS Cryogenic and
Battery Systems
2.1.1.Q.1.4 AEHCS Al Control and Monitoring
2.1.1.Q.1.5 AEHCS Performance and Testing
2.1.1.Q.1.6 AEHCS Safety and Redundancy
2.1.1.Q.1.7 AEHCS Maintenance and Inspection
2.1.1.R ATA 29 - Hydraulic Power:
2.1.1.S ATA 30 - Ice and Rain
Protection:
2.1.1.T ATA 31 - Instruments:
2.1.1.U ATA 32 - Landing Gear:
2.1.1.V ATA 33 - Lights:
2.1.1.W ATA 34 - Navigation:
2.1.1.X ATA 35 - Oxygen:
2.1.1.Y ATA 36 - Pneumatic:

2.1.1.Z ATA 38 - Water/Waste:
2.1.1.AA ATA 45 - Central Maintenance
System:
2.1.1.AB ATA 46 - Information Systems:
2.1.1.AC ATA 49 - Airborne Auxiliary
Power:
2.1.1.AD ATA 51 - Standard Practices -
Airframe Structures:
2.1.1.AE ATA 52 - Doors:
2.1.1.AE.1 Door Design and
Operation
2.1.1.AE.2 Safety and Locking
Mechanisms
2.1.1.AE.3 Emergency Exits and
Evacuation Procedures
2.1.1.AE.4 Maintenance and
Inspection
2.1.1.AF ATA 53 - Fuselage:
2.1.1.AF.1 53-10-00-000 Nose
Section
2.1.1.AF.2 53-20-00-000 Forward
Section
2.1.1.AF.3 53-30-00-000 Central
Section
2.1.1.AF.4 53-40-00-000 Belly
Section
2.1.1.AF.5 53-50-00-000 Tail Cone
Section
2.1.1.AF.6 53-60-00-000
2.1.1.AF.7 53-70-00-000
Additional Stations (Reserved for
Future Use)
2.1.1.AF.8 53-80-00-000 Auxiliary Stations (Reserved for Future Use)
2.1.1.AF.9 53-99-99-000 User
Guide
2.1.1.AG ATA 55 - Stabilizers:
2.1.1.AH ATA 56 - Windows:
2.1.1.AI ATA 57 - Wings:
2.1.1.AJ ATA 58 - - Wing Anti-Icing:
2.1.1.AK ATA 67 - Rotors (Not
Applicable):
2.1.1.AL ATA 70 - Standard Practices - Engine:
2.1.1.AM ATA 71 - Powerplant (Q-01
Quantum Propulsion System):
2.1.1.AM.1 Q-01 Quantum
Propulsion System Integration
2.1.1.AM.2 Propulsion System
Control and Monitoring
2.1.1.AM.3 Interface with AEHCS
2.1.1.AU ATA 72 - Engine (Q-01):
2.1.1.AV ATA 73 - Engine Fuel and Control:
2.1.1.AW ATA 74 - Ignition:
2.1.1.AX ATA 75 - Air:
2.1.1.AY ATA 76 - Engine Controls:
2.1.1.AZ ATA 77 - Engine Indicating:
2.1.1.BA ATA 78 - Exhaust:
2.1.1.BB ATA 79 - Oil:
2.1.1.BC ATA 80 - Starting:
2.1.1.CA ATA 91 - Charts
2.1.1.DA ATA 92 - Electrical System
Testing
2.1.1.DB ATA 93 - Avionics Systems
2.1.1.DC ATA 94 - Propulsion System
Testing
2.1.1.DD ATA 95 - Structural and
Mechanical Testing
2.1.1.DE ATA 96 - Environmental Control and Life Support Testing
2.1.1.DF ATA 97 - Fire Protection
System Testing
2.1.1.DG ATA 98 - Flight Test Program
2.1.1.DH ATA 99 - Software and System
Integration Testing
2.1.1. DI ATA 100 - Certification and
Documentation
2.1.2 AMPEL360XWLRGA General
Documentation:
2.1.3 AMPEL360XWLRGA Maintenance
Manuals:
2.1.4 AMPEL360XWLRGA Illustrated
Parts Catalog:
2.1.5 AMPEL360XWLRGA Wiring and
Schematics:
    """

    output_directory = "COAFI_Part2"
    os.makedirs(output_directory, exist_ok=True)
    parsed_structure = parse_ata_structure(input_text)
    create_directories_and_files(output_directory, parsed_structure)

    print(f"\nDirectory structure and files created in: {output_directory}")

app.run_server(debug=True)
