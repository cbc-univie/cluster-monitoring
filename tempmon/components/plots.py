import datetime

import plotly.express as px
from dash import Input, Output, callback, dcc, html
from utils.preprocess_data import generate_dfs

#get the data
#TODO: maybe check with timestamp if we can skip the conversion from log to csv and just load the df
rs02, rs10 = generate_dfs()

@callback(
    Output(component_id="simple_plot", component_property="figure"),
    #Input("line-selector", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(start_date, end_date):
    filtered_data = rs02.query(
        "date >= @start_date and date <= @end_date"
    )
    # trace1 = go.Scatter(x=filtered_data["date"], y=filtered_data["server room temp"], mode='lines', name='server room temp')
    # trace2 = go.Scatter(x=filtered_data["date"], y=filtered_data["outdoor temp"], mode='lines', name='outdoor temp')
    # selected_traces = [trace for trace in [trace1, trace2] if trace['name'] in selected_lines]
    # fig = go.Figure()
    # for trace in selected_traces:
    #     fig.add_trace(trace)
    #return {'data': selected_traces}
    simple_figure = px.line(x=filtered_data["date"], y=filtered_data["server room temp"], labels={"server room temp": "server room"}, title="rs02")
    simple_figure.update_traces(name="server room temp", showlegend=True) # needs to come directly after!

    simple_figure.add_scatter(x=filtered_data["date"], y=filtered_data["outdoor temp"], mode='lines', name='outdoor temp', yaxis="y1")
    simple_figure.add_scatter(x=filtered_data["date"], y=filtered_data["total jobs"], mode='lines', name='total jobs', yaxis="y2")
    simple_figure.update_layout(xaxis_title="Date", yaxis=dict(title='Temperature °C'), yaxis2=dict(title="Jobs", overlaying="y", side="right")),
                                #yaxis_title="Temperature (°C)", yaxis2_title="Jobs", showlegend=True)
   
    return simple_figure

@callback(
    Output(component_id="rs10", component_property="figure"),
    #Input("line-selector", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_rs10(start_date, end_date):
    filtered_data = rs10.query(
        "date >= @start_date and date <= @end_date"
    )
    # trace1 = go.Scatter(x=filtered_data["date"], y=filtered_data["server room temp"], mode='lines', name='server room temp')
    # trace2 = go.Scatter(x=filtered_data["date"], y=filtered_data["outdoor temp"], mode='lines', name='outdoor temp')
    # selected_traces = [trace for trace in [trace1, trace2] if trace['name'] in selected_lines]
    # fig = go.Figure()
    # for trace in selected_traces:
    #     fig.add_trace(trace)
    #return {'data': selected_traces}
    simple_figure = px.line(x=filtered_data["date"], y=filtered_data["server room temp"], title="rs10 (🌹)")
    simple_figure.update_traces(name="server room temp", showlegend=True) # needs to come directly after!

    simple_figure.add_scatter(x=filtered_data["date"], y=filtered_data["outdoor temp"], mode='lines', name='outdoor temp')
    simple_figure.add_scatter(x=filtered_data["date"], y=filtered_data["total jobs"], mode='lines', name='total jobs', yaxis="y2")

    

    simple_figure.update_layout(xaxis_title="Date", yaxis=dict(title='Temperature °C'), yaxis2=dict(title="Jobs", overlaying="y", side="right")),
    #simple_figure.update_layout(xaxis_title="Date", yaxis_title="Temperature (°C)")
   
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
                                min_date_allowed=datetime.date(2023, 7, 24),
                                max_date_allowed=rs02["date"].max(),
                                start_date=datetime.date(2023, 7, 24),
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
            ) #, here was a problem
            # html.Div(
            #     children=[
            #         # dcc.Checklist(
            #         #     id='line-selector',
            #         #     options=[
            #         #         {'label': 'server room temp', 'value': 'server room temp'},
            #         #         {'label': 'outdoor temp', 'value': 'outdoor temp'},
            #         #     ],
            #         #     value=['server room temp', 'outdoor temp'],  # Initial lines to show
            #         #     labelStyle={'display': 'inline-block'}
            #         # ),
            #         html.Div(
            #             children = dcc.Graph(
            #                 id="simple_plot",
            #                 config={"displayModeBar": False},
            #                 #figure={"data": [trace1, trace2]}
            #             ),
            #             className="card",
            #         ),
            #         html.Div(
            #             children = dcc.Graph(
            #                 id="rs10",
            #                 config={"displayModeBar": False},
            #                 #figure={"data": [trace1, trace2]}
            #             ),
            #             className="card",
            #         ),
            #     ],
            #     className="wrapper",
            # )#,

)

























#data = get_test_data()
#print(data.head())

# simple_plot = (
#     html.Div(
#         children=[
#             html.Div(
#                 children=[
#                     html.Div(
#                         children="Date Range", className="menu-title"
#                     ),
#                     dcc.DatePickerRange(
#                         id="date-range",
#                         min_date_allowed=data["date"].min().date(),
#                         max_date_allowed=data["date"].max().date(),
#                         start_date=data["date"].min().date(),
#                         end_date=data["date"].max().date(),
#                     ),
#                 ]
#             ),
#         ],
#         className="menu",
#     ),
#     html.Div(
#                 children=[
#                     html.Div(
#                     children = dcc.Graph(
#                         id="simple_plot",
#                         config={"displayModeBar": False},
#                         # figure={
#                         #     "data": [
#                         #         {
#                         #             "x": data["date"],
#                         #             "y": data["server room temp"],
#                         #             "type": "lines",
#                         #         },
#                         #     ],
#                         #     "layout": {
#                         #             "title": {
#                         #                 "text": "Server room temp with time",
#                         #                 "x": 0.05,
#                         #                 "xanchor": "left",
#                         #             },
#                         #             "xaxis": {"fixedrange": True},
#                         #             "yaxis": {
#                         #                 "tickprefix": "$",
#                         #                 "fixedrange": True,
#                         #             },
#                         #             "colorway": ["#17b897"],
#                         #     },
#                         # },
#                     ),
#                     className="card",
#                 ),
#                 ],
#                 className="wrapper",
# )
# )