# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([
                                    dcc.Dropdown(id='site-dropdown',
                                                options=[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                                value='ALL',
                                                placeholder='Select a Launch Site',
                                                searchable=True)
                                ], style={'width': '80%', 'padding': '3% 10%'}),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div([
                                    dcc.RangeSlider(id='payload-slider',
                                                    min=spacex_df['Payload Mass (kg)'].min(),
                                                    max=spacex_df['Payload Mass (kg)'].max(),
                                                    step=1000,
                                                    marks={i: str(i) for i in range(0, int(max_payload)+1000, 1000)},
                                                    value=[min_payload, max_payload])
                                ], style={'width': '80%', 'padding': '1% 10%'}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Define callback for success-pie-chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)

def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        pie_data = spacex_df['class'].value_counts()
    else:
        pie_data = spacex_df[spacex_df['Launch Site'] == selected_site]['class'].value_counts()

    fig = px.pie(values=pie_data.values, names=pie_data.index, title='Success vs. Failure Count')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Define callback for success-payload-scatter-chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)

def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) & 
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                     title='Payload vs. Launch Success')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()




#in terminal ensure to install the following
#python3 -m pip install packaging
#python3 -m pip install pandas dash
#pip3 install httpx==0.20 dash plotly
#pip install pandas
#pip install plotly
#pip install dash

