import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

df = pd.read_excel("data/consumer_sentinel_data_book_2018_data_1/State_Ranking.xlsx")
states = pd.read_csv("data/consumer_sentinel_data_book_2018_data_1/states.csv")
res = df.merge(states, on='State', how='left')

class Visualize():
    # Choropleth chart
    def choropleth(self):
        fig = go.Figure(data=go.Choropleth(
            locations=res['Abbreviation'], # Spatial coordinates
            z = res['Reports per 100K Population'].astype(float), # Data to be color-coded
            locationmode = 'USA-states', # set of locations match entries in `locations`
            colorscale = 'Reds',
            colorbar_title = "per 100K Population",
        ))

        fig.update_layout(
            title_text = '2018 US Fraud Reports by State',
            geo_scope='usa', # limite map scope to USA
        )
        return fig

    # Pie Chart
    def reportsByContactMethods(self):
        fig = plt.figure()
        contact = pd.read_csv("data/consumer_sentinel_data_book_2018_data_1/2018_CSN_Fraud_Reports_by_Contact_Method.csv",header=2)
        contact=contact.drop([6,7,8,9,10])
        contact["Percentage"]=[float(i.strip('%'))/100 for i in contact["Percentage"]]
        fig = go.Figure(data=[go.Pie(
                        labels=contact['Contact Method'],
                        values=contact['Percentage'],
                        textinfo='percent',
                        hoverinfo='label+percent'
        )])
        fig.update_layout(title_text = 'Reports by Contact Methods')
        return fig

    # Bar Chart
    def amountByContactMethods(self):
        fig = plt.figure()
        contact = pd.read_csv("data/consumer_sentinel_data_book_2018_data_1/2018_CSN_Fraud_Reports_by_Contact_Method.csv",header=2)
        contact=contact.drop([6,7,8,9,10])
        contact["Total $ Lost"]=[int(i[1:-1])*1000000 for i in contact["Total $ Lost"]]
        fig = go.Figure(data=[
            go.Bar(x=contact["Contact Method"], y=contact["Total $ Lost"], marker_color='royalblue')
        ])
        fig.update_layout(title_text = 'Amount by Contact Methods')
        return fig
    
    # Pie Chart
    def amountByPaymentMethods(self):
        pmt = pd.read_csv("data/consumer_sentinel_data_book_2018_data_1/2018_CSN_Fraud_Reports_by_Payment_Method.csv", header=2, encoding='windows-1252')
        pmt = pmt.drop([9, 10, 11, 12, 13, 14, 15])
        pmt[" Total $ Loss "] = [int(i.replace(',', '')[1:-1]) for i in pmt[" Total $ Loss "]]

        fig = go.Figure(data=[go.Pie(
                        labels=pmt['Payment Method'],
                        values=pmt[' Total $ Loss '],
                        textinfo='percent',
                        hoverinfo='label+percent',
                        hole=.3
        )])
        fig.update_layout(title_text = 'Amount by Payment Methods')
        return fig
    
# Uncomment below line to run functions in this file
# Visualize().choropleth()
