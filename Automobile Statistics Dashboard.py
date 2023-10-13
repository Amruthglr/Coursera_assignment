import pandas as pd
import numpy as np
import dash
from dash import dcc 
from dash import html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output

# Load the data using Pandas
# data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DV0101EN-Coursera/labs/v4/Final_Project/DV0101EN-Final_Assign_Part_2_Questions.py")
data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv")
# Initialize the dash app
app = dash.Dash(__name__)

# Set the title for dashboard
# app.title("Automobile Statistics Dashboard")

# List of years
year_list = [i for i in range(1983, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
                    #Adding title to the dashboard
                    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'Center', 'color': '#503D36', 'font-size':40}),

                    # Input Section for dropdown
                    html.Div([
                        html.Label("Select Statistics"),
                        dcc.Dropdown(
                            id = 'dropdown-statistics',
                            options=[
                                {'label': 'Yearly Statistics', 'value':'Yearly Statistics'},
                                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}],
                            value= 'Select Statistics',
                            placeholder= 'Select a statistics'
                        )
                    ]),

                    html.Div(dcc.Dropdown(
                                id = 'select-year',
                                options=[{'label':i, 'value':i} for i in year_list],
                                placeholder='Select year',
                                value = 'select-year',
                                # style={'textAlign': 'Center', 'color': '#503D36', 'font-size':40}

                    )),
                    html.Div([#TASK 2.3: Add a division for output display
                            html.Div(id='output-container', className='chart-grid', style={'display':'flex'}),])
])
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value' )
)

def update_input_container(selected_statistics):
    if  selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

@app.callback(
    Output(component_id ='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
    Input(component_id= 'select-year', component_property='value')]
    )

def update_output_container(selected_statistics, entered_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        #Plotting Line Graph
        plot1_data_R = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        plot1_fig_R = dcc.Graph(figure= px.line(plot1_data_R, x = 'Year', y = 'Automobile_Sales', title = 'Automobile sales fluctuation in Recession Period'))

        #Plotting Bar Chart
        plot2_data_R = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        plot2_fig_R = dcc.Graph(figure=px.bar(plot2_data_R, x = 'Vehicle_Type', y = 'Automobile_Sales', title = 'Average number of vehicles sold by vehicle type'))

        #Plotting Pie Chart
        plot3_data_R = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        plot3_fig_R = dcc.Graph(figure=px.pie(plot3_data_R, values='Advertising_Expenditure', names='Vehicle_Type', title = "Percentage of Advertising expenditure per vehicle type"))

        # Plotting Bar Chart
        plot4_data_R = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        plot4_fig_R = dcc.Graph(figure=px.bar(plot4_data_R, x ='unemployment_rate', y = 'Automobile_Sales', title='Effect of unemployment rate on vehicle type and sales'))

        # return [plot1_fig, plot2_fig, plot3_fig, plot4_fig]
        return[
            html.Div(className='chart-item', children=[html.Div(children=plot1_fig_R), html.Div(children=plot2_fig_R)]),
            html.Div(className='chart-item', children=[html.Div(children=plot3_fig_R), html.Div(children=plot4_fig_R)])
        ]

    elif (entered_year and selected_statistics == 'Yearly Statistics'):

        yearly_data = data[data['Year']== entered_year]

        #Plotting line chart
        plot1_data = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        plot1_fig = dcc.Graph(figure=px.line(plot1_data, x = 'Year', y = 'Automobile_Sales', title = 'Automobile sales fluctuation in whole period'))

        #Plotting line Chart
        plot2_data = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        plot2_fig = dcc.Graph(figure=px.line(plot2_data, x = 'Month', y = 'Automobile_Sales', title= 'Total Monthly Automobile sales'))

        #Plotting Bar Chart
        plot3_data = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        plot3_fig = dcc.Graph(figure=px.bar(plot3_data, x = 'Vehicle_Type', y = 'Automobile_Sales', title = 'Average number of vehicles sold during the given year' ))

        # Plotting Pie Chart
        plot4_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        plot4_fig = dcc.Graph(figure=px.pie(plot4_data, values= 'Advertising_Expenditure', names='Vehicle_Type', title = 'otal Advertisement Expenditure for each vehicle'))

        return [
            html.Div(className='chart-item', children=[html.Div(plot1_fig), html.Div(plot2_fig)]),
            html.Div(className='chart-item', children=[html.Div(plot3_fig), html.Div(plot4_fig)])
        ]
    else:
        return None

if __name__ == "__main__":
    app.run_server(debug=True)
    
