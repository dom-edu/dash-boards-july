import numpy as np 
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc ,  Input, Output,callback


# load in the gapminder data 
URL = "https://raw.githubusercontent.com/plotly/datasets/refs/heads/master/gapminder_unfiltered.csv"

# read into pandas dataframe  
gapminder_df = pd.read_csv(URL)


# let's instantiate the dash app 
app = Dash(__name__) 

# dash components 

# drop down menu 
years_ = gapminder_df['year']

dd_1 = dcc.Dropdown(
    years_, 
    years_[0], 
    id='year-dd'
) 

# tree map 
treemap_ = px.treemap(gapminder_df, 
                      path=[px.Constant("world"), 
                            'continent', 
                            'country'], 
                      values='pop',
                      color='lifeExp',
                    #   hover_data=['iso_alpha'],
                    color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(gapminder_df['lifeExp'], weights=gapminder_df['pop']))

# define layout to make dash happy 
app.layout = [
    dd_1,
    dcc.Graph(figure=treemap_, id="treemap-fig")
]

@callback(
    Output('treemap-fig','figure'),
    Input('year-dd','value')
)
def update_graph(value):

    # filter our dataframe by year that is passed 

    # year is equal to the value selected in the dropdown 
    filter_ = gapminder_df['year'] == value
    filtered_df = gapminder_df[filter_]

    # make a new treemap 
    new_tree_map = px.treemap(filtered_df, 
        path=[px.Constant("world"), 
            'continent', 
            'country'], 
        values='pop',
        color='lifeExp',
    #   hover_data=['iso_alpha'],
    color_continuous_scale='RdBu',
    color_continuous_midpoint=np.average(filtered_df['lifeExp'], weights=filtered_df['pop']))

    # return the new tree map to be updated in the graph object 
    return new_tree_map




# let's run the app 
app.run(debug=True,port=5001)