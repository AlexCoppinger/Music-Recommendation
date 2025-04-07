# Music-Recommendation
Music recommendation software using Spotify API

# Main Idea - 
Create a modular music recommendation system which pigeon-holes suggestions for a specific genre/style. You can then save that recommendation algorithm, and create a new one aiming for a new genre/style. For each algorithm, the user rates the song presented to them–they can then add it or/and move on to the next song. A button, to ‘unspecify’ the genre, can be used to widen the search and remove you from potential pigeon-holes you encounter. 

# Strategy - 
We will use the Spotify API to find correlational data between different songs depending on what playlists they’re in. A heat-map could then be created, gauging the correlation between different songs. 

Bayes’ Theorem must be used (e.g. Tokenization) 

Neural Nets should be very useful (can also be used for the ‘unspecify’ button by increasing the step size and inputting a random value)

Linear Regression could also be used although we would need to think about what ‘value’ we want to predict–or any boolean values (also very good for the ‘unspecify’ button)

Some sort of correlational analysis which could be done through clustering (potentially)

# Plan - 
# Set up preliminary stuff 
Text editors

Git repositories

Programs that need installing etc.

# Figure out how to even load the data
Figure out spotify API

Load data into software

What software exactly???

# Exploratory Data Analysis
Figure out how the data works 

What features can be extracted?

Numerical, categorical, etc?

Create visualizations using small subsection of the data 

Figure out what algorithms would work best given the data found

# Development of algorithms
Set up whatever algorithm decided (I’m currently assuming a neural network using tokenization)

How do we create a validation in the training set?

How do we make it so that the algorithm doesn’t need too many validations to decide on the genre/style (we don’t want the user to be rating huge amounts of songs before they’re given good songs)

How do we organize the algorithm to optimize the relatedness 

Interestingly enough, looking at ChatGPT’s algorithm could be useful 

# Setup Front-End
What platform will we use?

Website?

How do we store the data?

How do we connect front-end to back-end?

How does the interaction between user and data happen?

What platforms will we use in general? 

This section will require potentially the most research
