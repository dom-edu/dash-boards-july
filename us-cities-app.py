import pandas as pd 
import plotly.express as px
from dash import Dash, html, dcc ,  Input, Output,callback

url = "https://raw.githubusercontent.com/plotly/datasets/refs/heads/master/2014_us_cities.csv"

cities_df = pd.read_csv(url)


# too much data, let's slim it down to top_10
top_10_cities = cities_df.sort_values('pop', ascending=False).head(10)


# add a plotly bar chart 
x = top_10_cities['name'] # get city names 
y = top_10_cities['pop'] # get city populations
bar_ = px.bar(x=x, y=y)

# drop down 
# make cities 
dd_1 = dcc.Dropdown(
    x,
    x[:2], # by default select first two 
    id="cities-dd",
    multi=True
)


# change axis labels, usually 
# how we edit styles in dash 
bar_.update_layout(
    xaxis_title = "City",
    yaxis_title = "Pop"
)


# instantiate the dash app 
app = Dash(__name__)

# app layout 
app.layout = [
    html.Div(children="US City Populations", style={'textAlign':'center'}),
    dd_1,
    dcc.Graph(figure=bar_, id="cities-bar-chart")
]

# we want to register a call back 
@callback(
    Output('cities-bar-chart', 'figure'),
    Input('cities-dd', 'value')
)
def update_graph(value):
    print("DEBUG:", value)

    # filter the dataframe by selected value 
    filter_ = cities_df['name'].isin(value) # filter by selected values


    cities_sel_df = cities_df[filter_]
    x_ = cities_sel_df['name']
    y_ = cities_sel_df['pop']

    # remake the bar_chart 
    bar_ = px.bar(x= x_, y=y_)

    # bar chart styles
    bar_.update_layout(
        xaxis_title = "City",
        yaxis_title = "Pop"
    )
    
    return bar_






app.run(debug=True, port=5000)
