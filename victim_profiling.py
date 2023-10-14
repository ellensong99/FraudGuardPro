# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 20:19:24 2023

@author: quanz
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pickle


# DATA CLEANING
file_path = "data/victim_profiling.tsv"
data = pd.read_csv(file_path, sep='\t')
# print(data['V3023A'].unique())

# Selecting and renaming columns
relevant_columns = ['SC214A', 'V3014', 'V3084', 'V3085', 'V4478_1', 'V4500_1', 'V4498_1']
data_filtered = data[relevant_columns]
column_rename = {
    'SC214A': 'Household Income',
    'V3014': 'Age (Allocated)',
    'V3084': 'Sexual Orientation',
    'V3085': 'Gender Identity at Birth',
    'V4478_1': 'Activity at Time of Incident',
    'V4500_1': 'Amount of Pay Lost',
    'V4498_1': 'Total Number of Days Lost'
}
data_renamed = data_filtered.rename(columns=column_rename)

# Cleaning the independent variables
replacements = {
    'Sexual Orientation': {8: np.nan, 9: np.nan},
    'Gender Identity at Birth': {3: np.nan, 4: np.nan, 8: np.nan, 9: np.nan},
    'Activity at Time of Incident': {11: np.nan, 95: np.nan, 96: np.nan, 99: np.nan}
}
data_renamed.replace(replacements, inplace=True)

# Cleaning dependent variables
data_renamed['Total Number of Days Lost'] = pd.to_numeric(data_renamed['Total Number of Days Lost'], errors='coerce').replace([997, 998, 999], np.nan).fillna(0)
data_renamed['Amount of Pay Lost'] = pd.to_numeric(data_renamed['Amount of Pay Lost'], errors='coerce').replace({99997: np.nan, 99998: np.nan, 99999: np.nan}).fillna(0)

# Ensure Non-Blank Entries for key columns
required_cols = ['Household Income', 'Age (Allocated)', 'Sexual Orientation', 'Gender Identity at Birth', 'Activity at Time of Incident']
data_cleaned = data_renamed.dropna(subset=required_cols).copy()

# Handling Categorical Variables with One-Hot Encoding
data_encoded = pd.get_dummies(data_cleaned, columns=[ 'Sexual Orientation', 'Gender Identity at Birth', 'Activity at Time of Incident'])

# Standardizing data for clustering
scaler = StandardScaler()
scaling_columns = ['Household Income', 'Age (Allocated)', 'Total Number of Days Lost', 'Amount of Pay Lost']
data_encoded[scaling_columns] = scaler.fit_transform(data_encoded[scaling_columns])

# save the cleaned data
output_file_path = "data/victim_profiling_cleaned.csv"
data_encoded.to_csv(output_file_path, index=False)

all_columns = data_encoded.columns
# print(all_columns)


# Find the optimal number of clusters using the Elbow method
# distortions = []
# K = range(1, 10)
# for k in K:
#     kmeanModel = KMeans(n_clusters=k)
#     kmeanModel.fit(data_encoded)
#     distortions.append(kmeanModel.inertia_)

# plt.figure(figsize=(10, 6))
# plt.plot(K, distortions, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Distortion')
# plt.title('The Elbow Method showing the optimal k')
# plt.show()

# Assuming an optimal number of clusters 
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k)
clusters = kmeans.fit_predict(data_encoded)
data_cleaned['Cluster'] = clusters
# print("Shape of data_encoded:", data_encoded.shape)



def assign_to_cluster(user_input, columns):
    df_encoded = pd.DataFrame([user_input], columns=columns)
    for col in all_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    df_encoded = df_encoded[all_columns]
    
    df_encoded[scaling_columns] = scaler.transform(df_encoded[scaling_columns])
    
    print("Shape of transformed user input:", df_encoded.shape)
    
    
    return kmeans.predict(df_encoded)[0]



def display_cluster_message(cluster_assigned):
    # Introduction
    intro_message = """Based on our comprehensive analysis of fraud-related incidents, we've identified three distinct demographic profiles that have had varying experiences with fraud. <br>These groups, or 'clusters' as we refer to them, offer insights into patterns of fraud victimization and how different demographics might be impacted:<br>

1. Young Low-Income Victims: Primarily consisting of younger individuals with modest incomes, this group has been fortunate to experience only minimal disruptions due to fraud.<br>
2. Middle-Aged, Wealthier Targets: This group is characterized by middle-aged individuals in higher income brackets. Despite their affluence, they too have reported minimal disruptions, which might suggest stronger protective measures or awareness.<br>
3. High-Impact Victims: A smaller but notably affected group, these individuals have faced significant disruptions from fraudulent activities, indicating the severity of incidents they've encountered.<br>

As we delve deeper into each cluster, we'll provide tailored advice and insights based on the characteristics and experiences of each group. Let's begin by understanding where you might fit in.<br><br>"""

    # Cluster Messages
    cluster_messages = {
        0: "Based on the provided information, you align with a demographic primarily comprising younger individuals with lower household incomes. <br>The good news is that individuals in this category typically report minimal disruptions due to fraud. It's possible that, despite having lower incomes, individuals in this group may have fewer assets vulnerable to fraudulent activities, or have adopted newer technological means to protect themselves. <br>We advise staying updated on the latest security protocols and being cautious about sharing personal details.",
        
        1: "Your profile suggests you are part of a demographic that mainly consists of middle-aged individuals who are in a higher income bracket. <br>While affluence might sometimes make people in this category attractive targets for fraudsters, the reported disruptions due to fraud are minimal. <br>This could suggest that individuals like you are either more vigilant, have robust security measures in place, or perhaps the fraudulent attempts have been less severe. <br>Continue practicing safe digital habits, regularly updating passwords, and monitoring financial transactions closely.",
        
        2: "Your profile indicates that you may belong to a demographic that, while smaller in number, has unfortunately experienced significant disruptions due to fraud. <br>It's concerning to note that people in this category report notably higher 'days lost' due to the impacts of fraud. <br>It's essential for individuals in this group to be particularly vigilant. <br>Consider seeking professional advice on enhancing security measures, regularly monitoring your accounts for unusual activity, and being wary of suspicious communications.<br>Remember, prevention is better than cure."
    }

    # Display the messages
    print(intro_message)
    print("\n" + "="*40 + "\n")
    print(cluster_messages[cluster_assigned])
    return intro_message + cluster_messages[cluster_assigned]

    
# Save the scaler
with open('data/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Function to load scaler and standardize user input
def standardize_input(values):
    with open('data/scaler.pkl', 'rb') as f:
        scaler_loaded = pickle.load(f)
    return scaler_loaded.transform([values])[0]

def get_input_from_options(prompt, options):
    # for i, option in enumerate(options, 1):
        # print(f"{i}. {option}")
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Please enter a number.")


def prepare_data_for_clustering(household_income, age, sexual_orientation, gender_identity, activity, amount_pay_lost,total_days_lost):

    # Encoding the race
    # Before encoding:
   
    # Encoding the sexual orientation
    sexual_orientation_dict = {
        'Lesbian or gay': 'Sexual Orientation_1.0',
        'Straight, that is, not lesbian or gay': 'Sexual Orientation_2.0',
        'Bisexual': 'Sexual Orientation_3.0',
        'Something else': 'Sexual Orientation_4.0',
        'I don\'t know the answer': 'Sexual Orientation_5.0',
        'Refused': 'Sexual Orientation_6.0'
    }
    # sexual_orientation_encoded = [1 if sexual_orientation_dict.get(sexual_orientation) == key else 0 for key in sexual_orientation_dict.values()]
    sexual_orientation_encoded = [
    1 if sexual_orientation == key else 0
    for key in sexual_orientation_dict.keys()
]
    # Encoding the gender identity
    gender_identity_dict = {
        'Male': 'Gender Identity at Birth_1.0',
        'Female': 'Gender Identity at Birth_2.0'
    }
    # gender_identity_encoded = [1 if gender_identity_dict.get(gender_identity)== key else 0 for key in gender_identity_dict.values()]
    gender_identity_encoded = [
    1 if gender_identity == key else 0
    for key in gender_identity_dict.keys()
]
    # Encoding the activity
    activity_dict = {
        'Work or on duty': 'Activity at Time of Incident_1.0',
        'On way t/f work': 'Activity at Time of Incident_2.0',
        'On way t/f school': 'Activity at Time of Incident_3.0',
        'On way t/f other': 'Activity at Time of Incident_4.0',
        'Shop, errands': 'Activity at Time of Incident_5.0',
        'Attend school': 'Activity at Time of Incident_6.0',
        'Leisure from home': 'Activity at Time of Incident_7.0',
        'Sleeping': 'Activity at Time of Incident_8.0',
        'Other activities at home': 'Activity at Time of Incident_9.0',
        'Other': 'Activity at Time of Incident_10.0'
    }
    activity_encoded = [1 if activity_dict.get(activity) == key else 0 for key in activity_dict.keys()]

   
    values_to_scale = [[household_income, age, amount_pay_lost, total_days_lost]]
    scaled_values = scaler.transform(values_to_scale)[0]

    household_income = scaled_values[0]
    age = scaled_values[1]
    amount_pay_lost = scaled_values[2]
    total_days_lost = scaled_values[3]


    # Merge the standardized and encoded values
    features = [household_income, age] + sexual_orientation_encoded + gender_identity_encoded + activity_encoded +[amount_pay_lost, total_days_lost]

    return np.array(features)



# if __name__ == '__main__':
    # Capturing user input
class Cluster():
    def victim_profile(self, amount_pay_lost, total_days_lost, household_income, age, sexual_orientation,
                       gender_identity, activity):
        user_data = prepare_data_for_clustering(household_income, age, sexual_orientation, gender_identity, activity, amount_pay_lost, total_days_lost)
        assigned_cluster = assign_to_cluster(user_data, all_columns)

        return display_cluster_message(assigned_cluster)
    
# Uncomment below line to run functions in this file
# Cluster().victim_profile(1,1,1,1,"Bisexual", "Female", "Attend School")

