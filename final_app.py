# Imports
import os
import sys
import pickle
import spotipy
import spotipy.util as util
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, GradientBoostingClassifier, AdaBoostClassifier, VotingClassifier
from xgboost import XGBClassifier

# A function to deal with outliers in tempo
# The range of tempos will be limited to range from 100 to 200
def tempo_adjuster(tempo):
    
    # Divide any tempo over 200 by 2
    if tempo > 200:
        tempo /= 2
        return tempo
    
    # Multiply any tempo under 100 by 2
    elif tempo < 100:
        tempo *= 2
        return tempo
    
    # Leave all other tempos alone
    else:
        return tempo


# Get the username from terminal
username = sys.argv[1]

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f'.cache-{username}')
    token = util.prompt_for_user_token(username)

# Create a Spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token)

# User information
user = spotifyObject.current_user()
display_name = user['display_name']

# Begin user interface
while True:

    # Welcome prompt
    print()
    print()
    print('Welcome to EDM Genre Classifier ' + display_name + '!')
    print()
    print('1 - Search')
    print('2 - Exit')
    print()
    choice = input('Your choice: ')
    print()
    
    # Begin search
    if choice == '1':
    
        # Select a song or artist
        choice = '0'
        while choice == '0':
            print()
            query = input('Enter an EDM song or artist: ')
            print()

            # Search Spotify for results from the query
            results = spotifyObject.search(query, limit=20)
            # A list of track results
            results_list = results['tracks']['items']

            # Check if any search results came up
            if len(results_list) == 0:
                print()
                print('No results for that search!')
                continue
                
            # A dictionary to store the URI for each track in the results
            track_lookup = {}

            # Display a menu of song results
            for i in range(len(results_list)):
                print(str(i + 1) + ':', results_list[i]['artists'][0]['name'], '-', results_list[i]['name'])
                # populating the lookup dictionary
                track_lookup[str(i + 1)] = results_list[i]['uri']

            while True:
                # Prompt the user to pick from the menu
                print()
                choice = input('Enter the number for the correct track, or enter 0 to search again: ')
                print()

                # Account for invalid entries
                try:
                    if int(choice) not in range(21):
                        print('Please enter an integer between 0 and 20')
                        continue
                except ValueError:
                    print('Please enter an integer between 0 and 20')
                    continue

                # Option to search again
                if choice == '0':
                    break
                    
                break
            
            # Option to search again
            if choice == '0':
                continue
            
            break

        # Get the audio features for the chosen track and store them in a dataframe
        track_data = pd.DataFrame(spotifyObject.audio_features([track_lookup[choice]]))
            
        # Drop unnecessary columns
        track_data.drop([
            'analysis_url', 
            'id',
            'track_href', 
            'type', 
            'uri',
            'acousticness', 
            'key', 
            'instrumentalness', 
            'liveness', 
            'mode', 
            'speechiness', 
            'time_signature',
            'valence'
        ], axis=1, inplace=True)
            
        # Adjust the tempo if necessary
        track_data['tempo'] = track_data['tempo'].map(tempo_adjuster)
            
        # Create polynomial features up to 5 degrees
        pf = PolynomialFeatures(degree=5)
        # Training data
        track_data = pf.fit_transform(track_data)
            
        # Load the saved model
        with open('final_model.pkl', 'rb') as f:
            model = pickle.load(f)
            
        # Use the model to make a prediction
        print(model.predict(track_data)[0].upper())
        
    elif choice != '2':
        print("Please enter 1 or 2.")
        
    else:
        break