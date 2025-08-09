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
countries_ = gapminder_df['country'].unique()

dd_1 = dcc.Dropdown(
    years_, 
    years_[0], 
    id='year-dd'
) 

dd_2 = dcc.Dropdown(
    countries_,
    countries_[0],
    id='countries-dd' 
)

def create_tree_map(df_):
    """
    creates a plotly tree map from a dataframe 
    """
    treemap_ = px.treemap(df_, 
                        path=[px.Constant("world"), 
                                'continent', 
                                'country'], 
                        values='pop',
                        color='lifeExp',
                        #   hover_data=['iso_alpha'],
                        color_continuous_scale='RdBu',
                    # color_continuous_midpoint=np.average(df_['lifeExp'], weights=gapminder_df['pop']))
                    )
    return treemap_

def create_scatterplot(df_):
    """
    creates a plotly scatter plot from a dataframe 
    """
    return px.scatter(x=df_['year'], y=df_['pop'])

# instantiate figures
treemap_ = create_tree_map(gapminder_df)
scatter_ = create_scatterplot(gapminder_df)

# create a scatter plot 

# define layout to make dash happy 
app.layout = [
    dd_1,
    html.H2(children="Tree map of Country Populations", 
            style={'textAlign': 'center'}, 
            id="tm-title"),
    dcc.Graph(figure=treemap_, id="treemap-fig"),
    dd_2,
    html.H2(children="Populations Growth for Country", 
            style={'textAlign': 'center'}, 
            id="sp-title"),
    dcc.Graph(figure=scatter_, id='sp-fig')
]

@callback(
    Output('treemap-fig','figure'),
    Input('year-dd','value')
)
def update_graph(value):
    """
    Updates the treemap figure to work with a single value
    """

    # filter our dataframe by year that is passed 

    # year is equal to the value selected in the dropdown 
    filter_ = gapminder_df['year'] == value
    filtered_df = gapminder_df[filter_]

    # make a new treemap 
    new_tree_map = create_tree_map(filtered_df)

    # return the new tree map to be updated in the graph object 
    return new_tree_map
# let's run the app 

@callback(
    Output('tm-title','children'),
    Input('year-dd','value')
)
def update_title(value):
    """
    Updates the title of the tree map h2 element
    """

    h2_text = f"Tree map of Country Populations for {value}"
    return h2_text


@callback(
    Output('sp-fig','figure'),
    Input('countries-dd', 'value')
)
def update_scatter(value):
    """
    filters data by selected country
    updates scatter plot 
    """
    # for matching selected country
    filter_ = gapminder_df['country'] == value

    # filter data
    filtered_data = gapminder_df[filter_]

    return create_scatterplot(filtered_data)

app.run(debug=True,port=5001)