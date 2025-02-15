import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Load the data
df_kpi_extended = pd.read_csv('data/kpi_data_extended.csv')

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
    html.Div(id='component-structure')
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

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
