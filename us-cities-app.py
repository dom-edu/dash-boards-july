import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc ,  Input, Output,callback

# loading in the data 
URL = "https://raw.githubusercontent.com/plotly/datasets/refs/heads/master/2014_us_cities.csv"
cities_df = pd.read_csv(URL)


# too much data, let's slim it down to top_10
top_10_cities = cities_df.sort_values('pop', ascending=False).head(10)


# add a plotly bar chart 
x = top_10_cities['name'] # get city names 
y = top_10_cities['pop'] # get city populations
bar_ = px.bar(x=x, y=y)

# drop down component 
# make cities 
dd_1 = dcc.Dropdown(
    x,
    x[:2], # by default select first two 
    id="cities-dd",
    placeholder="Select a city",
    multi=True
)

# change axis labels, usually 
# how we edit styles in dash 
bar_.update_layout(
    xaxis_title = "City",
    yaxis_title = "Pop"
)

# format tooltip text 
cities_df['text'] = cities_df['name'] + '<br>Population ' + (cities_df['pop']/1e6).astype(str)+' million'

limits = [(0,3),(3,11),(11,21),(21,50),(50,3000)]
colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
cities = []
scale = 5000


# empty frame 
geo_scatter_ = go.Figure()

for i in range(len(limits)):
    lim = limits[i]
    df_sub = cities_df[lim[0]:lim[1]]
    geo_scatter_.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_sub['lon'],
        lat = df_sub['lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['pop']/scale,
            color = colors[i],
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1])))

geo_scatter_.update_layout(
        title_text = '2014 US city populations<br>(Click legend to toggle traces)',
        showlegend = True,
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)',
        )
    )




# instantiate the dash app 
app = Dash(__name__)

# app layout 
app.layout = [
    html.Div(children="US City Populations", style={'textAlign':'center'}),
    dd_1,
    dcc.Graph(figure=bar_, id="cities-bar-chart"),
    dcc.Graph(figure=geo_scatter_, id="cities-geo-scatter")
]

# we want to register a call back 
@callback(
    Output('cities-bar-chart', 'figure'),
    Input('cities-dd', 'value')
)
def update_graph(value):
    """
    
    

    Args:
        value : selected cities 

    Returns:
        new bar chart with selected cities 
    """
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
