import requests
import streamlit as st
import re
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from client import RestClient
st.set_option('deprecation.showPyplotGlobalUse', False)
st.sidebar.title("Settings")
dataforseoapiemail = st.sidebar.text_input("Data for SEO email")
dataforseoapipass = st.sidebar.text_input("Data for SEO API password")
country = st.sidebar.selectbox('Which country would you like SERPs to be from', ('UK', 'US'))
keywords = st.sidebar.text_area("Keywords")
searchbutton = st.sidebar.button("Search");
st.title("What % of images have product schema?")
st.markdown("Find out what proportion of images for various SERPs are marked up with product schema. The data will look at the % of the top 100 results, and also the top 10.\n\nYou will need a DataforSEO API key to use this tool. You can <a href='https://app.dataforseo.com/register'>sign up to DataforSEO</a> and get free trial credit (enough for around 300 keywords). Once you have registered, you can see your credentials in your dashboard.",unsafe_allow_html=True)

if country == "UK":
	countrycode = 2826
elif country == "US":
	countrycode = 2840

if (searchbutton):
	with st.spinner("Loading..."):

			lines = keywords.split("\n")

			if keywords != "":
				
				st.title("Keyword results");
					
				numofTop10 = 0
				numofTop100 = 0

				for line in lines:
					countMatches = 0
					
						
					
					client = RestClient(dataforseoapiemail, dataforseoapipass)
					post_data = dict()
					post_data[len(post_data)] = dict(
						language_code="en",
						location_code=countrycode,
						keyword=line
					)

					response = client.post("/v3/serp/google/images/live/html", post_data)

					if response["status_code"] == 20000:
						m = re.findall("<a class=\"w.*? jsname=.*? jsaction=.*?<\/a>.*?<\/div>", response['tasks'][0]['result'][0]['items'][0]['html'])
						
						first10 = 1;
						firstpageresults = 0;
						for match in m:
							if (re.search("Click for product information", match)):
								countMatches += 1
								if first10 < 11:
									firstpageresults += 1;
							first10 += 1;
								
								
							
					else:
						st.text("error. Code: %d Message: %s" % (response["status_code"], response["status_message"]))
						

					
					st.subheader(line.title())
					index = ["Top 100 Results","Top 10 Results"]
					firstpageresultsPer = (firstpageresults / 10 ) * 100
					
					df = pd.DataFrame({'Product Schema': [countMatches, firstpageresultsPer],
						   'Non-Product Schema': [100 - countMatches, 100 - firstpageresultsPer]}, index=index)
					ax = df.plot.barh(stacked=True,legend=False,figsize=(5,1))
					plt.xlabel('% of images with product schema')
					st.pyplot()
					
					numofTop10 += firstpageresults
					numofTop100 += countMatches


				st.title("Average Results")
				st.markdown("Out of all keywords analysed, the data averages out at:")



				index = ["Top 100 Results","Top 10 Results"]
				firstpageresultsPer = (numofTop10 / (10 * len(lines) ) ) * 100
				totalresultsPer = (numofTop100 / (100 * len(lines) ) ) * 100

				df = pd.DataFrame({'Product Schema': [totalresultsPer,firstpageresultsPer],
					   'Non-Product Schema': [100 - totalresultsPer, 100 - firstpageresultsPer]}, index=index)
				ax = df.plot.barh(stacked=True,legend=False,figsize=(5,1))
				plt.xlabel('% of images with product schema')
				st.pyplot()

				st.success("Finished!")




