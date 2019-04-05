from pckg.src.login import *

if func == "tag":
    #Clear tags and then add new ones
    urls, anime_list = goto_anime_list()

    for i in range(0, len(anime_list)):
        #Remove tags
        #remove_tag(browser, urls[i], anime_list[i])

        #Fill any empty slots
        fill_empty_tag(browser, urls[i], anime_list[i])

        #Or replace all tags
        #replace_tag(browser, urls[i], anime_list[i])

        #Or update tags
        #update_tag(browser, urls[i], anime_list[i])

    browser.close()
elif func == "rank":
    from pckg.src.anime import anime
    
    #Get anime in each tab
    animes = []
    for tab in TABS:
        #Skip all anime tab
        if tab == "All Anime":
            continue
            
        #Loop over all anime
        for i in range(len(anime_list)):
            #Get anime info
            name = anime_list[i].text
            url = urls[i].get_attribute("href")
            ID = re.search(ID_PATTERN, url).group()

            #Instantiate class
            animes.append(anime(name, url, ID))

        #Replace related anime and recommendations with objects
        for anime in animes:
            anime.replace_anime(animes, "related")
            anime.replace_anime(animes, "recommendations")

        #Rank
        rank(animes)
        browser.close()
else:
    print("Invalid function.")
    sys.exit()
