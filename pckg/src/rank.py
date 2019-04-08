from .libs import *

def rank(animes):
    '''
    Ranks anime on the plan to watch
    list of a user to aid in choosing
    a user's next anime they should
    watch.
    '''

    #Not sure how to weight these yet - should be some percentage
    status = {
        "Dropped": 0,
        "On Hold": 1/4,
        "Plan to Watch": 2/4,
        "Currently Watching": 3/4,
        "Completed": 1,
        } 

    #Setup and calculate genre avgs
    genres, avgs, var, nums = setup_genres()
    genre_avgs = tot_genre_avg(animes, genres, avgs, var, nums)

    #Create parameter lists
    genre_scores = []
    rel_scores = []
    num_rel = []
    rec_scores = []
    num_rec = []
    for anime in animes:
        if anime.status == "Plan to Watch": 
            genre_scores.append(calculate_genre_score(anime, genre_avgs))
            rel_scores.append(calculate_related_score(anime, animes, status))
            num_rel.append(len([rel for rel in anime.related_anime if rel in animes]))

            rec, num = calculate_recommended_score(anime, animes, status)
            rec_scores.append(rec)
            num_rec.append(num)

    #Now calculate individual scores and rank
    print(genre_scores, "\n", rel_scores, "\n", num_rel, "\n", rec_scores, "\n", num_rec)
    for i, anime in enumerate([anime for anime in animes if anime.status == "Plan to Watch"]):
        genre_rating = normalize(i, genre_scores)
        rel_rating = normalize(i, rel_scores)
        nrel_rating = normalize(i, num_rel)
        rec_rating = normalize(i, rec_scores)
        nrec_rating = normalize(i, num_rec)
        print(anime.name, genre_rating, rel_rating, nrel_rating, rec_rating, nrec_rating)

        anime.ranking = (genre_rating + rel_rating + nrel_rating + rec_rating + nrec_rating) / 5
    
    #Now sort by final rankings
    rankings = sorted(animes, key = lambda x: x.ranking, reverse = True)

    #Output
    for anime in rankings:
        if anime.status == "Plan to Watch":
            print("{:05.2f} {}".format(round(anime.ranking, 2), anime.name))
    sys.exit()

    return rankings

def normalize(i, arr):
    '''
    Normalizes values within array through
    feature scaling.
    '''

    #Check for division by zero
    if max(arr) == min(arr):
        return arr[i]

    #Calculate normalized rating
    rating = (10 * (arr[i] - min(arr))) / (max(arr) - min(arr))

    return rating

def setup_genres():
    '''
    Sets up the necessary lists for
    calculating genre averages.
    '''
    
    genres = ["Action", "Adventure", "Cars", "Comedy", "Dementia", "Demons",
          "Drama", "Ecchi", "Fantasy", "Game", "Harem", "Hentai", "Historical",
          "Horror", "Josei", "Kids", "Magic", "Martial Arts", "Mecha", "Military",
          "Music", "Mystery", "Parody", "Police", "Psychological", "Romance",
          "Samurai", "School", "Sci-Fi", "Seinen", "Shoujo", "Shoujo Ai", "Shounen",
          "Shounen Ai", "Slice of Life", "Space", "Sports", "Super Power",
          "Supernatural", "Thriller", "Vampire", "Yaoi", "Yuri"]
    
    avgs = [0.0]*len(genres) #Initialize at 0 to start at base value
    var = [0.0]*len(genres) #Initialize at 0 to start at base value
    nums = [0]*len(genres)   #Pretend there's already an anime rated at 5

    return genres, avgs, var, nums    

def tot_genre_avg(animes, genres, avgs, var, nums):
    '''
    Calculates the average score of each
    genre to weight by the genres of each
    anime.
    '''

    #Ignore PTW ratings and update avg/var for all genres
    for anime in animes:
        if anime.status != "Plan to Watch":
            for genre in anime.genres:
                rating = int(anime.user_rating)
                index = genres.index(genre)
                muprev = avgs[index]
                
                avgs[index] = (nums[index] * avgs[index] + rating) / (nums[index] + 1)
                var[index] = var[index] + ((rating - muprev) * (rating - avgs[index]) - \
                             var[index]) / (nums[index] + 1)
                
                nums[index] += 1

    #Create dictionary of averages
    genre_avgs = dict(zip(genres, zip(avgs, var, nums)))
    
    return genre_avgs

def calculate_genre_score(anime, genre_avgs):
    '''
    Calculates the scoring for each anime
    on the PTW list based on it's genre.
    '''
    
    genre_length = 0
    mu = 0

    #Calculate score and length
    for genre in anime.genres:
        genre_length += genre_avgs[genre][2]
        mu += genre_avgs[genre][0] * genre_avgs[genre][2]

    #Calculate weighted rating
    if mu == 0:
        genre_score = 0
    else:
        genre_score = mu / genre_length

    return genre_score

def calculate_related_score(anime, animes, status):
    '''
    Calculates the scoring for each anime
    on the PTW list based on it's related anime
    if they are on the list but not PTW.
    '''

    related_animes = [rel for rel in anime.related_anime if rel in animes]

    '''
    #Map values from [0, 20] to [0, 1] - may need to increase this later
    if len(related_animes) > 20:
        print("Warning, # of recommended animes is greater than scale factor.")
        
    scaled_rel = len(related_animes) / 20
    '''

    #Calculate related anime score
    related_score = sum([(rel.user_rating * status[rel.status]) for rel in related_animes \
                         if rel.status != "Plan to Watch"])

    return related_score

def calculate_recommended_score(anime, animes, status):
    '''
    Calculates the scoring for each anime
    on the PTW list based on it's recommended anime
    if they are on the list but not PTW.
    '''

    #Separate keys and count number of recommendations
    recommended_animes = anime.recommendations
    recommended_keys = [rec for rec in recommended_animes if rec in animes and rec.status != "Plan to Watch"]
    num_rec = sum([recommended_animes[rec] for rec in recommended_animes if rec in animes])

    '''
    #Map values from [0, 100] to [0, 1] - may need to increase this later
    if len(recommended_animes) > 100:
        print("Warning, # of recommended animes is greater than scale factor.")
        
    scaled_rec_values = [x / 100 for x in recommended_values]
    '''
    
    #Calculate recommended anime score
    recommended_score = 0
    for i, rec in enumerate(recommended_keys):
        recommended_score += rec.user_rating * status[rec.status]

    return recommended_score, num_rec
