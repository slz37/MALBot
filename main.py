from pckg.src.libs import *
from pckg.src import login, tag, anime, rank
        
def load():
    '''
    Loads anime data from previously saved file.
    '''
    
    try:
        anime_list = anime.anime.load()
        print("Loaded anime succesfully.")
    except:
        print("Failed to load anime.")

def begin_tag():
    '''
    Performs tag methods for anime in a
    user's MAL page.
    '''

    #Initiate browser
    browser, list_url = login.login()
    
    #Clear tags and then add new ones
    urls, anime_list = login.goto_anime_list(browser, list_url)

    for i in range(0, len(anime_list)):
        #Remove tags
        #tag.remove_tag(browser, urls[i], anime_list[i])

        #Fill any empty slots
        tag.fill_empty_tag(browser, urls[i], anime_list[i])

        #Or replace all tags
        #tag.replace_tag(browser, urls[i], anime_list[i])

        #Or update tags
        #tag.update_tag(browser, urls[i], anime_list[i])

    browser.close()
    
def begin_rank():
    '''
    Creates a ranking of anime on the
    user's PTW list.
    '''

    #MAL Anime List Tabs
    TABS = {
            "Currently Watching": 1,
            "Completed": 2,
            "On Hold": 3,
            "Dropped": 4,
            "Plan to Watch": 6,
            "All Anime": 7
            }
    animes = []

    #Initiate browser
    browser, list_url = login.login()
    
    #Get anime in each tab
    for tab in TABS:
        #Skip all anime tab - avoid double counting
        if tab != "Currently Watching":
            continue

        #Go to user's MAL anime list
        anime_list, urls = login.goto_anime_list(browser, list_url, tab)

        #Break if user has nothing on PTW
        if tab == "Plan to Watch" and len(anime_list) == 0:
            print("No anime on plan to watch list.")
            sys.exit()

        if len(anime_list) > 0:
            #Need temp array so we don't try to replace with an anime with its object many times
            temp = []
            
            #Loop over all anime
            for i in range(len(anime_list)):
                #Get anime info
                name = anime_list[i].text
                url = urls[i].get_attribute("href")
                ID = re.search(ID_PATTERN, url).group()

                #Instantiate class
                temp.append(anime.anime(browser, name, url, ID, tab))

            #Replace related anime and recommendations with objects
            for ani in temp:
                ani.replace_anime(animes, "related")
                ani.replace_anime(animes, "recommendations")

            #Now add to full list
            animes += temp

    #Save to file for future use
    anime.anime.save(animes)

    #Rank
    rank.rank(animes)
    browser.close()

if __name__ == "__main__":
    #Initiate Setup
    ID_PATTERN = re.compile("(?<=/)[\d]+(?=/)")

    begin_rank()
