# notes
'''
This file is for housing the main dash application.
This is where we define the various css items to fetch as well as the layout of our application.
'''

# package imports
import datetime
import os

import dash
import dash_bootstrap_components as dbc

# local imports
from components import footer, navbar
from dash import html  #Input, Output, dcc,

app = dash.Dash(
    __name__,
    # server=server,
    use_pages=True,    # turn on Dash pages
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME
    ],  # fetch the proper css items we want
    # meta_tags=[
    #     {   # check if device is a mobile device. This is a must if you do any mobile styling
    #         'name': 'viewport',
    #         'content': 'width=device-width, initial-scale=1'
    #     }
    # ],
    # suppress_callback_exceptions=True,
    title='Dash app structure'
)

def serve_layout():
    '''Define the layout of the application'''
    return html.Div(
        children = [
            html.Div(
                children = [
                    html.P(children="🌹", className="header-emoji"),
                    html.H1(children="Cluster Monitoring", className="header-title"),
                    html.P(
                        children=(
                            "Insights into our clusters"
                        ),
                        className="header-description",
                    ),
                ],
                className="header",
            ),
            navbar,
            dbc.Container(
                dash.page_container,
                class_name='my-2'
            ),
            footer
            
        ]
    )


app.layout = serve_layout   # set the layout to the serve_layout function
#server = app.server         # the server is needed to deploy the application



if __name__ == "__main__":
    app.run_server(
        #host=APP_HOST,
        #port=APP_PORT,
        debug=True #APP_DEBUG,
        #dev_tools_props_check=DEV_TOOLS_PROPS_CHECK
    )
