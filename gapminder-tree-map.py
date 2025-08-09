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
    [countries_[0]],
    id='countries-dd', 
    placeholder="Select a country",
    multi=True

)

marks_ = {year : str(year) for year in range(years_.min(), years_.max(), 5)}

s_1 = dcc.Slider(years_.min(), 
                 years_.max(), 
                 5,
                 value=years_.median(),
                 marks = marks_, # fix for 2k showing up on each bullet point 
               id='year-slider'
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

# create a scatter plot 

def create_lineplot(df_):
    """
     creates a plotly line plot from a dataframe 
    """
    return px.line(df_, x="year", y="pop", color='country')


# instantiate figures
treemap_ = create_tree_map(gapminder_df)
# scatter_ = create_scatterplot(gapminder_df)
line_plot = create_lineplot(gapminder_df)



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
            id="lp-title-pop"),
    html.H2(children="Years:", 
            style={'textAlign': 'center'}, 
            id="lp-title-years"),       
    dcc.Graph(figure=line_plot, id='lp-fig'),
    s_1
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
def update_tm_title(value):
    """
    Updates the title of the tree map h2 element
    """

    h2_text = f"Tree map of Country Populations for {value}"
    return h2_text


@callback(
    Output('lp-fig','figure'),
    Input('countries-dd', 'value'),
    Input('year-slider', 'value')
)
def update_lp(val1, val2):
    """
    filters data by selected country
    updates scatter plot 
    """
    # for matching selected country
    filter_ = gapminder_df['country'].isin(val1)

    # for matching range slider values
    filter_2 = gapminder_df['year'] <= val2

    # filter data
    filtered_data = gapminder_df[filter_ & filter_2]

    return create_lineplot(filtered_data)


@callback(
    Output('lp-title-pop','children'),
    Input('countries-dd','value')

)
def update_lp_title_pop(value):

    countries_txt = ', '.join(value)
    h2_text = f"Population Growth for {countries_txt}"
    return h2_text

@callback(
    Output('lp-title-years','children'),
    Input('year-slider','value')
    
)
def update_lp_title_years(value):

    
    h2_text = f"Years: 1952 - {value}"
    return h2_text


app.run(debug=True,port=5001)