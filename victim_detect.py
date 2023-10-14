import pandas as pd
import numpy as np
from imblearn.over_sampling import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import accuracy_score, classification_report, \
    confusion_matrix
import math
from sklearn.model_selection import train_test_split


def data_clean(data_file):
    df = pd.read_csv(data_file)

    # Remove rows with missing values:
    df.dropna(inplace=True)

    # Remove duplicate rows:
    df.drop_duplicates(inplace=True)

    columns_to_drop = ["Numro d'identification / Number ID", "Country", "Pays",
                       "Complaint Received Type", "Type de plainte reue",
                       "Province/tat",
                       "Catgories thmatiques sur la fraude et la "
                       "cybercriminalit",
                       "Mthode de sollicitation", "Genre",
                       "Langue de correspondance", "Type de plainte",
                       "Date Received / Date reue",
                       "Province/State",
                       "Fraud and Cybercrime Thematic Categories",
                       "Complaint Type"]
    df.drop(columns=columns_to_drop, inplace=True)

    df_filtered = df[
        (df['Solicitation Method'] != 'Other/unknown')
        & (df['Language of Correspondence'] != 'Not Available')
        & (df['Victim Age Range / Tranche d\'ge des victimes'] !=
           '\'Not Available / non disponible')
        & (df["Solicitation Method"] != 'Not Available')
        & (df["Gender"] != 'Not Available')
        & (df["Gender"] != 'Unknown')
        & (df["Gender"] != 'Other')]

    # Make a copy of the filtered DataFrame
    df_filtered_copy = df_filtered.copy()

    # Rename the columns in the copied DataFrame
    df_filtered_copy.rename(columns={
        'Solicitation Method': 'Approaches',
        'Language of Correspondence': 'Language',
        'Victim Age Range / Tranche d\'ge des victimes': 'Age Range',
        'Dollar Loss /pertes financires': 'Dollar Loss',
        'Number of Victims / Nombre de victimes': 'Number of Victims'
    }, inplace=True)

    df_filtered_copy.to_csv('data/cleaned_file.csv', index=False)


def data_process(data_file):
    raw = pd.read_csv(data_file)

    # Create a copy of the DataFrame
    df = raw.copy()
    df['Dollar Loss'] = df['Dollar Loss'].apply(
        lambda x: float(x.replace('$', '').replace(',', '').strip()))

    # Perform one-hot encoding
    # List of columns to be one-hot encoded
    columns_to_encode = ["Gender", "Language", "Approaches", "Age Range"]

    # Use pd.get_dummies to perform one-hot encoding
    df_encoded = pd.get_dummies(df, columns=columns_to_encode)

    return df_encoded


def model_random_overresample(df, independent):

    # Train test split
    X = df[independent]
    y = df['Number of Victims']

    # Instantiate the oversampler
    oversampler = RandomOverSampler(sampling_strategy='minority')

    # Fit and transform the data
    X_resampled, y_resampled = oversampler.fit_resample(X, y)

    # Split the resampled data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_resampled,
                                                        y_resampled,
                                                        test_size=0.20)

    # creating a RF classifier
    clf = RandomForestClassifier(n_estimators=100)

    # Training the model on the training dataset
    clf.fit(X_train, y_train)

    # # performing predictions on the test dataset
    y_pred = clf.predict(X_test)

    # evaluation
    print("The evaluation index of the model: ")
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Precision:", metrics.precision_score(y_test, y_pred))
    print("Recall:", metrics.recall_score(y_test, y_pred))
    print("F1 Score:", metrics.f1_score(y_test, y_pred))
    # print("Confusion Matrix:\n", metrics.confusion_matrix(y_test, y_pred))
    #
    # # Calculate and display feature importances
    # feature_imp = pd.Series(clf.feature_importances_,
    #                         index=X.columns).sort_values(ascending=False)
    # print(feature_imp)

    # # Get model parameters
    # print(clf.get_params())
    #
    # # Get model metadata routing
    # print(clf.get_metadata_routing())
    #
    # Predict log probabilities of class labels for the test data
    # Predict class probabilities for the test data
    # proba = clf.predict_proba(X_test)
    #
    # # Handle cases where probabilities are very close to zero or one
    # epsilon = 1e-15  # Small constant to avoid division by zero
    # proba = np.maximum(epsilon, proba)
    # proba = np.minimum(1 - epsilon, proba)
    #
    # # Compute log probabilities
    # y_pred2 = np.log(proba)
    # print(y_pred2)
    # #
    return clf


# if __name__ == "__main__":
class Detect():
    def VictimDetect(self,gender, language, approach, age):
    
        # Raw data cleaning
        # This step is to clean the raw data, and output a cleaned data file
        # then we will only use the cleaned data file for the later analysis
        #data_clean('can_crime_data.csv')
        df = data_process('data/cleaned_file.csv')

        # Independent variables declaration
        independent = ['Gender_Female', 'Gender_Male',
                    'Gender_Prefer not to say', 'Language_English',
                    'Language_French',
                    'Approaches_Direct call',
                    'Approaches_Door to door/in person',
                    'Approaches_Fax', 'Approaches_Email', 'Approaches_Internet',
                    'Approaches_Internet-social network', 'Approaches_Mail',
                    'Approaches_Print', 'Approaches_Radio',
                    'Approaches_Television',
                    'Approaches_Text message', 'Approaches_Video Call',
                    'Age Range_\'1 - 9',
                    'Age Range_\'10 - 19', 'Age Range_\'100 ',
                    'Age Range_\'20 - 29',
                    'Age Range_\'30 - 39', 'Age Range_\'40 - 49',
                    'Age Range_\'50 - 59',
                    'Age Range_\'60 - 69', 'Age Range_\'70 - 79',
                    'Age Range_\'80 - 89',
                    'Age Range_\'90 - 99', 'Age Range_\'Business / Entreprise',
                    'Age Range_\'Deceased / Dcd']

        # Random Forest Model building with over_sampling technique
        rd_model = model_random_overresample(df, independent)
        gender_choice = 1 if gender == "Female" else 0
        language_choice = 1 if language == "English" else 0
        d={"Direct call":1, "Door to door/in person": 2, "Fax":3,
        "Email": 4,"Internet":5,"Internet-social network":6, "Mail":7,
        "Print":8,"Radio":9,"Television":10,"Text message": 11, "Video Call":12}
        approach_choice = d[approach]

        
        age_range_choice = math.floor(int(age)/10)+1

        # Create a blank data list with all values as 0
        sample_data = [0] * len(independent)

        # Replace values in the sample_data list based on user input
        sample_data[gender_choice-1] = 1
        sample_data[
            language_choice + 1] = 1
        sample_data[
            approach_choice + 4] = 1
        sample_data[
            age_range_choice + 16] = 1

        # Create a DataFrame with the same column names as your training data
        prediction_df = pd.DataFrame([sample_data], columns=independent)
        predicted_number_of_victims = rd_model.predict(prediction_df)

        if predicted_number_of_victims == 1:
            # print(
            #     "\nYou have a high probability to be scammed. Please be cautious!")
            return "\nYou have a high probability to be scammed. Please be cautious!"
        else:
            # print(
            #     "\nYou're probably not being scammed, but please still be careful.\n")
            return "\nYou're probably not being scammed, but please still be careful.\n"

# Uncomment below line to run functions in this file
# Detect().VictimDetect()