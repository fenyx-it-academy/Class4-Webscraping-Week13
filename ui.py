import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import psycopg2
import plotly.graph_objects as go
import pandas as pd
import pandas.io.sql as sqlio

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def get_database(click=0, model='', year=0, km=1000000, color='', price=10000000, city=''):
    global df_all, df_filtered
    
    ##### Database queryleri ve sonuclari
    conn = psycopg2.connect('dbname=auto user=postgres password=Fsm1453.')
    cursor = conn.cursor()

    query_1 = f"SELECT model, year, km, color, price, city FROM cars ORDER BY year ASC;"
    cursor.execute(query_1)
    the_data = cursor.fetchall()
    df_all = pd.DataFrame(the_data, columns=[desc[0] for desc in cursor.description]) 
    
    if click>0:
        query_2= f"SELECT model, year, km, color, price, city FROM cars WHERE (model LIKE '%{model}%') and (year>={year}) and (km<={km}) and (color LIKE '{color}%') and (price<={price}) and (city LIKE '{city}%') order by price asc;"
        cursor.execute(query_2)
        the_data = cursor.fetchall()
        df_filtered= pd.DataFrame(the_data, columns=[desc[0] for desc in cursor.description])
    else:
        pass
   
    cursor.close()
    conn.commit()
    conn.close()
    
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
                html.Br(), # ustten bosluk icin                           
                dcc.Input(id='model', type='text', placeholder='Model'),
                dcc.Input(id='year', type='number', placeholder='Year'),
                dcc.Input(id='km', type='number', placeholder='KM'),
                dcc.Input(id='color', type='text', placeholder='Color'),
                dcc.Input(id='price', type='number', placeholder='Price'),
                dcc.Input(id='city', type='text', placeholder='City'),
                html.Br(),
                html.Br(),
                html.Button('Import', id='import', n_clicks=0),
                html.Button('Filter', id='filter', n_clicks=0),
                html.Br(),
                html.Br(),
                
                html.Div(id='place')
               

])

## Callback fonksiyonu
@app.callback(
    Output(component_id='place', component_property='children'),
    
    [Input(component_id='import', component_property='n_clicks'),
    Input(component_id='filter', component_property='n_clicks'),
    Input(component_id='city', component_property='n_clicks')],
    
    [State(component_id='model', component_property='value'),
     State(component_id='year', component_property='value'),
     State(component_id='km', component_property='value'),
     State(component_id='color', component_property='value'),
     State(component_id='price', component_property='value'),
     State(component_id='city', component_property='value')]
    )

def save(n_clicks1, n_clicks2, n_clicks3, value1, value2, value3, value4, value5, value6):
    global df_all, df_filtered
    
    ctx = dash.callback_context
    button = ctx.triggered[0]['prop_id'].split('.')[0]
    
    data_table = None
    
    if n_clicks1>0:
        if button == 'import':
            get_database(0, value1, value2, value3, value4, value5, value6)
            dat = df_all
            

        elif button == 'filter':
            get_database(n_clicks2, value1, value2, value3, value4, value5, value6)
            dat = df_filtered
        
        data_table = dash_table.DataTable(
                    id='table_all',
                    data=dat.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in dat.columns],
                    style_cell={'textAlign': 'center', 'width': '100px', 'minWidth': '100px', 'maxWidth': '100px'},
                    fixed_rows={'headers': True, 'data': 0},
                    style_header={'fontWeight': 'bold'},
                    page_size=10,
                    selected_rows=[],
                    style_table={'overflowX': 'auto'},
                    editable=True )

    return [data_table]
                         
if __name__ == '__main__':
    app.run_server(debug=False)


