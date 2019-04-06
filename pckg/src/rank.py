from .libs import *

def rank(animes):
    '''
    Ranks anime on the plan to watch
    list of a user to aid in choosing
    a user's next anime they should
    watch.
    '''

    '''
    Things to include when ranking:
    -Average rating of genres
    -Average rating and status of related anime if on list
    -For a specific anime, if a recommendation is in the user's list, weight by
     number of users recommending, status, and rating if available
    '''

    #Setup and calculate genre avgs
    genres, avgs, nums = setup_genres()
    genre_avgs = genre_avg(animes, genres, avgs, nums)
    print(genre_avgs)

    #Update and output results
    rankings = calculate_rankings(animes, genre_avgs)
    
    for anime in rankings:
        if anime.status == "Plan to Watch":
            print("{:05.2f} {}".format(round(anime.ranking, 2), anime.name))
    sys.exit()

    return rankings

def calculate_rankings(animes, genre_avg):
    '''
    Takes in the current rankings and
    a metric by which to weight them
    and updates the rankings based
    on that metric.
    '''

    #Not sure how to weight these yet - should be some percentage
    status = {
        "Dropped": 0,
        "On Hold": 1/4,
        "Plan to Watch": 2/4,
        "Currently Watching": 3/4,
        "Completed": 1,
        } 

    #Calculate ranking for all anime in PTW list
    for anime in animes:
        if anime.status == "Plan to Watch":
            #Genres
            genre_score = sum([genre_avg[genre] for genre in anime.genres])
            genre_length = len(anime.genres)

            #Related anime
            related_animes = [rel for rel in anime.related_anime if rel in animes]

            #Map values from [0, 20] to [0, 1] - may need to increase this later
            if len(related_animes) > 20:
                print("Warning, # of recommended animes is greater than scale factor.")
                
            scaled_rel = len(related_animes) / 20
            
            related_score = sum([(rel.user_rating * status[rel.status] * scaled_rel) for rel in related_animes])
            related_length = len(related_animes)

            #Separate keys and values
            recommended_animes = anime.recommendations
            recommended_keys = [rec for rec in recommended_animes if rec in animes]
            recommended_values = [recommended_animes[rec] for rec in recommended_keys]

            #Map values from [0, 100] to [0, 1] - may need to increase this later
            if len(recommended_animes) > 100:
                print("Warning, # of recommended animes is greater than scale factor.")
                
            scaled_rec_values = [x / 100 for x in recommended_values]
            
            #Recommended anime
            recommended_score = 0
            for i, rec in enumerate(recommended_keys):
                recommended_score += rec.user_rating * status[rec.status] * scaled_rec_values[i]
            recommended_length = len(recommended_keys)

            #Calculate overall average now
            if anime.name.lower() == ".hack//g.u. returner":
                print(related_animes)
                print(genre_score, related_score, recommended_score,
                      genre_length, related_length, recommended_length)
            anime.ranking = (genre_score + related_score + recommended_score) / \
                            (genre_length + related_length + recommended_length)

    #Now sort by final rankings
    rankings = sorted(animes, key = lambda x: x.ranking, reverse = True)

    return rankings

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
    avgs = [5.0]*len(genres) #Initialize at 5 to start at neutral value
    nums = [1]*len(genres)   #Pretend there's already an anime rated at 5

    return genres, avgs, nums    

def genre_avg(animes, genres, avgs, nums):
    '''
    Calculates the average score of each
    genre to weight by the genres of each
    anime.
    '''

    #Ignore PTW ratings and update avg for all genres
    for anime in animes:
        if anime.status != "Plan to Watch":
            for genre in anime.genres:
                index = genres.index(genre)
                avgs[index] = (nums[index] * avgs[index] + int(anime.user_rating)) / (nums[index] + 1)
                nums[index] += 1

    #Create dictionary of averages
    genre_avgs = dict(zip(genres, avgs))
    
    return genre_avgs
