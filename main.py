import dash, matplotlib
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from phone import Phone
from visualize import Visualize
from victim_detect import Detect
from scam import Scam
from victim_profiling import Cluster

matplotlib.use('Agg')
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div([
    html.H1("FraudGuardPro"),
    
    html.Div([
        html.Label("Select a report type:"),
        dcc.Dropdown(
            id='report-type',
            options=[
                {'label': 'Fraud Report by State', 'value': 'state-report'},
                {'label': 'Reports by Contact Methods', 'value': 'contact-reports'},
                {'label': 'Amount by Contact Methods', 'value': 'contact-amount'},
                {'label': 'Amount by Payment Methods', 'value': 'payment-amount'}
            ],
            value='state-report'
        )
    ]),
    
    html.Div(id='report-output'),

    html.Div([
        html.H2("Search Phone Number"),
        html.Label("Enter the telephone number:"),
        dcc.Input(id='phone-input', type='text', value='', style={"margin-left": "15px"}),
        html.Br(),
        html.Button("Submit", id='phone-submit-button'),
        html.Div(id='phone-output')
    ]),


    html.Div([
        html.H2("Are You Scammed?"),
        html.Label("Select your gender:"),
        dcc.RadioItems(
            id='gender-input',
            options=[
                {'label': 'Female', 'value': 'Female'},
                {'label': 'Male', 'value': 'Male'},
                {'label': 'Prefer not to say', 'value': 'Prefer not to say'}
            ],
            value='white'
        ),
        html.Br(),  
        html.Label("Select your language:"),
        dcc.RadioItems(
            id='language-input',
            options=[
                {'label': 'English', 'value': 'English'},
                {'label': 'French', 'value': 'French'}
            ],
            value='white'
        ),
        html.Br(),  
        html.Label("Select the approach:"),
        dcc.Dropdown(
            id='approach-input',
            options=[
                {'label': 'Direct call', 'value': 'Direct call'},
                {'label': 'Door to door/in person', 'value': 'Door to door/in person'},
                {'label': 'Fax', 'value': 'Fax'},
                {'label': 'Email', 'value': 'Email'},
                {'label': 'Internet', 'value': 'Internet'},
                {'label': 'Internet-social network', 'value': 'Internet-social'},
                {'label': 'Mail', 'value': 'Mail'},
                {'label': 'Print', 'value': 'Print'},
                {'label': 'Radio', 'value': 'Radio'},
                {'label': 'Television', 'value': 'Relevision'},
                {'label': 'Text message', 'value': 'Text message'},
                {'label': 'Video Call', 'value': 'Video Call'},
            ],
            value='direct-call',
            style={'width': '55%', 'height':30}
        ),
        html.Br(),
        html.Label("Enter your age:"),
        dcc.Input(id='age-input', type='text', value='', style={"margin-left": "15px"}),
        html.Br(),
        html.Button("Submit", id='group-submit-button'),
        html.Div(id='group-output')
        
    ]),

    html.Div([
        html.H2("Discover your group!"),
        html.Label("What's the amount of money you think you have lost due to fraud so far?"),
        dcc.Input(id='amount-input', type='number', value="", style={"margin-left": "15px"}),
        html.Br(),  
        html.Label("How many days you think you have lost due to fraud so far?"),
        dcc.Input(id='days-input', type='number', value="", style={"margin-left": "15px"}),
        html.Br(),  
        html.Label("Enter your income:"),
        dcc.Input(id='income-input', type='text', value="", style={"margin-left": "15px"}),
        html.Br(),
        html.Label("Enter your age:"),
        dcc.Input(id='ages-input', type='text', value='', style={"margin-left": "15px"}),
        html.Br(),  
        html.Label("Select your Sexual Orientation:"),
        dcc.Dropdown(
            id='so-input',
            options=[{'label': 'Lesbian or gay', 'value': 'Lesbian or gay'}, 
                     {'label': 'Straight, that is, not lesbian or gay', 'value': 'Straight, that is, not lesbian or gay'}, 
                     {'label': 'Bisexual', 'value': 'Bisexual'}, 
                     {'label': 'Something else', 'value': 'Something else'}, 
                     {'label': "I don't know the answer", 'value': "I don't know the answer"}, 
                     {'label': 'Refused', 'value': 'Refused'}],
            value='',
            style={'width': '55%', 'height':30}
        ),
        html.Br(),
        html.Label("Select your gender:"),
        dcc.RadioItems(
            id='sex-input',
            options=[
                {'label': 'Female', 'value': 'Female'},
                {'label': 'Male', 'value': 'Male'},
            ],
            value='white'
        ),
        html.Br(),
        html.Label("Select your Activity at Time of Incident:"),
        dcc.Dropdown(
            id='activity-input',
            options=[{'label': 'Work or on duty', 'value': 'Work or on duty'}, 
                     {'label': 'On way t/f work', 'value': 'On way t/f work'}, 
                     {'label': 'On way t/f school', 'value': 'On way t/f school'}, 
                     {'label': 'On way t/f other', 'value': 'On way t/f other'}, 
                     {'label': 'Shop, errands', 'value': 'Shop, errands'}, 
                     {'label': 'Attend school', 'value': 'Attend school'}, 
                     {'label': 'Leisure from home', 'value': 'Leisure from home'}, 
                     {'label': 'Sleeping', 'value': 'Sleeping'}, 
                     {'label': 'Other activities at home', 'value': 'Other activities at home'}, 
                     {'label': 'Other', 'value': 'Other'}],
            value='',
            style={'width': '55%', 'height':30}
        ),
        html.Br(),
        html.Button("Submit", id='cluster-submit-button'),
        html.Div(id='cluster-output')
    ]),


    html.Div([
        html.H2("Identify Scam Emails"),
        html.Label("Copy your Email Here:"),
        dcc.Textarea(
            id='email-input',
            value='',
            style={'width': '100%', 'height': 200, 'resize': 'none'}
        ),
        html.Button("Submit", id='email-submit-button'),
        html.Div(id='email-output')
    ]),
])

# Define callback to update the report section based on the dropdown selection
@app.callback(
    Output('report-output', 'children'),
    [Input('report-type', 'value')]
)
def update_report(selected_report):
    if selected_report == 'state-report':
        return dcc.Graph(figure=Visualize().choropleth())
    elif selected_report == 'contact-reports':
        return dcc.Graph(figure=Visualize().reportsByContactMethods())
    elif selected_report == 'contact-amount':
        return dcc.Graph(figure=Visualize().amountByContactMethods())
    elif selected_report == 'payment-amount':
        return dcc.Graph(figure=Visualize().amountByPaymentMethods())

# Define callback to handle phone number search
@app.callback(
    Output('phone-output', 'children'),
    [Input('phone-submit-button', 'n_clicks')],
    [dash.dependencies.State('phone-input', 'value')]
)
def update_output_div(n_clicks, phone_number):
    if n_clicks is not None:
        result = Phone().search_phone_number(phone_number)  
        return html.Div(result)
    
# Define callback to handle if you are scammed
@app.callback(
    Output('group-output', 'children'),
    [Input('group-submit-button', 'n_clicks')],
    [dash.dependencies.State('gender-input', 'value'),
     dash.dependencies.State('language-input', 'value'),
     dash.dependencies.State('approach-input', 'value'),
     dash.dependencies.State('age-input', 'value')]
)
def update_user_info(n_clicks, gender, language, approach, age):
    if n_clicks:
        return html.P(Detect().VictimDetect(gender, language, approach, age))

# Define callback to handle which cluster you belong to    
@app.callback(
    Output('cluster-output', 'children'),
    [Input('cluster-submit-button', 'n_clicks')],
    [dash.dependencies.State('amount-input', 'value'),
     dash.dependencies.State('days-input', 'value'),
     dash.dependencies.State('income-input', 'value'),
     dash.dependencies.State('ages-input', 'value'),
     dash.dependencies.State('so-input', 'value'),
     dash.dependencies.State('sex-input', 'value'),
     dash.dependencies.State('activity-input', 'value')]
)
def update_user_info(n_clicks, amount, days, income, age, so, gender, activity):
    if n_clicks:
        ret = Cluster().victim_profile(amount, days, income, age, so, gender, activity)
        strlist= []
        for i in ret.split("<br>"):
            strlist.append(i)
            strlist.append(html.Br())
        return html.P(strlist)

# Define callback to handle if this is a scam email
@app.callback(
    Output('email-output', 'children'),
    [Input('email-submit-button', 'n_clicks')],
    [dash.dependencies.State('email-input', 'value')]
)
def update_output_email(n_clicks, email):
    if n_clicks:
        result = Scam().scam_email(email)  
        return html.Div(result)
    
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
