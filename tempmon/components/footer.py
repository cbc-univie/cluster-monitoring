# notes
'''
This file is for creating a simple footer element.
This component will sit at the bottom of each page of the application.
'''

# package imports
from datetime import datetime

import dash_bootstrap_components as dbc
from dash import html

footer = html.Footer(
    dbc.Container(
        [
            dbc.Row([
                dbc.Col(
            #html.Hr(),
            '(c) cbc-univie',
                ),
                dbc.Col(
            #html.Br(),
            datetime.today().date(),
                ),
                dbc.Col(
            
            #html.Br(),
            'Footer item 3'
            )
            ]
            )
        ]
    )
)
