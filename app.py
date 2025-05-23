import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Data (bu yerda o'zing json datangni qo'y)
df = pd.read_json('Results.json')
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['Year'] = df['OrderDate'].dt.year

# KPIlar
total_sales = df['SalesAmount'].sum()
unique_customers = df['CustomerKey'].nunique()
avg_discount = df['DiscountAmount'].mean()

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H2("Sales Dashboard"),
    html.Div([
        html.Div([
            html.H4("Total Sales"),
            html.P(f"{total_sales:,.2f}"),
        ], style={
            'padding': '20px', 'background': '#f1f1f1', 'border-radius': '12px', 'width': '180px', 'display': 'inline-block', 'margin-right': '15px', 'textAlign': 'center'
        }),
        html.Div([
            html.H4("Unique Customers"),
            html.P(f"{unique_customers}"),
        ], style={
            'padding': '20px', 'background': '#f1f1f1', 'border-radius': '12px', 'width': '180px', 'display': 'inline-block', 'margin-right': '15px', 'textAlign': 'center'
        }),
        html.Div([
            html.H4("Avg. Discount"),
            html.P(f"{avg_discount:.2f}"),
        ], style={
            'padding': '20px', 'background': '#f1f1f1', 'border-radius': '12px', 'width': '180px', 'display': 'inline-block', 'textAlign': 'center'
        }),
    ], style={'margin-bottom': '30px'}),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
        value=sorted(df['Year'].unique())[0],
        clearable=False
    ),
    dcc.Graph(
        id='sales-bar',
        config={'displayModeBar': False},
              ),
])

@app.callback(
    Output('sales-bar', 'figure'),
    Input('year-dropdown', 'value')
)
def update_chart(selected_year):
    filtered = df[df['Year'] == selected_year]
    fig = px.bar(
        filtered,
        x='EnglishProductName',
        y='SalesAmount',
        title=f'Sales Amount by Product ({selected_year})'
    )
    fig.update_layout(xaxis_tickangle=-45, height=600)
    return fig

if __name__ == '__main__':
    app.run(debug=False, port=8050)