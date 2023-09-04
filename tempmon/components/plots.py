import datetime

import plotly.express as px
from dash import Input, Output, callback, dcc, html

from utils import filter, generate_dfs

colors = px.colors.qualitative.Plotly
BLUE,RED,GREEN = colors[0:3]

#get the data
#TODO: maybe check with timestamp if we can skip the conversion from log to csv and just load the df
rs02, rs10 = generate_dfs()
avg_t_rs02, avg_t_rs10 = filter(rs02, rs10, col_name="server room temp")

@callback(
    Output(component_id="simple_plot", component_property="figure"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(start_date, end_date):
    filtered_data = rs02.query(
        "date >= @start_date and date <= @end_date"
    )
    simple_figure = px.line(x=filtered_data["date"], y=filtered_data["server room temp"], labels={"server room temp": "server room"}, title="rs02")
    simple_figure.update_traces(name="server room (raw)", showlegend=True, opacity=0.25, marker=dict(color=BLUE)) # needs to come directly after!

    simple_figure.add_scatter(x=filtered_data["date"], y=filtered_data["filtered server room temp"], mode='lines', name='server room temp', yaxis="y1", marker=dict(color=BLUE))
    simple_figure.add_scatter(x=filtered_data["date"], y=filtered_data["outdoor temp"], mode='lines', name='outdoor temp', yaxis="y1", marker=dict(color=RED))
    simple_figure.add_scatter(x=filtered_data["date"], y=filtered_data["total jobs"], mode='lines', name='total jobs', yaxis="y2", marker=dict(color=GREEN))
    simple_figure.update_layout(xaxis_title="Date", yaxis=dict(title='Temperature °C'), yaxis2=dict(title="Jobs", overlaying="y", side="right"))
    simple_figure['layout']['yaxis2']['showgrid'] = False
   
    return simple_figure

@callback(
    Output(component_id="rs10", component_property="figure"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_rs10(start_date, end_date):
    filtered_data = rs10.query(
        "date >= @start_date and date <= @end_date"
    )
    simple_figure = px.line(x=filtered_data["date"], y=filtered_data["server room temp"], title="rs10 (🌹)")
    simple_figure.update_traces(name="server room (raw)", showlegend=True, opacity=0.25, marker=dict(color=BLUE)) # needs to come directly after!

    simple_figure.add_scatter(x=filtered_data["date"], y=filtered_data["filtered server room temp"], mode='lines', name='server room temp', yaxis="y1", marker=dict(color=BLUE))
    simple_figure.add_scatter(x=filtered_data["date"], y=filtered_data["outdoor temp"], mode='lines', name='outdoor temp', marker=dict(color=RED))
    simple_figure.add_scatter(x=filtered_data["date"], y=filtered_data["total jobs"], mode='lines', name='total jobs', yaxis="y2", marker=dict(color=GREEN))

    simple_figure.update_layout(xaxis_title="Date", yaxis=dict(title='Temperature °C'), yaxis2=dict(title="Jobs", overlaying="y", side="right"))
    simple_figure['layout']['yaxis2']['showgrid'] = False

   
    return simple_figure

first_plots = (html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children="Pick your start and end day for the plots!", className="menu-title"
                            ),
                            dcc.DatePickerRange(
                                id="date-range",
                                min_date_allowed= datetime.date(2023, 7, 24),
                                max_date_allowed=rs02["date"].max(),
                                start_date=datetime.date.today() - datetime.timedelta(days=15),
                                end_date=rs02["date"].max(),
                            ),
                            html.Div(
                                children = dcc.Graph(
                                    id="simple_plot",
                                    config={"displayModeBar": False},
                                    figure={}
                                ),
                                className="card",
                            ),
                            html.Div(
                                children = dcc.Graph(
                                    id="rs10",
                                    config={"displayModeBar": False},
                                ),
                                className="card",
                            ),
                        ]
                    ),
               ],
                className="menu",
            )
)