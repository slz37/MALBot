from pckg.src.login import *

def test():
    from pckg.src.anime import anime

    names = ["sword art online",
             ".hack//g.u. trilogy",
             ".hack//g.u. returner",
             ".hack//sign"]
    urls = ["https://myanimelist.net/anime/11757/Sword_Art_Online",
            "https://myanimelist.net/anime/3269/hack__GU_Trilogy",
            "https://myanimelist.net/anime/2928/hack__GU_Returner",
            "https://myanimelist.net/anime/48/hack__Sign"]
    IDS = ["11757",
           "3269",
           "2928",
           "48"]
    tabs = ["Plan to Watch",
            "Plan to Watch",
            "Completed",
            "Plan to Watch"]
    
    #Get anime in each tab
    animes = []

    #Go to my list for testing but don't need data
    _, _ = goto_anime_list("",
                           u"https://myanimelist.net/animelist/Combinatorics")

    for i in range(0, len(names)):
        #Preselected data
        name = names[i]
        url = urls[i]
        ID = IDS[i]
        tab = tabs[i]
        
        animes.append(anime(browser, name, url, ID, tab))

    #Replace related anime and recommendations with objects
    for anime in animes:
        anime.replace_anime(animes, "related")
        anime.replace_anime(animes, "recommendations")

    #Get rankings
    rank(animes)

    browser.close()
