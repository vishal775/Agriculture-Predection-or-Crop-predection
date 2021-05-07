from bs4 import BeautifulSoup 
import requests
from pandas import ExcelWriter
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import urllib.request
import time
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) 
        return True
    except:
        return False

def inter():
     time.sleep(1)
     if connect():
          print( 'Internet Connected')
          start()
          
     else:
          print('No Internet Connection!')
          print('Retrying to connect')
          inter()
         
def predict(a,b,climate):
     count=0
     c=b.upper()
     strList = a.split()
     newString = ''
     for val in strList:
          count+=1
          if count >= 2:
               newString += val.capitalize()
          else:
               newString += val.capitalize()+ ' '
     d=newString
     raindata = pd.read_csv("F:/Agriprediction/Tamilnadu agriculture yield data.csv")
     if d in set(raindata['State_Name']) and c in set(raindata['District_Name']):
          #print(set(raindata['District_Name']))
          r = raindata[raindata['District_Name'].str.contains(c, na=False)]
          writer = ExcelWriter('F:/Agriprediction/PythonExport.xlsx')
          r.to_excel(writer,'Sheet1',index=False)
          writer.save()
          dat = pd.read_excel("F:/Agriprediction/PythonExport.xlsx")
          con='Whole Year'
          s = dat[dat['Season'].str.contains(con, na=False)]
         # writer = ExcelWriter('F:/Agriprediction/PythonExport.xlsx')
          dat1 = pd.read_excel("F:/Agriprediction/PythonExport.xlsx")
          con1=climate
          s1 = dat1[dat1['Season'].str.contains(con1, na=False)]
          bsten=s.nlargest(5,['Production Quantity in Kilogram'])
          bsten1=s1.nlargest(5,['Production Quantity in Kilogram'])
          ge=bsten.drop_duplicates(subset=['Season', 'Crop'], keep="first")
          ge1=bsten1.drop_duplicates(subset=['Season', 'Crop'], keep="first")
          writer2 = ExcelWriter('F:/Agriprediction/PythonExport.xlsx')
          ge.to_excel(writer2,sheet_name = 'Whole Year',index=False)
          ge1.to_excel(writer2,sheet_name = climate,index=False)
          writer2.save()
          print('\nThe climate is '+climate)
          print('======================================================================================================')
          print('The suitable crop for this climate :\n')
         # store="Whole Year crops are \n"+ge+"\n"+climate+" crops are \n"+ge1
          print("Whole Year crops are\n ")
          print(ge)
          print('======================================================================================================')
          print("\n"+climate+" crops are\n ")
          print(ge1)
          print('======================================================================================================')     
     else:
          print('No state found in the database')
          
def start():
     a=input('State:')
     b=input('Enter District:')
     c=b.upper()
     city = a
     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=cf670ba7b5d11004cd051eef972d1a40&units=metric'.format(city)
     res = requests.get(url)
     data = res.json()
     temp = data['main']['temp']
     wind_speed = data['wind']['speed']
     latitude = data['coord']['lat']
     longitude = data['coord']['lon']
     description = data['weather'][0]['description']
     #print('\n=========climate is '+description+'=========\n')  #to check the present climate which not mentioned below you can check here
     if 'overcast clouds' in description:
          name='Temperature is {t} degree celcius, Wind Speed  {w} m/s, Latitude  {l}, Longitude  {lo}, It is rainy'.format(t=temp,w=wind_speed,l=latitude,lo=longitude,d=description)
          predict(a,b,'Rainy')
     elif 'haze' in description or 'scattered clouds' in description or 'broken clouds' in description:
          name='Temperature is {t} degree celcius, Wind Speed  {w} m/s, Latitude  {l}, Longitude  {lo}, It is sunny'.format(t=temp,w=wind_speed,l=latitude,lo=longitude,d=description)
          predict(a,b,'Sunny')
     elif 'clear sky' in description:
          name='Temperature is {t} degree celcius, Wind Speed  {w} m/s, Latitude  {l}, Longitude  {lo}, It is clear sky'.format(t=temp,w=wind_speed,l=latitude,lo=longitude,d=description)
          predict(a,b,'Clear sky')
     else:
          name='Temperature is {t} degree celcius, Wind Speed  {w} m/s, Latitude  {l}, Longitude  {lo}, It is {d}'.format(t=temp,w=wind_speed,l=latitude,lo=longitude,d=description)
          print(name)
          predict(a,b,'Whole Year')
inter()


          


