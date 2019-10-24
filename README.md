# EDM-Genre-Classifier

Accurately predicting the genre of a song based on its audio features.

- By Josh Robin


## Executive Summary
 
There a many different types and styles of music out there. For this reason, we have created a system of categorizing music by genres and subgenres. Genres help us to understand how music evolves and forms trends, and also helps listeners identify what they like to listen to. When it comes to the more well-known genres, most people are easily able to tell the difference between them. Some of the more obscure subgenres however, have differences that are more nuanced and difficult for most people to recognize. For example, recognizing the differences between rock music and classical music is much easier than distinguishing alternative rock from punk rock. Still, we know that human beings are generally capable of identifying a musical genre. The more people listen to different styles of music, the more they learn about what makes these styles unique, and the better they become at making distinctions between them. In theory, a machine learning algorithm could learn about these differences as well. What I would like to explore in this project is how well a computer would be able to accurately predict the genre of a song.

---

## Problem Statement

Can we use a machine learning model to accurately predict the genre of a song based on its audio data? To test this, I chose four major subgenres of Electronic Dance Music (EDM). While there are more than four genres of EDM, four of the biggest are dubstep, house, trance, and drum & bass. Being that these genres are all still electronic music, they might sound fairly similar to most people. However, fans of this type of music or people involved in the electronic music industry would most likely be able to tell one from another. I wanted the genres to be fairly similar becuase if a computer can tell the difference between trance and house, it can probably tell the difference between less similar genres just as well, if not better. The ability to create a model that can do this accurately could prove very useful for music applications such as Spotify or Pandora who are in the business of providing their users with music fit their personal preferences. If these companies can use machine learning to automatically classify vast libraries of music by genre in a streamlined fashion, this cuts out a lot of unnecessary work, and if users like one song in a particular genre, chances are they will like others in the same genre.

---

## Spotipy and the Spotify API

Spotify's API allows access to data on millions of songs. In order to interface with the API, I will be using a Python library called Spotipy. Supported and developed by Spotify, Spotipy provides a great way to efficiently access detailed data on all kinds of music, including audio features such as the key, tempo, duration, loudness, and danceability. These audio features can be used to train a genre classification model.

---

## Process

The first step in this process was collecting the data. Using Spotipy, I accessed Spotify's recommendation engine to collect data on the audio features of 1000 songs from each of the four genres, 4000 in total. I also handpicked another 100 songs (25 from each genre) to serve as a validation set.

Next, I cleaned my dataset in two major steps. First, I determined that there were a small number of tracks that didn't truly represent songs from their respective genres, such as extended mixes and transition tracks, so I removed them. Second, I found that the tempos were not all measured on the same scale, which would have thrown off the results of my model so I adjusted them to be on a uniform scale. Once the data was cleaned I explored the distributions of each of the features and their correlations to the target. I found that five features in particular were the best predictors of genre: duration, loudness, tempo, danceability and energy. With these features, I created polynomial features up to 5 degrees. In addition I created two scaled versions of this data to compare in modeling, one with a standard scaler and one with a power transformer.

I then attempted a series of classification algorithms for modeling. The larger dataset was split into training and test sets. Each estimator was evaluated on both of these sets, as well as the validation data, using the two scaled versions and the unscaled version of the data. The following default models were each attempted first: Logistic Regression, K-Nearest Neighbor, Decision Tree, Bagged Decision Trees, Random Forest, AdaBoost, Gradient Boost, and XGBoost. Once I had done this, I determined that the Logistic Regression and K-Nearest Neighbor algorithms did not work as well as the others, so I didn't pursue these any further. With the remaining algorithms, I used Randomized Search and Grid Search to tune hyperparameters and improve the performance of these models. Finally, I narrowed in on the 5 best models and ensembled them with a Voting Classifier. This combination of estimators became my final model.

Lastly, I wrote a Python script that uses the model I had built in conjunction with the Spotify API. The program allows a user to search for any song in the Spotify library and it will collect the audio features and predict the genre of that song, provided it is either dubstep, house, trance, or drum and bass. 

---

## Conclusion and Recommendations

My final model was able to predict the correct genre for 93% of the validation set. Using my final genre predictor on various EDM songs, I found that it predicted the genre correctly with a level of accuracy about the same as the validation set. One important thing to address here is that validation set and final app both provided significantly better results than the training and test sets. My final model had an accuracy score of 82% on the training set and 75% on the test set. This trend applied to all of the models I tried. The validation was always much better. In exploring this further, I found that this was due to the way I chose the songs for validation as compared to the recommendation provided by Spotify. When Spotify makes recommendations based on a genre such as dubstep, the songs fall into the category of dubstep generally, but some more loosely than others. There is a good degree of variety in the selections, even if they are relatively within the same genre. The dubstep songs I handpicked for validation, however, were more generic to the genre, and therefore had much less variety. The fact the model was better at predicting songs that would be considered more classic dubstep was actually a good sign to me. Training the model on a dataset with a little more variety seemed to make it more robust.

Despite the relatively strong performance of this genre classifier, I still feel that its biggest limitation is in the data used to train it. 1000 songs for each genre isn't a whole lot, especially when some of it needs to be used for testing. With more data, I believe I could achieve even better results. In addition, having some variety in each of the four classes is a good thing, but there may be a little too much variety in this dataset. Some of the songs stray pretty far from what would traditionally be considered for their respective genres, which may be throwing off the model to some degree. Finding a balance between having enough data and having good data was difficult, but it led me to keeping some of these outliers.

Overall, given the fact that I chose four very similar genres, I am pretty satisfied with the results I achieved in this project. The final app performs well enough that someone could use it effectively to classify EDM music. In the future, I would like to use my own recommendation system to see if I can build a better dataset for this project. I would also like to try a similar process with other genres, perhaps some that are less similar to each other. There are many more possibilities to expand on this idea and I plan to explore this further.