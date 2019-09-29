# Imports
import os
import sys
import spotipy
import spotipy.util as util
import pandas as pd

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

# Create a list of genres to collect songs from
genres = ['dubstep', 'house', 'trance', 'drum-and-bass']

# Create a list to store the audio features for each song collected
full_track_list = []

# Loop through each genre
for genre in genres:
    
    # Moniter the progress of the data collection
    print()
    print(f"Getting recommendations for {genre}...")
    
    # The recommendation method is limited to 100 songs at a time
    # This process must therefore be repeated many times to get as many songs as possible
    # There seem to be 1000 possible songs that Spotify can recommend for each genre
    # Running the loop 1500 times for each genre is enough to get them all
    for _ in range(1_500):
        
        # Pull 100 recommendations from the specified genre and store the JSON data
        tracks_json = spotifyObject.recommendations(seed_genres=[genre], limit=100)['tracks']

        # Create a list to store the URI for each song collected
        uri_list = []
        
        # Populate the list of URIs from the JSON data
        for track in tracks_json:
            uri_list.append(track['uri'])

        # Get the audio features for each song collected
        # These are stored as a list of dictionaries
        track_list = spotifyObject.audio_features(uri_list)

        # Loop through each song
        for i in range(len(track_list)):
            # Add an entry in each dictionary to store the genre
            track_list[i]['genre'] = genre

        # Add the group of tracks to the total list
        full_track_list.extend(track_list)

# Store the audio features in a dataframe
songs = pd.DataFrame(full_track_list)

# Drop all duplicates
songs.drop_duplicates(inplace=True)

# Save the dataframe as a csv file
songs.to_csv('data/songs.csv', index=False)



# Validation Data

# This dictionary contains 100 hand-picked songs (25 from each genre) and their corresponding genres
# These songs will serve as a validation dataset for subsequent models
val_dict = {
    'spotify:track:2qOS00vav7CVkOwfkkXktG': 'house',
    'spotify:track:6y1UtRcHQU07aUs3oxZ8Yn': 'house',
    'spotify:track:7hU38LHqMSPFrvoqADFJp4': 'house',
    'spotify:track:27nfKLXSw4Mmg0JMDcke93': 'house',
    'spotify:track:5FzuDFYmUFcvjraadJXv28': 'house',
    'spotify:track:1yAPglN5AGf7UoLK062ZYq': 'house',
    'spotify:track:5SD3MnYc8Mhpa5S3ojfIZj': 'house',
    'spotify:track:05h42SuH5WMgxNGEy7dbcY': 'house',
    'spotify:track:75UTBPkYyjIZhwCblCj9K7': 'house',
    'spotify:track:3bqzUDyN8wTCmdyzg6OlF3': 'house',
    'spotify:track:7Llqq3e3Hf4ICVJNBi2muE': 'house',
    'spotify:track:0tnFKjEEsjD3AVShRgtIun': 'house',
    'spotify:track:0h0jt3hxUR46AKIcCmchEr': 'house',
    'spotify:track:3MKevsnOdyWx6roRjKC0h5': 'house',
    'spotify:track:4SkGgfxDq8w0dLMdNRHEiS': 'house',
    'spotify:track:5ijp0ctfwwkmkR6hWDQnwn': 'house',
    'spotify:track:3wF2VOoVu4ETxBMJHT4Yao': 'house',
    'spotify:track:31F6r4J0qRBpXOUELOiybQ': 'house',
    'spotify:track:3D9l2sYUaTtJVOPp0AUpvW': 'house',
    'spotify:track:3c9RceD6okF9YiMGUpuCdE': 'house',
    'spotify:track:0YoVlRcAurKJVaLl4HRJYH': 'house',
    'spotify:track:2qFxaqBT4rHl3Nzs4mgUE7': 'house',
    'spotify:track:00eUmfHL07d9oSaZqq3Ucr': 'house',
    'spotify:track:35V6qXUDCvwZdmbKe5PlPG': 'house',
    'spotify:track:1SYNgyiVRZEBhV0P4YFBk8': 'house',
    'spotify:track:6LpVLK8IO21wXnYuYXTwgC': 'trance',
    'spotify:track:0XTYRfeyXX6ddRlF9LyZsC': 'trance',
    'spotify:track:2SFRhN9BX8akC4uHucD9PK': 'trance',
    'spotify:track:1Ie6SG92HfF46SC98w4sGN': 'trance',
    'spotify:track:6H26xIfCfb2BoVwmtfidUJ': 'trance',
    'spotify:track:7ASHtIrbW2rjMNaLOpvNgP': 'trance',
    'spotify:track:5oGlRKBSqHxuVBwPUIBnXU': 'trance',
    'spotify:track:1lh95xF2kYep1GW4WdGXKx': 'trance',
    'spotify:track:508n2SCjTiWIBHgvezad8T': 'trance',
    'spotify:track:4vPJXzwWlLjYser0Qcmv49': 'trance',
    'spotify:track:5xzzxWj8a1YBbNZhNLqWuQ': 'trance',
    'spotify:track:1pOjVQ65GHLlP4Acl9vwOa': 'trance',
    'spotify:track:7k5ABsm9RQNTE8CWATKMNm': 'trance',
    'spotify:track:1wzxYNLHfxwY1vQQAojaxX': 'trance',
    'spotify:track:6uss5GDw40yTPaXuP7TsKU': 'trance',
    'spotify:track:4dDZvLmBey7ijmpivR32Na': 'trance',
    'spotify:track:1KLIfTWf4lC4qOxuJEHPnS': 'trance',
    'spotify:track:5gpLmWxbc0aNgeqyaH0Ydv': 'trance',
    'spotify:track:5n3tNVZ4WyydTmDFDr9iBF': 'trance',
    'spotify:track:2cMujmlPsmEHAwUeLL1hfA': 'trance',
    'spotify:track:1m5HxBZlcA2KqXJ8ZghnjX': 'trance',
    'spotify:track:2MJlDoSisqIOzRaX8F37rH': 'trance',
    'spotify:track:6H3GXYNZsZhNb7LFdzVDVf': 'trance',
    'spotify:track:4ICkowPvxuLjymzLRltHYT': 'trance',
    'spotify:track:5294lgEa3wtmaupitIVJgx': 'trance',
    'spotify:track:0XSZDREixJOyBOw35KNkLo': 'drum-and-bass',
    'spotify:track:7DJkK9rY3HG96yGgRBv172': 'drum-and-bass',
    'spotify:track:1E7qIumIv72LydoAlxc9Kd': 'drum-and-bass',
    'spotify:track:3ac536Eml3t9d7CUVzMAia': 'drum-and-bass',
    'spotify:track:5cRDn5aGMLvWsldoRmOOz0': 'drum-and-bass',
    'spotify:track:0z9uYjZDr4HBpjKGvHHvrg': 'drum-and-bass',
    'spotify:track:3wcaYt92DPhOlDr5P45VgL': 'drum-and-bass',
    'spotify:track:5SHVGJ1lIMGRNPCbZLdFGw': 'drum-and-bass',
    'spotify:track:6eVu4lMmOK0JF3Fk07he44': 'drum-and-bass',
    'spotify:track:7BcArT6d86OQjsjZc504Pk': 'drum-and-bass',
    'spotify:track:1855jGsailIqrndEQtV4rL': 'drum-and-bass',
    'spotify:track:10EpXLXKHmNSVKvX7A5hg8': 'drum-and-bass',
    'spotify:track:67P3rmv8zBbrbvuSBRUzd2': 'drum-and-bass',
    'spotify:track:3kPOjkwckRJT6eNGJXIyNS': 'drum-and-bass',
    'spotify:track:4w5KCU6ktSQTZJtDbOFj9C': 'drum-and-bass',
    'spotify:track:5TGdeBW6v7BuGYjtiFKwyC': 'drum-and-bass',
    'spotify:track:0iLk17qRwCZYQVVKTTOfn5': 'drum-and-bass',
    'spotify:track:4nrcPumLm5ozA8qOEHcVm2': 'drum-and-bass',
    'spotify:track:1GzeZBt9GXs9hAuopZGacR': 'drum-and-bass',
    'spotify:track:31iPEHYTzazuEYqBRM76AG': 'drum-and-bass',
    'spotify:track:3q97VZitbqsa1LgDAVw9W9': 'drum-and-bass',
    'spotify:track:0uYbmxQt98OjX6VcDYo2Vc': 'drum-and-bass',
    'spotify:track:0qEdai4Xiqfq6Gb6JtjQYs': 'drum-and-bass',
    'spotify:track:3MN9ql5yvE0ACqGlSPnB6M': 'drum-and-bass',
    'spotify:track:0VrhJQBnT3VzdqI1FlCM4X': 'drum-and-bass',
    'spotify:track:7vSqIX6kwfYDyr5p3PKtEU': 'dubstep',
    'spotify:track:2RlV5lFcbC3qF5Da9IkSwc': 'dubstep',
    'spotify:track:07LCO1xsdnd1epIsqGAMz3': 'dubstep',
    'spotify:track:3GN81q8SpGj9PVaWDVmPsa': 'dubstep',
    'spotify:track:2GQ5KZ2i1GQcvrGd0FhDAv': 'dubstep',
    'spotify:track:4wysKuyN4GHPTRtOsbD981': 'dubstep',
    'spotify:track:76I3PmbGZazzNlEwlp1y85': 'dubstep',
    'spotify:track:6kZ2zeBKrotvH4LKvXQ0A2': 'dubstep',
    'spotify:track:49C2uDJ3QuCPop9o030V2O': 'dubstep',
    'spotify:track:5VLpL2ZxEBgYcoLr6hK17l': 'dubstep',
    'spotify:track:1axYKkAUrZbB1axBahVM2J': 'dubstep',
    'spotify:track:2nxo1GPtdBnlpas7InuOG4': 'dubstep',
    'spotify:track:5iPMMpJIGxUlH3CLFuwIkJ': 'dubstep',
    'spotify:track:7lm7HjAjpVKqWS2cQGQhzl': 'dubstep',
    'spotify:track:0bH5YzmIgaQ4ay1t89eMAh': 'dubstep',
    'spotify:track:3OaunNUlXXs5e2PXtNAzzG': 'dubstep',
    'spotify:track:3qhW0ioG27ZRFbZn1diK2m': 'dubstep',
    'spotify:track:3Ui9jL2IyUyu2EzffYmqPp': 'dubstep',
    'spotify:track:6GAhe3wXCDJP1RK5lZLyjX': 'dubstep',
    'spotify:track:1AcoISuZA2tq5uFOwRA7yu': 'dubstep',
    'spotify:track:48ho478N3GtM9tZedeaQWj': 'dubstep',
    'spotify:track:2g2Bo0Ju0CkgboI7bcR6JK': 'dubstep',
    'spotify:track:5LfkJez2ixlKfbQCZ0UU65': 'dubstep',
    'spotify:track:3g96DAZEVsFB0mVbEaHw3p': 'dubstep',
    'spotify:track:6puWOoY5pvOoycq5RDSrO5': 'dubstep'
}

# Get the audio features for the validation set and store them in a dataframe
val = pd.DataFrame(spotifyObject.audio_features(val_dict.keys()))
# Add the genres as a column in the dataframe
val['genre'] = val_dict.values()
# Save the dataframe as a csv file
val.to_csv('data/val.csv', index=False)
# Erase cache
os.remove(f'.cache-{username}')