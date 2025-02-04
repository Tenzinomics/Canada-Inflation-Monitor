import pandas as pd

from stats_can import StatsCan
sc = StatsCan()

from dash import Dash, dcc, html
import plotly.graph_objects as go


#Inflation data table from statscan
#df = sc.table_to_df("18-10-0004-01")
#canada = df[df["GEO"]=="Canada"]  
#canada[canada["REF_DATE"]=="2024-11-01"] #change the date to the latest release


#Creating a dictionary variable to pull specific inflation series 
overallinfkey = {
"overall":"v41691232",
"core":"v41691233",
"allexmortgage":"v41691240",
"allexshelter":"v41691241",
"mortgageinterest":"v41691056"
}

#Pulling the data from statscan
df = sc.vectors_to_df(overallinfkey.values())
df.columns=list(overallinfkey.keys()) 


#Applying year over year change to the dataframe
df_yoy = df.pct_change(periods=12) * 100

df_yoy = df_yoy[df_yoy.index.year >= 2015].round(2)



#Creating the charts

#1. Overall CPI
chart1 = go.Figure()


chart1.add_trace(go.Scatter(x=df_yoy["overall"].index, y=df_yoy["overall"].values, mode='lines', name='inf1', line=dict(color='green')))


# Update layout for the second chart
chart1.update_layout(
    title="1. Overall CPI",
    #xaxis_title="% Year-Over-Year",
    yaxis_title="Year-Over-Year (%)",
    showlegend=False,

    # Disable zooming and scrolling
    dragmode=None,  # Disable drag (zoom)
    xaxis=dict(fixedrange=True),  # Disable zooming in x-axis
    yaxis=dict(fixedrange=True, 
            zeroline=True,           # Enable the zero line
            zerolinecolor="black",   # Set the zero line color to black
            zerolinewidth=1,),         # Set the width of the zero line),  # Disable zooming in y-axis

    title_font=dict(
        family="Arial, sans-serif",  # Choose the font family
        size=20,                    # Set the size of the title
        color="black",              # Set the color of the title
        weight="bold"               # Set the title to bold
    ),

    shapes=[
    # Add a rectangle (the shaded area)
        {
            'type': 'rect',
            'x0': df_yoy.index.min(),         # Start from the leftmost point (x-axis)
            'x1': df_yoy.index.max(),         # End at the rightmost point (x-axis)
            'y0': 1,               # Start at y=1
            'y1': 3,               # End at y=2
            'fillcolor': 'rgba(128, 128, 128, 0.3)',  # Gray color with transparency (0.3 opacity)
            'line': {
                'color': 'rgba(255, 255, 255, 0)',  # Transparent border
            },
        }
    ],

)


#2. Mortgage Interest CPI
chart2 = go.Figure()

chart2.add_trace(go.Scatter(x=df_yoy["mortgageinterest"].index, y=df_yoy["mortgageinterest"].values, mode='lines', name='inf2', line=dict(color='green')))

# Update layout for the second chart
chart2.update_layout(
    title="2. Mortgage Interest CPI",
    #xaxis_title="% Year-Over-Year",
    yaxis_title="Year-Over-Year (%)",
    showlegend=False,

    # Disable zooming and scrolling
    dragmode=None,  # Disable drag (zoom)
    xaxis=dict(fixedrange=True),  # Disable zooming in x-axis
        yaxis=dict(fixedrange=True, #disabling zooming in y-ax
            zeroline=True,           # Enable the zero line
            zerolinecolor="black",   # Set the zero line color to black
            zerolinewidth=1,),         # Set the width of the zero line),  # Disable zooming in y-axis

    title_font=dict(
        family="Arial, sans-serif",  # Choose the font family
        size=20,                    # Set the size of the title
        color="black",              # Set the color of the title
        weight="bold"               # Set the title to bold
    ),
)



#3. Overall CPI Ex. Mortgage Interest CPI
chart3 = go.Figure()

chart3.add_trace(go.Scatter(x=df_yoy["allexmortgage"].index, y=df_yoy["allexmortgage"].values, mode='lines', name='inf3', line=dict(color='green')))

# Update layout for the second chart
chart3.update_layout(
    title="3. Overall CPI Excluding Mortgage Interest",
    #xaxis_title="% Year-Over-Year",
    yaxis_title="Year-Over-Year (%)",
    showlegend=False,

    # Disable zooming and scrolling
    dragmode=None,  # Disable drag (zoom)
    xaxis=dict(fixedrange=True),  # Disable zooming in x-axis
        yaxis=dict(fixedrange=True, #disabling zooming in y-ax
            zeroline=True,           # Enable the zero line
            zerolinecolor="black",   # Set the zero line color to black
            zerolinewidth=1,),         # Set the width of the zero line),  # Disable zooming in y-axis

    title_font=dict(
        family="Arial, sans-serif",  # Choose the font family
        size=20,                    # Set the size of the title
        color="black",              # Set the color of the title
        weight="bold"               # Set the title to bold
    ),

    shapes=[
    # Add a rectangle (the shaded area)
        {
            'type': 'rect',
            'x0': df_yoy.index.min(),         # Start from the leftmost point (x-axis)
            'x1': df_yoy.index.max(),         # End at the rightmost point (x-axis)
            'y0': 1,               # Start at y=1
            'y1': 3,               # End at y=2
            'fillcolor': 'rgba(128, 128, 128, 0.3)',  # Gray color with transparency (0.3 opacity)
            'line': {
                'color': 'rgba(255, 255, 255, 0)',  # Transparent border
            },
        }
    ],

)




app = Dash(__name__)

app.layout = html.Div(
    children=[
        
        html.H1("Canada CPI Breakdown"),
        
        # First chart
        html.Div(
            children=[
                dcc.Graph(id="chart1", figure=chart1)
            ],
            style={"height": "100px", "width": "100px", "display": "inline","margin": "auto", "padding": "20px"}
        ),
        
        # Second chart
        html.Div(
            children=[
                dcc.Graph(id="chart2", figure=chart2)
            ],
            style={"height": "100px", "width": "100px", "display": "inline","margin": "auto", "padding": "20px"}
        ),

        # Third chart
        html.Div(
            children=[
                dcc.Graph(id="chart3", figure=chart3)
            ],
            style={"height": "100px", "width": "100px", "display": "inline","margin": "auto", "padding": "20px"}
        ),

    ]
)

# # Save the layout as a static HTML file without Dash interactivity
# def save_layout_to_html(app):
#     with open("dashboard_output.html", "w") as f:
#         f.write(app.index_string)

# # Save the app layout to an HTML file
# #save_layout_to_html(app)

# # Run the app
if __name__ == "__main__":
    #app.run_server(debug=True)
    app.run_server(port=8051)




