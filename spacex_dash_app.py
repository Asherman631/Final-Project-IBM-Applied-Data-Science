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
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                            {'label':'All Sites', 'value':'All Sites'},
                                            {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                            {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                            {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                            {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}
                                    ],
                                    value='All Sites',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                marks={i: '{} (Kg)'.format(i) for i in range(0, 10001, 1000)},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_pie(entered_site):
  if entered_site == 'All Sites':
    piedata = spacex_df[['Launch Site', 'class']]
    piedat = piedata.groupby(['Launch Site']).sum()
    pie_fig = px.pie(piedat, values='class', names=piedat.index, title='Total successful launches by site')
    return pie_fig
  else:
    piedata = spacex_df[spacex_df['Launch Site']==entered_site]
    piedat = piedata['class'].value_counts()
    pie_fig = px.pie(piedat, names=piedat.index, values=piedat.values, title='Total successful launches for site {}'.format(entered_site))
    return pie_fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])
def get_sct(entered_site, payload):
  if entered_site == 'All Sites':
    sctdata = spacex_df[['Launch Site', 'class', 'Payload Mass (kg)', 'Booster Version Category']]
    sctdat = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1])]
    sct_fig = px.scatter(sctdat, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    return sct_fig
  else:
    sctdata = spacex_df[['Launch Site', 'class', 'Payload Mass (kg)', 'Booster Version Category']]
    sctdat1 = sctdata[sctdata['Launch Site']==entered_site]
    sctdat = sctdat1[(sctdat1['Payload Mass (kg)'] >= payload[0]) & (sctdat1['Payload Mass (kg)'] <= payload[1])]
    sct_fig = px.scatter(sctdat, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    return sct_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)