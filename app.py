import dash
from dash import Input, Output, State,dcc, html,callback
from dash_iconify import DashIconify
import ml
import openai

app = dash.Dash("MLAssistant",suppress_callback_exceptions=True)

app.layout = html.Div(id="screen", children=[
    html.Div(id="top_bar", children=[
        dcc.ConfirmDialog(id='api_alert',message='Please,refresh and enter a valid API Key before doing anything'),
        dcc.Input(id="api_key", type="text", placeholder="Enter your OpenAI API key here"),
        html.Div(id="icons", children=[
            html.A(href="https://github.com/AlexandreDps/DashGPT_Challenge", target="_blank",children=[
            DashIconify(icon="ion:logo-github", width=50, color="black")
            ]),
        html.A(href="https://www.linkedin.com/in/alexandre-descomps/", target="_blank",children=[
            DashIconify(icon="fa:linkedin", width=50,color='blue')
            ]),
        ])
    ]),
    html.Div(id="line1",className="line", children=[
        html.Div(id="monster", children= [
            html.Div(id="eyes", children=[
                html.Div(className="eye", children=[
                    html.Div(id='left_eye')
                ]),
                html.Div(className="eye", children= [
                    html.Div(id='right_eye')
                ])
            ]),
            html.Div(id="mouth",children=[
                dcc.Upload(id='upload-data',multiple=False, children=[
                    html.P("Drag and drop or Select a CSV file to build a machine learning model")
                ])
            ])
        ]),
        html.Div(id="speech1",className="speech", children=[
            html.P("Hello, my name is Jasper. I'll be your machine learning assistant !"),
            html.P("Let's start this journey together. Feed me with a CSV file containing a few columns for the parameters and one representing the data to be predicted")
        ])
    ]),
    dcc.Loading(id="loading_1", children=[
        html.Div(id="line2",className="line")
    ]),
    html.Div(id="line3",className="line",children=[
        dcc.Loading(id="loading_2")
    ])
])

@callback(Output('line2', 'children'),
          Output('mouth', 'style'),
          Output('upload-data', 'style'),
          Output('upload-data', 'disabled'),
          Output('api_key', 'disabled'),
          Output('api_alert', 'displayed'),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'),
          State('api_key', 'value'),
          prevent_initial_call=True)
def update_output(contents, names, api_key):
    try:
        openai.api_key = api_key
        df,res = ml.parse_content(contents,names)
        selection = html.Div(className="center",id="line2_style", children=[
            dcc.Store(id='data_store', data=df.to_json()),
            html.Div([html.P(res)],className="speech"),
            html.Label("Select the type of problem : ",className='underline'),
            dcc.RadioItems(["Regression","Classification","Multi-Classification"],inline=True,id="problem_type"),
            html.Label("Select the variable to predict : ",className='underline'),
            dcc.RadioItems(df.columns,inline=True,id="variable_to_predict"),
            html.Button('Train Model', id='train_model', n_clicks=0)
        ])
        style = {'animation': 'happy 1s ease-out forwards'}
        style2 = {'animation': 'dissapear 0.3s ease-out forwards'}
        api_alert = False
        return selection,style,style2,True,True,api_alert
    except:
        api_alert=True
        return None,None,None,False,False,api_alert

@callback(
    Output('loading_2', 'children'),
    Input('train_model', 'n_clicks'),
    State("problem_type",'value'),
    State("variable_to_predict","value"),
    State("data_store","data"),
    prevent_initial_call=True
)
def train_model(n_clicks,problem,variable,df):
    try:
        if n_clicks>0:
            res,advices,fig = ml.train_model(df,problem,variable)
            advices = advices.split("\n")
            p_content = []
            p_content.append(html.P("Good Work ! Jasper got some advices to improve your score :"))
            for i in advices:
                p_content.append(html.P(i))
            res = html.Div(className="center", children=[html.P(res),
                            html.P("We have chosen to display the most important variables only whose score exceeds 1%. These scores correspond to the impact of variables on the prediction."),
                            dcc.Graph(figure=fig),
                            html.Div(p_content, className="speech", id="speech3"),
                            html.Button("Download The Model", id="btn_download"),
                            dcc.Download(id="download_model")
                            ])
            return res
    except:
        res = html.Div(className="center", children=[
            html.P('This is an invalid selection, change the variable to predict and/or the type of model'),
        ])
        return res

@callback(
    Output("download_model", "data"),
    Input("btn_download", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "catboost_model.cmb"
    )

if __name__ == '__main__':
    app.run_server(debug=True)