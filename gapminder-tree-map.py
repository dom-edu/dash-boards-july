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


# let's run the app 
app.run(debug=True,port=5001)