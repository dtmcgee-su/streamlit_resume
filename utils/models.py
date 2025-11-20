# This script will be used to generate models to alter be referenced on the site
##### Imports #####
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots

##### Data Cleaning, Merging #####
df_pitch_movement = pd.read_csv('./data/pitch_movement.csv')
df_pitch_stats = pd.read_csv('./data/pitch-arsenal-stats.csv')

df_pitch_movement['pitcherId_pitchType'] = df_pitch_movement['pitcher_id'].astype(str) + '_' + df_pitch_movement['pitch_type']
df_pitch_stats['pitcherId_pitchType'] = df_pitch_stats['player_id'].astype(str) + '_' + df_pitch_stats['pitch_type']
df_pitch_movement = df_pitch_movement.dropna()
df_pitch_movement.rename(columns={'last_name, first_name': 'pitcher_name'}, inplace=True)

# filter data for relevant columns
df_pitch_movement = df_pitch_movement[[
    'pitcher_name',	
    'pitcher_id',	
    'team_name_abbrev',	
    'pitch_hand',
    'pitch_type',
    'pitch_type_name',
    'avg_speed',
    'pitches_thrown',
    'total_pitches',
    'pitch_per',
    'pitcher_break_z',
    'pitcher_break_z_induced',
    'pitcher_break_x',
    'pitcherId_pitchType'
]]

df_pitch_stats = df_pitch_stats[[
    'ba',	
    'slg',	
    'woba',	
    'whiff_percent',	
    'k_percent',	
    'put_away',	
    'est_ba',	
    'est_slg',	
    'est_woba',	
    'hard_hit_percent',
    'pitcherId_pitchType'
]]


# left join on movement
df_merged = df_pitch_movement.merge(df_pitch_stats, on='pitcherId_pitchType', how='left', suffixes=('_movement', '_stats'))


PERFORMANCE_METRIC = 'whiff_percent'

##### Feature Engineering #####
# Defining elite pitch status based on whiff percentage
# The top 25% of pitches by whiff percentage will be considered "elite"
whiff_threshold = df_merged[PERFORMANCE_METRIC].quantile(0.75)

df_merged['is_elite'] = np.where(df_merged[PERFORMANCE_METRIC] >= whiff_threshold, 1, 0)

print(f"Total number of elite pitches in the dataset: {df_merged['is_elite'].sum()}")


##### Define Features #####
X_features=[
    'pitch_per',
    'pitcher_break_z_induced',
    'pitcher_break_x',
    'avg_speed',
    'est_ba',	
    'est_slg',	
    'est_woba',
    'hard_hit_percent',
    'pitch_hand',
    # 'pitch_type_name',
]

CATEGORICAL_FEATURES = [
    'pitch_hand',
    'pitch_type_name',
]

CONTINUOUS_FEATURES = [
    'pitch_per',
    'pitcher_break_z_induced',
    'pitcher_break_x',
    'avg_speed',
    'est_ba',	
    'est_slg',	
    'est_woba',
    'hard_hit_percent',
]


X = df_merged[X_features].copy()
X.dropna(inplace=True)

Y = df_merged['is_elite']
Y = Y[X.index] # Keep Y aligned with X

# # One hot encode categorical variables
# X = pd.get_dummies(X, columns=CATEGORICAL_FEATURES, drop_first=True)

scaler = StandardScaler()
X[CONTINUOUS_FEATURES] = scaler.fit_transform(X[CONTINUOUS_FEATURES])



##### Train/Test Split #####
X_train, X_test, Y_train, Y_test = train_test_split(
    X, 
    Y, 
    test_size=0.2, 
    random_state=42, 
    stratify=Y)



##### Model Training ######
random_forest_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced'
)

random_forest_model.fit(X_train, Y_train)

# Predict on test set
Y_pred = random_forest_model.predict(X_test)
Y_proba = random_forest_model.predict_proba(X_test)[:,1]




##### Model Evaluation #####
print('Model Evaluation')
print(classification_report(Y_test, Y_pred, target_names=['Non-Elite', 'Elite']))
print(f"ROC AUC Score: {roc_auc_score(Y_test, Y_proba): .4f}")

confusion_matrix = confusion_matrix(Y_test, Y_pred)
cm_df = pd.DataFrame(
    confusion_matrix, 
    index=['Actual Non-Elite', 'Actual Elite'], 
    columns=['Predicted Non-Elite', 'Predicted Elite']
)

# heatmap
fig_cm = go.Figure(data=go.Heatmap(
    z=confusion_matrix,
    x=['Predicted Non-Elite', 'Predicted Elite'],
    y=['Actual Non-Elite', 'Actual Elite'],
    colorscale='Blues',
    colorbar=dict(title='Count')
))

# add annotations
for i in range(len(confusion_matrix)):
    for j in range(len(confusion_matrix[0])):
        fig_cm.add_annotation(
            x=cm_df.columns[j], 
            y=cm_df.index[i], 
            text=str(confusion_matrix[i, j]),
            showarrow=False,
            font=dict(color="black" if confusion_matrix[i, j] < confusion_matrix.max() / 2 else "white", size=16)
        )

fig_cm.update_layout(
    title='Confusion Matrix: Pitch Elite Status Prediction',
    xaxis_title='Predicted Label',
    yaxis_title='True Label',
    yaxis=dict(autorange='reversed') # Makes the labels appear top-to-bottom
)

fig_cm.write_html('plotly_confusion_matrix.html')
print("Plotly Confusion Matrix saved as 'plotly_confusion_matrix.html'")
print("-" * 50)


##### Feature Importance #####
feature_importances = pd.Series(
    random_forest_model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)


df_fi = pd.DataFrame({
    'Feature': feature_importances.index,
    'Importance': feature_importances.values
})

fig_fi = px.bar(
    df_fi,
    x='Importance',
    y='Feature',
    orientation='h',
    title='Feature Importance for Predicting Elite Pitches',
    color='Importance',
    color_continuous_scale=px.colors.sequential.Viridis
)

fig_fi.update_layout(
    yaxis={'categoryorder':'total ascending'} 
)

fig_fi.write_html('plotly_feature_importance.html')
print("Plotly Feature Importance Plot saved as 'plotly_feature_importance.html'")