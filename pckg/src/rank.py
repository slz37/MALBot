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
    -Rating of related anime if on list
    -Number of related anime on list
    -Status of related anime(completed, dropped, etc.)
    
    -For a specific anime, if a recommendation is in the user's list, weight by
     number of users recommending
    '''

    #Setup and calculate genre avgs
    genres, avgs, nums = setup_genres()
    genre_avgs = genre_avg(animes, genres, avgs, nums)

    #Update and output results
    test = update_rankings(animes, genre_avgs)
    for anime in test:
        if anime.status == "Plan to Watch":
            print("{} {}".format(round(anime.ranking, 2), anime.name))
    sys.exit()

    return rankings

def update_rankings(animes, genre_avg):
    '''
    Takes in the current rankings and
    a metric by which to weight them
    and updates the rankings based
    on that metric.
    '''

    #Not sure how to weight these yet
    status = {
        "Currently Watching": 6,
        "Completed": 10,
        "On Hold": 4,
        "Dropped": 1,
        "Plan to Watch": 5,
        } 

    for anime in animes:
        if anime.status == "Plan to Watch":
            #Genres
            for genre in anime.genres:
                anime.ranking += genre_avg[genre]

            anime.ranking /= len(anime.genres) #normalize

            #Related anime
            for related_anime in anime.related_anime:
                if related_anime in animes:
                    #Factor in rating of related anime
                    if related_anime.user_rating != "-":
                        anime.ranking += (int(related_anime.user_rating) * status[related_anime.status]) / 100
                    else:
                        anime.ranking += (5 * status[related_anime.status]) / 100 #no ranking -> neutral

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

    #Check if each anime has rating and update avg for all genres
    for anime in animes:
        if anime.user_rating != "-":
            for genre in anime.genres:
                index = genres.index(genre)

                avgs[index] = (nums[index] * avgs[index] + int(anime.user_rating)) / (nums[index] + 1)
                nums[index] += 1

    #Create dictionary of averages
    genre_avgs = dict(zip(genres, avgs))
    
    return genre_avgs
