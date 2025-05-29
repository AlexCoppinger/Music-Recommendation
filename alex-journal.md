How to merge your branch on github:
git checkout your-branch
git fetch origin
git merge origin/main   # Update your branch first
# (fix conflicts if needed)

git checkout main
git pull origin main    # Make sure main is fresh
git merge your-branch
git push origin main    # Push the updated main

git checkout your-branch #To go back to your branch

When saving on your branch:

git add .
git commit -m "Built the login page form"
git push origin your-branch-name

# Week 1

The name of this algorithm is VibeLink

This week I came up with the idea of the app
I created a plan and rough outline for how we will achieve it
I completed the README.md file and added it to our repository

# Week 2
I setup a proper coding environment
Submitted an application for gitHub education for copilot

Goals: 

Setup the virtual environment for Django 
Make the keys hidden
Begin writing code for the algorithms


Notes: 

before each coding session, write: source venv/bin/activate

Janata's pwap (program) file includes:

- migrations (a folder)
- templates/pwap (a folder with html code)
- __init__.py
- admin.py 
- apps.py 
- models.py 
- spotify.py 
- tests.py 
- urls.py ## this file is similar to ours from spotify_app
- views. py 

I am missing the spotify.py which probably comes from not linking my environment with the Spotify API
I am also missing urls.py which I don't completely understand the point of that one


Janata's psc182_s25--which I assume is analogous to our 'spotify_app' foldler-- includes:

- settings (which includes 3 files: __init__.py, dev.py, and settings.py)
-__init__.py 
- asgi.py  
- urls.py ## this file is also similar to ours but slightly different
- wsgi.py 


To do:

There is no dev.py file anywhere, I forgot what it's for but there's barely anything in it in Janata's repository
There is a settings.py file in Janata's but within the settings directory--I'm assuming this may have something to do with the secret keys stuff
We need to make a requirements.txt file that includes packages we are using & whatever else


Moving forward, we need to add the spotify API, of which Federico has a specific one. 
We also need to come up with a proper name that makes it easier to organize this stuff--'music-recommendation' and 'spotify_app' and 'music_rec' aren't going to suffice
I am also very confused on what the venv is for. I'm worried I may have created the venv and not used it properly since I don't understand how it works
We need to understand how the keys mechanism works, and figure out how to implement the thing Janata did

We need to figure out how to setup the spotify API thing, and get the keys






Questions for Janata:

- Since I'm working with Federico, is there a specific convention he recommends to
deal with our code? I understand gitHub is good at doing this, but it may get annoying
to have to pull, commit, and push every single time. Is this needed? Is there a better way?
- What method for securiing the 'secret key' is being used? 
- Why config.get for the spotify stuff but not config like for the secret key?
- Could we see the ini file to understand the format?
- What is the point of import pdb? what does the module pdb do?
- Just curious, but what does the module os do?
- I don't really understand the point of a dev.py file. It doesn't work regardless although I'm assuming it's allowing the DEBUG to be True?
- Why did db.sqlite3 pop up in larger musicrec folder?

# Week 3
setting up a django shell

- python manage.py shell --> for running the shell
- when running a shell, it executes 
- pip freeze > requirements.txt
- > --> dumps into file
- >> appends the things

In terms of content: 
(we want to clean up views and fetching and spotify API, and then how to store and work in our local database)

- If we're not doing a post request (putting something on the webstie)
- We're taking stuff (from the get request)
- need to create a forms.py
- form consist of various fields
- different input boxes, or dropdown menues that give options
- fields for inputting things 
- clean method makes the field clean so that it's nicely formatted
- Could do a response

- in html there is namespace to end-point (which is in the urls.py) --> which is 
- {} --> in HTML is django template stuff 

- Haven't dealt with database
- Haven't dealt with the limits --> You can go to the next page and loop for a long time 

We can use user URI as a feature 

Django has 'bulk' update stuff

Week 5 
- 671 071 2698
- In views there's a 'select_purpose' function --> that gives the purpose of the search 
- in spotify.py add a import_items --> makes sure that if you have a search, you don't have to do it again 
- would want to delete items from before if you make a new search so that the duplicates aren't needed (although for us this might not be useful)
- In models, we have something that records the rating of each track 
- get_playlist_track --> To get playlist for a track... and then create a playlist to put music into it
- sp.auth --> to get a user's ID credentials and stuff 
- dir(request.user)
- in models.py --> Add specific user (abstract user) --> in class User(AbstractUser)
- You user @ login_required for registration --> each registration is going to require a specific type of thing
- you do the login thing in models, spotify, ... --> Don't forget all of the imports in views.py 
- in forms.py, we have a custom user registration form (CustomUserCreationForm) which comes from a package called UserCreationForm
- potentially in the future autogenerate a username, and authenticate through spotify 
- python manage.py makemigrations --> to create migrations
- What is a decorator? (which is the login_required thing)
- Using a seperate spotify model isn't maybe the best. A Django user is maybe not the best idea 

Thinking out loud about what I want to do for the machine learning algorithm:
We want to use the correlation between playlists to tell us whether songs are related or not?

So basically, every song is related to every other song based on how many playlists it has in common with it
So in our dataset we need every song and every single playlist it belongs in. Is there a command that does this?
Let's say we load 100 random tracks, we need to be able to tell what playlists its in, etc. 

What we could also do is find a subsection of playlists, and analyze them for each song. 
- If a playlist contains a song, we add a tick to it with that token 
- At the end, we should have a list of every song that within those playlists, and all the playlists it's in
- So within our database of songs, we'd have each song and each playlist that it is a part of, and we can check 
whether each song has playlists in common with other songs 

- Later on, we could go multiple layers deep, finding the correlation of each song to each other song. If it is 1 
playlist away, then there's a lower coefficient, etc. This could, however, go on infinitely, and it may be useful to have 
a limit (maybe the as I've said before, could be logarithmic, where the further it is, the less it matters, but the 
closer it is, the more it matters)
- We would tally each one of these against each other to find the ideal song. And maybe the algorithm could update each
layer for 1 song. If it can find one and the songs are within a coefficient, great. Otherwise, it can update until we find one. 


We can create this relatedness between each song. The thing is attaching it to a coefficient that the user rates is interesting.
How do we make sure that each time a user rates a song, it will update the recommendation? We could try multiplying it by the weights
of the songs and each related--if it's, let's say, larger than 5, it's positive, and less, negative. However, I'm worried about
certain songs gaining a huge amount of traction, and then they would be hard to divide. There almost needs to be a way 
to completely remove a song. I guess the person could maybe choose whether to add it to the playlist, and if it's not added,
then it's gone, and if it is, then it increases the weights. 


$\sigma$

Find a markdown plugin


I guess this is the most feasable version of our model. A proof of concept. The only thing is, 

# Week 6

querySelector in javascript --> goes through an array and .forEach achieves to specific thing

# Week 8 
AUTH_USER_MODEL = "pwap.User"

That's funny

variable = models.variable.first() ==> To find the first in the variable

TrackXPlaylist.object.filter(track=track, playlist__playlistsearchresult__query) 


It's also proportional to infinity, and not to a 
maximum value

