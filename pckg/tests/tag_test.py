from pckg.src.login import *

def test():
    #Initiate browser
    browser, list_url = login()
    
    #Clear tags and then add new ones
    urls, anime_list = goto_anime_list(browser, list_url)

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
