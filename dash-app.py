from dash import Dash, html

# intantiating app 
app = Dash()

# add layout 
app.layout = [
    # added a <div>Hello World</div>
    # children is the children element of a div tag which is the text field. 
    html.Div(children='Hello World')
]

if __name__ == '__main__':
    app.run(debug=True)
