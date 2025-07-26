from dash import Dash, html, dcc 

# intantiating app 
app = Dash()

# add layout 
app.layout = [
    # added a <div>Hello World</div>
    # children is the children element of a div tag which is the text field. 
html.Div([
    html.H1('Hello Dash'), 
    html.Div([
        html.P('Dash converts Python classes into HTML'),
        html.P("This conversion happens behind the scenes by Dash's JavaScript front-end")
    ]),
    dcc.Graph()
], style={'textAlign': 'center'})

]

if __name__ == '__main__':
    app.run(debug=True)
