from pckg.src.login import *

def test():
    from pckg.src.anime import anime

    names = ["occultic;nine",
             "black clover",
             "fate/stay night movie: heaven's feel - i. presage flower",
             "sword art online",
             ".hack//g.u. trilogy",
             ".hack//g.u. returner",
             ".hack//sign",
             ".hack//intermezzo",
             ".hack//liminality",
             "log horizon",
             "btooom!",
             "mahoutsukai no yome",
             "shinsekai yori"]
    urls = ["https://myanimelist.net/anime/32962/Occultic_Nine",
            "https://myanimelist.net/anime/34572/Black_Clover",
            "https://myanimelist.net/anime/25537/Fate_stay_night_Movie__Heavens_Feel_-_I_Presage_Flower",
            "https://myanimelist.net/anime/11757/Sword_Art_Online",
            "https://myanimelist.net/anime/3269/hack__GU_Trilogy",
            "https://myanimelist.net/anime/2928/hack__GU_Returner",
            "https://myanimelist.net/anime/48/hack__Sign",
            "https://myanimelist.net/anime/1143/hack__Intermezzo",
            "https://myanimelist.net/anime/299/hack__Liminality",
            "https://myanimelist.net/anime/17265/Log_Horizon",
            "https://myanimelist.net/anime/14345/Btooom",
            "https://myanimelist.net/anime/35062/Mahoutsukai_no_Yome",
            "https://myanimelist.net/anime/13125/Shinsekai_yori"]
    IDS = ["32962",
           "34572",
           "25537",
           "11757",
           "3269",
           "2928",
           "48",
           "1143",
           "299",
           "17265",
           "14345",
           "35062",
           "13125"]
    tabs = ["Plan to Watch",
            "Dropped",
            "Completed",
            "Plan to Watch",
            "Plan to Watch",
            "Plan to Watch",
            "Completed",
            "Plan to Watch",
            "Plan to Watch",
            "Plan to Watch",
            "Plan to Watch",
            "Dropped",
            "Completed"]
    
    #Get anime in each tab
    animes = []

    #Initiate browser
    browser, list_url = login()

    #Go to my list for testing but don't need data
    goto_anime_list(browser, u"https://myanimelist.net/animelist/Combinatorics")

    for i in range(0, len(names)):
        #Preselected data
        name = names[i]
        url = urls[i]
        ID = IDS[i]
        tab = tabs[i]
        
        animes.append(anime(browser, name, url, ID, tab))

    #Replace related anime and recommendations with objects
    for ani in animes:      
        ani.replace_anime(animes, "related")
        ani.replace_anime(animes, "recommendations")
    anime.save(animes)

    animes = anime.load()

    #Get rankings
    rank(animes)

    browser.close()
