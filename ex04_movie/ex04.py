#%%
import pandas as pd
df = pd.read_csv('movies.csv')
df
#%%
df.columns = df.columns.str.lower()
df
#%%
df.rename(columns={
    'one-line' : 'brief summary',
    'stars' : 'actors'
}, inplace=True)
df
#%% replacing \n
df['genre'] = df['genre'].str.replace(r'[\n]', '', regex=True)
df

#%% apply replacing to all columns selected
# when selecting many cols need to be in dataframe
df[['genre', 'brief summary', 'actors']] = df[['genre', 'brief summary', 'actors']].apply(
    lambda x : x.str.replace(r'[\n]', '', regex=True)
)
df

#%%
df['brief summary'] = df['brief summary'].replace('Add a Plot', 'Plot not Available')
df
# %%
mask1 = df.eval('rating.isnull()')
mask1
# %%
df[~mask1]

#%% delete runtime
df = df.drop(columns=['runtime','gross'], axis=1)
df
# %%
# extract director and actors
# make it into separate columns

df['director'] = df['actors'].str.extract(r'Director:\s*([\w\s,]+)', expand=False)
df['actor'] = df['actors'].str.extract(r'Stars?:\s*([\w\s,]+)', expand=False)
df = df.drop('actors', axis = 1)
df
# %%

mask2 = df['rating'].isnull() | df['director'].isnull() | df['actor'].isnull()
df[~mask2]
# %%
df.dtypes
# %%
