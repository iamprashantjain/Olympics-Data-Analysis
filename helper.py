import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0
    if year == 'OverAll' and country == 'OverAll':
        temp_df = medal_df
    elif year == 'OverAll' and country != 'OverAll':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'OverAll' and country == 'OverAll':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif year != 'OverAll' and country != 'OverAll':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
        x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

        x['Gold'] = x['Gold'].astype(int)
        x['Silver'] = x['Silver'].astype(int)
        x['Bronze'] = x['Bronze'].astype(int)
        x['Total '] = x['total'].astype(int)

    return x


def medal_tally(df):
	medal_tally = df.drop_duplicates(subset=['Team', 'region', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
	medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
																							 ascending=False).reset_index()
	medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

	medal_tally['Gold'] = medal_tally['Gold'].astype(int)
	medal_tally['Silver'] = medal_tally['Silver'].astype(int)
	medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
	medal_tally['Total '] = medal_tally['Total'].astype(int)
	return medal_tally


def country_year_list(df):
	years = df['Year'].unique().tolist()
	years.sort()
	years.insert(0,'OverAll')

	country = np.unique(df['region'].dropna().values).tolist()
	country.sort()
	country.insert(0,'OverAll')

	return years, country



# def participating_nations_plot(df):
#     participating_nations = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index()
#     participating_nations.rename(columns={'index': 'Year', 'Year': 'No of Countries'}, inplace=True)
#     return participating_nations
#
#
# def no_of_events_plot(df):
#     no_of_events = df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index()
#     no_of_events.rename(columns={'index':'Year','Year':'No. of Events'},inplace=True)
#     return no_of_events


def data_plot(df,col):
    data_plot = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index()
    data_plot.rename(columns={'index':'Year','Year':col},inplace=True)
    return data_plot


def most_decorated_athlete(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'OverAll':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def country_wise_medal(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    # fig = px.line(final_df,x='Year',y='Medal')
    # fig.show()
    return final_df


def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_athlete(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def athlete_personal_info(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != "OverAll":
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    men = df[df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = df[df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final

