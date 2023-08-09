# package imports
import dash
from components import first_plots
from dash import Input, Output, callback, dcc, html

dash.register_page(
    __name__,
    path='/',
    redirect_from=['/home'],
    title='Home'
)

layout = html.Div(
    [
        #html.H1('Home page!'),
        # html.Div(
        #     html.A('Checkout awesome correlations here.', href='/correlations')
        # ),
        #html.A('/page2', href='/page2'),
        # dcc.RadioItems(
        #     id='radios',
        #     options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        #     value='Orange',
        # ),
        html.Div(id='content'),
        first_plots
    ]
)

# @callback(Output('content', 'children'), Input('radios', 'value'))
# def home_radios(value):
#     return f'You have selected {value}'
