import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc ,  Input, Output,callback

GEO_SCALE = 500

# loading in the data 
URL = "https://raw.githubusercontent.com/plotly/datasets/refs/heads/master/2014_us_cities.csv"
cities_df = pd.read_csv(URL)

# strip name col of whitespace
cities_df['name'] = cities_df['name'].str.strip()

cities_df['text'] = cities_df['name'] + '<br>Population ' + (cities_df['pop']/1e6).astype(str)+' million'

def create_bar_chart(df_):
    
    x = df_['name'] # get city names 
    y = df_['pop'] # get city populations
    bar_ = px.bar(x=x, y=y)
    
    # change axis labels, usually 
    # how we edit styles in dash 
    bar_.update_layout(
        xaxis_title = "City",
        yaxis_title = "Pop"
    )
    
    return bar_
    

def create_geo_scatter(df_):
    
    
    
    # empty frame
    geo_scatter_ = go.Figure()
    
    # add one bubbles to city based on
    # entries of sel_cities 
    geo_scatter_.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon =df_['lon'],
        lat =df_['lat'],
        text =df_['text'],

        # adding a custom marker
        marker = dict(
            size =df_['pop']/GEO_SCALE,
            color = "royalblue",
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode = 'area'
        ),
        name = '{0}'.format(df_['name'])))

    # layout parameters
    geo_scatter_.update_layout(
            # title_text = '2014 US city populations<br>(Click legend to toggle traces)',
            showlegend = False,
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)',
            )
    )
    
    return geo_scatter_


# too much data, let's slim it down to top_10
top_10_cities = cities_df.sort_values('pop', ascending=False).head(10)

# create plotly visualizations
bar_ = create_bar_chart(top_10_cities)
geo_ = create_geo_scatter(top_10_cities)


# create UI components 
# dropdown 

# get list of cities names as strings 
cities_ = top_10_cities['name']

dd_1 = dcc.Dropdown(
    cities_,
    cities_[:2], # by default select first two 
    id="cities-dd",
    placeholder="Select a city",
    multi=True
)

# instantiate the dash app 
app = Dash(__name__)

# app layout 
app.layout = [
    html.Div(children="US City Populations", style={'textAlign':'center'}),
    dd_1,
    dcc.Graph(figure=bar_, id="cities-bar-chart"),
    dcc.Graph(figure=geo_, id="cities-geo-scatter")
]

# we want to register a call back 
@callback(
    Output('cities-bar-chart', 'figure'),
    Output('cities-geo-scatter', 'figure'),
    Input('cities-dd', 'value')
)
def update_graph(value):
   
    # filter the dataframe by selected value 
    filter_ = cities_df['name'].isin(value) # filter by selected values
    cities_sel_df = cities_df[filter_] 
    
    # recreates a new bar chart after filtering
    return create_bar_chart(cities_sel_df), create_geo_scatter(cities_sel_df)

    
app.run(debug=True, port=5000)
