from MALBot.src import login, tag

def test():
    #Initiate browser
    browser, list_url = login.login()
    
    #Clear tags and then add new ones
    anime_list = login.goto_anime_list(browser, list_url)

    for i in range(0, len(anime_list)):
        #Remove tags
        #tag.remove_tag(browser, anime_list[i])

        #Fill any empty slots
        tag.fill_empty_tag(browser, anime_list[i])

        #Or replace all tags
        #tag.replace_tag(browser, anime_list[i])

        #Or update tags
        #tag.update_tag(browser, anime_list[i])

    browser.close()
