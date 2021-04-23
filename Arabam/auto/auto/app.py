import sys
import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import psycopg2
import pandas.io.sql as sqlio

external_stylesheets=[dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True


app.layout = html.Div(
    [        
    html.I("Lutfen sorgu yapmak istediginiz degerleri giriniz!"),
    html.Br(),
    dcc.Input(id="input1", type="text", placeholder="Model"),
    dcc.Input(id="input2", type="text", placeholder="Yil", debounce=True),
    dcc.Input(id="input3", type="text", placeholder="Renk"),
    dcc.Input(id="input4", type="text", placeholder="Kilometre"),
    dcc.Input(id="input5", type="text", placeholder="Fiyat"),
    dcc.Input(id="input6", type="text", placeholder="il"),
    html.Button('Bring data', id='bring-data-button', n_clicks=0),
    html.Br(),
    html.Br(),
    html.Div(id='place1')
    ]
)

# Connection parameters, yours will be different
param_dic = {
    "host"      : "localhost",
    "database"  : "Arabalar",
    "user"      : "postgres",
    "password"  : "pg05330477"
}

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    print("Connection successful")
    return conn


# GET DATAFRAME
# select cls, avg(math) from tbl_not group by cls order by cls
def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    
    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
    
    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df


@app.callback(
    [Output(component_id='place1', component_property='children')],
    [Input(component_id='bring-data-button', component_property='n_clicks')],
    [State(component_id="input1", component_property='value'),
    State(component_id="input2", component_property='value'),
    State(component_id="input3", component_property='value'),
    State(component_id="input4", component_property='value'),
    State(component_id="input5", component_property='value'),
    State(component_id="input6", component_property='value')]
)
def save(n,v1,v2,v3,v4,v5,v6):
    w = False
    q = "SELECT model, yil, renk, kilometre, fiyat, il FROM cars"
    t = "SELECT model, yil, renk, kilometre, fiyat, il FROM cars WHERE"
    if v1:
        t = t + " model LIKE '%"+ v1 +"%'"
        w = True
    if v2:
        if w:
            t = t + " AND"
        t = t + " yil LIKE '%"+ v2 +"%'"
        w = True
    if v3:
        if w:
            t = t + " AND"
        t = t + " renk LIKE '%"+ v3 +"%'"
        w = True
    if v4:
        if w:
            t = t + " AND"
        t = t + " kilometre LIKE '%"+ v4 +"%'"
        w = True
    if v5:
        if w:
            t = t + " AND"
        t = t + " fiyat LIKE '%"+ v5 +"%'"
        w = True
    if v6:
        if w:
            t = t + " AND"
        t = t + " il LIKE '%"+ v6 +"%'"
        w = True    
    
    if v1 or v2 or v3 or v4 or v5 or v6:
        q = t
    
    conn = connect(param_dic)
    df = postgresql_to_dataframe(conn, q, ("Model", "Yil", "Renk", "Kilometre", "Fiyat", "Il"))


    return [dash_table.DataTable(
                id='table_ratio',
                data=df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df.columns],
                style_cell={'textAlign': 'center', 'width': '30px', 'minWidth': '10px', 'maxWidth': '50px'},
                fixed_rows={'headers': True, 'data': 0},
                style_header={'fontWeight': 'bold'},
                style_table={'overflowX': 'auto'},
                editable=True)]


if __name__ == "__main__":
    app.run_server(debug=True)


