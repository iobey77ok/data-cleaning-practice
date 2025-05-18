#%%
import pandas as pd
df = pd.read_csv('teststudent.csv')
df
# %%
import seaborn as sns
import matplotlib.pyplot as plt

# plot the line
sns.lineplot(data=df, x='Week', y='Quiz Score', hue='learning method', marker='o')
plt.title('Quiz Score Trend by Learning Method')
plt.show()

# %%
# from sklearn.linear_model import LinearRegression

# # extract digit from string
# # note: ML only works with numeric value
# df['week_num'] = df['Week'].str.extract(r'(\d+)').astype(int)

# # X = independent varaible that we think it influences Quiz score
# X = df[['Writing Score', 'Reading Score', 'week_num']]
# # Y = dependent variable
# y = df['Quiz Score']

# model = LinearRegression()
# model.fit(X, y)

# predictions = model.predict(X)


# %%
# df['predicted_quiz'] = predictions

# print(df[['Student Name','Week', 'Quiz Score', 'predicted_quiz']])

# %%
# plt.figure(figsize=(10, 6))
# sns.scatterplot(data=df, x='Quiz Score', y='predicted_quiz', hue='learning method')
# plt.plot([df['Quiz Score'].min(), df['Quiz Score'].max()],
#          [df['Quiz Score'].min(), df['Quiz Score'].max()],
#          color='gray', linestyle='--')  # Ideal prediction line
# plt.title('Actual vs Predicted Quiz Scores')
# plt.xlabel('Actual Quiz Score')
# plt.ylabel('Predicted Quiz Score')
# plt.show()

# %%

# this section is for predicting future with guessing input
# *** hardcoded ***
import pandas as pd

# Simulate future data for Method A and B
future_data = pd.DataFrame({
    'Writing Score': [4, 4, 5, 5, 5, 5, 4, 4, 5, 5, 5, 5],
    'Reading Score': [80, 82, 85, 87, 88, 90, 78, 80, 82, 85, 87, 90],
    'week_num': [3, 4, 5, 6, 7, 8, 3, 4, 5, 6, 7, 8],
    'learning method': ['A']*6 + ['B']*6
})

#%%
X_future = future_data[['Writing Score', 'Reading Score', 'week_num']]
future_data['predicted_quiz'] = model.predict(X_future)

# %%

# predicted quiz score
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
sns.lineplot(data=future_data, x='week_num', y='predicted_quiz', hue='learning method', marker='o')
plt.title('Predicted Quiz Scores (Next 6 Weeks)')
plt.xlabel('Week Number')
plt.ylabel('Predicted Quiz Score')
plt.show()

# %%


# this section is using past data to predict
# but we used avergae method first

# find avg score of each quiz by learning method
avg_scores = df.groupby('learning method')[['Writing Score', 'Reading Score']].mean()
print(avg_scores)

future_weeks = list(range(3, 9))  # Weeks 3 to 8

# generate future records
future_data = pd.DataFrame([
    {
        'week_num': week,
        'Writing Score': avg_scores.loc[method, 'Writing Score'],
        'Reading Score': avg_scores.loc[method, 'Reading Score'],
        'learning method': method
    }
    for week in future_weeks
    for method in avg_scores.index
])

future_data
# %%
X_future = future_data[['Writing Score', 'Reading Score', 'week_num']]
future_data['predicted_quiz'] = model.predict(X_future)

# %%
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.lineplot(data=future_data, x='week_num', y='predicted_quiz', hue='learning method', marker='o')
plt.title('Predicted Quiz Scores (Based on Past Averages)')
plt.xlabel('Week')
plt.ylabel('Predicted Quiz Score')
plt.xticks(future_weeks)
plt.grid(True)
plt.show()

# the trend is decreasing
# ------------------------------------------

# %%

df['week_num'] = df['Week'].str.extract(r'(\d+)').astype(int)

# Calculate trend (slope) for each method and score type
trends = df.groupby('learning method').apply(
    lambda group: pd.Series({
        'writing_slope': group[['week_num', 'Writing Score']].corr().iloc[0,1] * (group['Writing Score'].std() / group['week_num'].std()),
        'reading_slope': group[['week_num', 'Reading Score']].corr().iloc[0,1] * (group['Reading Score'].std() / group['week_num'].std()),
        'writing_start': group.loc[group['week_num'].idxmin(), 'Writing Score'],
        'reading_start': group.loc[group['week_num'].idxmin(), 'Reading Score']
    })
)

trends
# %%

future_weeks = list(range(3, 9))

# Simulate scores increasing with slope
future_data = pd.DataFrame([
    {
        'week_num': week,
        'Writing Score': trends.loc[method, 'writing_start'] + trends.loc[method, 'writing_slope'] * (week - 1),
        'Reading Score': trends.loc[method, 'reading_start'] + trends.loc[method, 'reading_slope'] * (week - 1),
        'learning method': method
    }
    for week in future_weeks
    for method in trends.index
])

future_data
# %%
X_future = future_data[['Writing Score', 'Reading Score', 'week_num']]
future_data['predicted_quiz'] = model.predict(X_future)

plt.figure(figsize=(10, 6))
sns.lineplot(data=future_data, x='week_num', y='predicted_quiz', hue='learning method', marker='o')
plt.title('Predicted Quiz Scores with Improvement Trend')
plt.xlabel('Week')
plt.ylabel('Predicted Quiz Score')
plt.xticks(future_weeks)
plt.grid(True)
plt.show()

# %%
