import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
fandango = pd.read_csv("fandango_scrape.csv")
print(fandango.head())
print(fandango.describe())
#relation btw popularity and rating
print(plt.figure(figsize=(10,4),dpi=150))
print(sns.scatterplot(data=fandango,x='RATING',y='VOTES'))
print(plt.show())

#calculate the correlation btw column
print(fandango.corr())
fandango['YEAR'] = fandango['FILM'].apply(lambda title:title.split('(')[-1].replace(')',','))
print(fandango['YEAR'].value_counts())

#COUNT OF MOVIE PER YEAR WITH PLOT
print(sns.countplot(data=fandango,x='YEAR'))
print(plt.show())

#10 MOVIES WITH HIEGHEST VOTES
print(fandango.nlargest(10,'VOTES'))

#MOVIES WITH NO VOTE
no_votes = fandango['VOTES']==0 
print(no_votes.sum())

fan_reviewes= fandango[fandango['VOTES']>0]
print(plt.figure(figsize=(10,4),dpi=150))
print(sns.kdeplot(data=fan_reviewes ,x='RATING', clip=[0,5],fill=True,label='True rating'))
print(sns.kdeplot(data=fan_reviewes,x='STARS',clip=[0,5],fill=True,label='Stars Displayed'))
print(plt.legend(loc=(1.05,0.5)))
print(plt.show())

#calculate the diff with STAR-RATING, round this diff to nearest decimal point
fan_reviewes["STARS_DIFF"] = fan_reviewes['STARS'] - fan_reviewes['RATING'] 
fan_reviewes['STARS_DIFF'] = fan_reviewes['STARS_DIFF'].round(2)
print(fan_reviewes)

#DISPLAY THE NO OF TIME CERTAIN DIFFERENCE ACCURS
print(plt.figure(figsize=(12,4),dpi=150))
print(sns.countplot(data=fan_reviewes,x='STARS_DIFF', palette='magma'))
print(plt.legend(loc=(1.05,0.5)))

print(plt.show())

print(fan_reviewes[fan_reviewes['STARS_DIFF']==1])

#READ IN THE ALL SITE SCORES
all_sites= pd.read_csv("all_sites_scores.csv")
print(all_sites.head())
print(all_sites.describe())

# CREAT A SCATTER PLOT USING RELATION BTW RT CRITIC REVIEWS AND USER REVIEWS

plt.figure(figsize=(10,4),dpi=150)
sns.scatterplot(data=all_sites, x='RottenTomatoes',y='RottenTomatoes_User')
plt.xlim(0,100)
plt.ylim(0,100)
#print(plt.show())

all_sites['ROTTEN_DIFF']= all_sites['RottenTomatoes']- all_sites['RottenTomatoes_User']
all_sites['ROTTEN_DIFF'].apply(abs).mean()

#PLOT DIFF BTW RT CRITIC RATING AND RT USER RATING
plt.figure(figsize=(10,4),dpi=150)
sns.histplot(data= all_sites,x='ROTTEN_DIFF',kde=True,bins=25)
print(plt.title("Rt critic scores minus Rt User score"))
print(plt.show())

#ABSOLUTE DIFF
plt.figure(figsize=(10,4),dpi=200)
sns.histplot(x=all_sites['ROTTEN_DIFF'].apply(abs),bins=25,kde=True)
print(plt.title("Abs Difference between RT Critics Score and RT User Score"))
#print(plt.show())

print('5 movies user loves but critics hate')
print(all_sites.nsmallest(5, 'ROTTEN_DIFF')[['FILM','ROTTEN_DIFF']])

print("Critics love, but Users Hate")
all_sites.nlargest(5,'ROTTEN_DIFF')[['FILM','ROTTEN_DIFF']]

#metacritic
plt.figure(figsize=(10,4),dpi=150)
sns.scatterplot(data=all_sites,x='Metacritic',y='Metacritic_User')
plt.xlim(0,100)
plt.ylim(0,10)
print(plt.show())

plt.figure(figsize=(10,4),dpi=150)
sns.scatterplot(data=all_sites,x='Metacritic_user_vote_count',y='IMDB_user_vote_count')
print(plt.show())

print(all_sites.nlargest(1,'IMDB_user_vote_count'))
print(all_sites.nlargest(1,'Metacritic_user_vote_count'))

df = pd.merge(fandango,all_sites,on='FILM',how='inner')
print(df.info())
print(df.head())
df['RT_Norm'] = np.round(df['RottenTomatoes']/20,1)
df['RTU_Norm'] =  np.round(df['RottenTomatoes_User']/20,1)
df['Meta_Norm'] = np.round(df['Metacritic']/20,1)
df['Meta_U_Norm'] =  np.round(df['Metacritic_User']/20,1)
df['IMDB_Norm']= np.round(df['IMDB']/20,1)
print(df.head())

norm_scores = df[['STARS','RATING','RT_Norm','RTU_Norm','Meta_Norm','Meta_U_Norm','IMDB_Norm']]
print(norm_scores.head())
fig, ax = plt.subplots(figsize=(15,6),dpi=150)
sns.kdeplot(data=norm_scores,clip=[0,5],shade=True,palette='Set1',ax=ax)
print(plt.show())  

def move_legend(ax, new_loc, **kws):
    old_legend = ax.legend_
    handles = old_legend.legendHandles
    labels = [t.get_text() for t in old_legend.get_texts()]
    title = old_legend.get_title().get_text()
    ax.legend(handles, labels, loc=new_loc, title=title, **kws)

fig, ax = plt.subplots(figsize=(15,6),dpi=150)
sns.kdeplot(data=norm_scores,clip=[0,5],shade=True,palette='Set1',ax=ax)
move_legend(ax,"upper left")
print(plt.show()) 

fig, ax = plt.subplots(figsize=(15,6),dpi=150)
sns.kdeplot(data=norm_scores[['RT_Norm','STARS']],clip=[0,5],shade=True,palette='Set1',ax=ax)
move_legend(ax,"upper left")
print(plt.show())

plt.subplots(figsize=(15,6),dpi=150)
sns.histplot(norm_scores,bins=50)
print(plt.show())

sns.clustermap(norm_scores,cmap='magma',col_cluster=False)
print(plt.show())

norm_films = df[['STARS','RATING','RT_Norm','RTU_Norm','Meta_Norm','Meta_U_Norm','IMDB_Norm','FILM']]
norm_films.nsmallest(10,'RT_Norm')

print('\n\n')
plt.figure(figsize=(15,6),dpi=150)
worst_films = norm_films.nsmallest(10,'RT_Norm').drop('FILM',axis=1)
sns.kdeplot(data=worst_films,clip=[0,5],shade=True,palette='Set1')
plt.title("Ratings for RT Critic's 10 Worst Reviewed Films");
print(plt.show())
print(norm_films.iloc[25])