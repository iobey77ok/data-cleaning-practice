#%% 
import pandas as pd

df = pd.read_csv('Greenhouse Plant Growth Metrics.csv')
df

#%%
df.rename(columns={
    'Random': 'plant sample',
    'ACHP': 'average Photosynthesis Level',
    'PHR': 'plant height',
}, inplace=True)
# tells Pandas to modify the DataFrame directly 
# not returning a new one.
df

