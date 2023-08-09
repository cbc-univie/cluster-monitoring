#notes
'''
If a page has a lot of components, I suggest splitting them up into their own files such as this one.
'''

# package imports
import datetime

import plotly.express as px
from dash import Input, Output, callback, dcc, html
from utils.geosphere import data_from_hourly
from utils.preprocess_data import generate_dfs

#import dash_bootstrap_components as dbc

random_component = html.Div('We are waiting for JK to give us some plots...')

#we schoudl really get the data at one spot!
rs02, rs10 = generate_dfs()
wg,_ = data_from_hourly("VKM") #windgeschwindigkeit
ns,_ = data_from_hourly("RSX") #niederschlag
sd,_ = data_from_hourly("SUX") #sonnenscheindauer

@callback(
    Output(component_id="corr1", component_property="figure"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(start_date, end_date):
    filtered_data = wg.query(
        "date >= @start_date and date <= @end_date"
    )
    filtered_rs02 = rs02.query(
        "date >= @start_date and date <= @end_date"
    )
    simple_figure = px.line(x=filtered_data["date"], y=filtered_data["VKM"], labels={"VKM": "wind speed"}, title="wind speed with rs02")
    simple_figure.update_traces(name="wind speed", showlegend=True) # needs to come directly after!

    simple_figure.add_scatter(x=filtered_rs02["date"], y=filtered_rs02["outdoor temp"], mode='lines', name='outdoor temp', yaxis="y2")
    simple_figure.update_layout(xaxis_title="Date", yaxis=dict(title='wind speed km/h'), yaxis2=dict(title="temperature °C", overlaying="y", side="right")),
                                #yaxis_title="Temperature (°C)", yaxis2_title="Jobs", showlegend=True)
   
    return simple_figure

correlation_plot = (html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children="Pick your start and end day for the plots!", className="menu-title"
                            ),
                            dcc.DatePickerRange(
                                id="date-range",
                                min_date_allowed=datetime.date(2023, 7, 24),
                                max_date_allowed=rs02["date"].max(),
                                start_date=datetime.date(2023, 7, 24),
                                end_date=rs02["date"].max(),
                            ),
                            html.Div(
                                children = dcc.Graph(
                                    id="corr1",
                                    config={"displayModeBar": False},
                                    figure={}
                                ),
                                className="card",
                            )
                        ]
                    ),
               ],
                className="menu",
            ) #, here was a problem
)
