import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://pickyourtrail.com/blog/wp-content/uploads/2016/08/20140204000881966198-original.jpg')


user_menu = st.sidebar.radio(
	'Select Options',
	('Medal Tally','Overall Analysis','Country wise Analysis','Athlete wise Analysis')
)

# st.dataframe(df)


if user_menu == 'Medal Tally':
	st.sidebar.header("Medal Tally")
	years,country = helper.country_year_list(df)

	selected_year = st.sidebar.selectbox("Select Year",years)
	selected_country = st.sidebar.selectbox("Select Country",country)

	medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

	if selected_year == "OverAll" and selected_country == "OverAll":
		st.title('All time Olympic medal tally')

	elif selected_year == "OverAll" and selected_country != "OverAll":
		st.title("Olympics Medals Won by " + selected_country)

	elif selected_year != "OverAll" and selected_country == "OverAll":
		st.title("Olympics Medal Tally in " + str(selected_year))

	elif selected_year != "OverAll" and selected_country != "OverAll":
		st.title("Olympics Medals Won by " + selected_country + " in " + str(selected_year))

	st.table(medal_tally)


elif user_menu == "Overall Analysis":
	editions = df['Year'].unique().shape[0] - 1
	cities = df['City'].unique().shape[0]
	sport = df['Sport'].unique().shape[0]
	athletes = df['Name'].unique().shape[0]
	nation = df['region'].unique().shape[0]
	events = df['Event'].unique().shape[0]


	st.title("Olympic Statistics")
	col1,col2,col3 = st.columns(3)
	with col1:
		st.header("Editions")
		st.write('How many Olympics happened?')
		st.markdown(editions)


	with col2:
		st.header("Hosts")
		st.write('How many cities hosted Olympics?')
		st.markdown(cities)


	with col3:
		st.header("Sports")
		st.write('How many different sports happened?')
		st.markdown(sport)

	col1, col2, col3 = st.columns(3)
	with col1:
		st.header("Athletes")
		st.write('How many Athletes participated?')
		st.markdown(athletes)

	with col2:
		st.header("Nations")
		st.write('How many Countries participated?')
		st.markdown(nation)


	with col3:
		st.header("Events")
		st.write('How many Events Happened?')
		st.markdown(events)


	# participating_nations = helper.participating_nations_plot(df)
	# fig = px.line(participating_nations, x='Year', y='No of Countries')
	# st.title("Participationg Nations Over the Years")
	# st.plotly_chart(fig)
	#
	# no_of_events = helper.no_of_events_plot(df)
	# fig = px.line(no_of_events, x='Year', y='No. of Events')
	# st.title("No of Events each the Years")
	# st.plotly_chart(fig)

	participating_nations = helper.data_plot(df,'region')
	fig = px.line(participating_nations, x='Year', y='region')
	st.title("Participationg Nations Over time")
	st.plotly_chart(fig)

	no_of_events = helper.data_plot(df,'Event')
	fig = px.line(no_of_events, x='Year', y='Event')
	st.title("No of Events Over time")
	st.plotly_chart(fig)


	participating_athletes = helper.data_plot(df,'Name')
	fig = px.line(participating_athletes, x='Year', y='Name')
	st.title("Athletes Over time")
	st.plotly_chart(fig)


	#heatmap
	st.title("No of Events in Every Sports")
	fig,ax = plt.subplots(figsize=(12,12))
	x = df.drop_duplicates(['Year', 'Sport', 'Event'])
	ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
				annot=True)
	st.pyplot(fig)


	st.title("Top Athletes")
	sport_list = df['Sport'].unique().tolist()
	sport_list.sort()
	sport_list.insert(0,'OverAll')

	selected_sport = st.selectbox('Select a Sport',sport_list)
	x = helper.most_decorated_athlete(df,selected_sport)
	st.table(x)


elif user_menu == "Country wise Analysis":
	st.sidebar.title("Countrywise Medal Tally")
	country_list = df['region'].dropna().unique().tolist()
	country_list.sort()

	selected_country = st.sidebar.selectbox('Select a Country',country_list)

	country_df = helper.country_wise_medal(df,selected_country)
	fig = px.line(country_df,x='Year',y="Medal")
	st.title(selected_country + " Medal Tally over the years")
	st.plotly_chart(fig)

	st.title("Medals in each category " + selected_country)
	pt = helper.country_event_heatmap(df,selected_country)
	fig, ax = plt.subplots(figsize=(12, 12))
	ax = sns.heatmap(pt,annot=True)
	st.pyplot(fig)

	st.title("Most Successfull Athlete of " + selected_country)
	top10_df = helper.most_successful_athlete(df,selected_country)
	st.table(top10_df)


elif user_menu == 'Athlete wise Analysis':
	athlete_df = df.drop_duplicates(subset=['Name', 'region'])
	x1 = athlete_df['Age'].dropna()
	x2 = athlete_df[athlete_df['Medal'] == "Gold"]['Age'].dropna()
	x3 = athlete_df[athlete_df['Medal'] == "Silver"]['Age'].dropna()
	x4 = athlete_df[athlete_df['Medal'] == "Bronze"]['Age'].dropna()
	fig = ff.create_distplot([x1, x2, x3, x4], ['OverAll Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
							 show_hist=False, show_rug=False)
	fig.update_layout(autosize=False,width=1000,height=600)
	st.title("Age wise Medals")
	st.plotly_chart(fig)



	famous_sport = df['Sport'].value_counts().nlargest(40).reset_index()['index'].tolist()
	x = []
	name = []
	for sport in famous_sport:
		temp_df = athlete_df[athlete_df['Sport'] == sport]
		x.append(temp_df[temp_df['Medal'] == "Gold"]["Age"].dropna())
		name.append(sport)
	fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
	st.title("Sports wise Age Distribution")
	st.plotly_chart(fig)



	# sport_list = df['Sport'].unique().tolist()
	# sport_list.sort()
	# sport_list.insert(0, 'Overall')
	#
	# st.title('Height Vs Weight')
	# selected_sport = st.selectbox('Select a Sport', sport_list)
	# temp_df = helper.athlete_personal_info(df, selected_sport)
	# fig, ax = plt.subplots()
	# ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
	# st.pyplot(fig)



	st.title("Men vs Women Participation")
	final = helper.men_vs_women(athlete_df)
	fig = px.line(final, x='Year', y=['Male', 'Female'])
	fig.update_layout(autosize=False, width=1000, height=600)
	st.plotly_chart(fig)
