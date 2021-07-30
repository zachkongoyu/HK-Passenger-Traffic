import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

d = dict()
ytd = datetime.date.today() - datetime.timedelta(days=1)

for date_ in pd.date_range('20200124', ytd):
    print(date_.strftime('%Y-%m-%d'))
    date__ = date_.strftime('%Y%m%d')

    response = requests.get(f'https://www.immd.gov.hk/eng/stat_{date__}.html')
    soup = BeautifulSoup(response.content)

    regions = [region.text for region in soup.findAll('td', headers='Control_Point')]

    Hong_Kong_Residents_Arrival = [data.text for data in soup.findAll('td', headers='Hong_Kong_Residents_Arrival')]
    Mainland_Visitors_Arrival = [data.text for data in soup.findAll('td', headers='Mainland_Visitors_Arrival')]
    Other_Visitors_Arrival = [data.text for data in soup.findAll('td', headers='Other_Visitors_Arrival')]
    Total_Arrival = [data.text for data in soup.findAll('td', headers='Total_Arrival')]

    Hong_Kong_Residents_Departure = [data.text for data in soup.findAll('td', headers='Hong_Kong_Residents_Departure')]
    Mainland_Visitors_Departure = [data.text for data in soup.findAll('td', headers='Mainland_Visitors_Departure')]
    Other_Visitors_Departure = [data.text for data in soup.findAll('td', headers='Other_Visitors_Departure')]
    Total_Departure = [data.text for data in soup.findAll('td', headers='Total_Departure')]    

    for i, region in enumerate(regions):
        try:
            temp_d = {date_.strftime('%Y-%m-%d') : {
                'Hong_Kong_Residents_Arrival' : Hong_Kong_Residents_Arrival[i], 
                'Mainland_Visitors_Arrival' : Mainland_Visitors_Arrival[i],
                'Other_Visitors_Arrival' : Other_Visitors_Arrival[i],
                'Total_Arrival' : Total_Arrival[i],
                'Hong_Kong_Residents_Departure' : Hong_Kong_Residents_Departure[i],
                'Mainland_Visitors_Departure' : Mainland_Visitors_Departure[i],
                'Other_Visitors_Departure' : Other_Visitors_Departure[i],
                'Total_Departure' : Total_Departure[i]}}

            temp_df = pd.DataFrame(temp_d)
            
            if region not in d:
                d[region] = temp_df
            else:
                d[region] = pd.concat([d[region], temp_df], axis=1)
        except:
            break

for k, v in d.items():
    v.T.to_csv(f"{k}.csv")