import pandas as pd 
import plotly.express as px
from dash import Dash, html, dcc 


# load in data:
# data URL 
url = "https://raw.githubusercontent.com/matplotlib/sample_data/refs/heads/master/aapl.csv" 

# load aapl data into data frame 
aapl_df = pd.read_csv(url)

# instantiating app 
app = Dash()


# plotly line graphs 

open_fig = px.line(aapl_df, 
            x="Date", 
            y="Open")

volume_fig = px.line(aapl_df, 
            x="Date", 
            y="Volume")


# add layout 
app.layout = [
    # added a <div>Hello World</div>
    # children is the children element of a div tag which is the text field. 
html.Div([
    html.H1('AAPL Stock 1984-2008'), 
    dcc.Graph(figure=open_fig),
    dcc.Graph(figure=volume_fig),
], style={'textAlign': 'center'})

]

if __name__ == '__main__':
    app.run(debug=True)
