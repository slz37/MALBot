import tkinter
from pckg.src.login import *

def setup():
    '''
    Sets up the user interface for
    interacting with a user's MAL page.
    '''
    
    #Master frame
    frame = tkinter.Frame(WINDOW)
    frame.grid(row = 1, column = 1)
    
    #Console Window
    console = tkinter.Text(frame, state = tkinter.DISABLED, width = 60)
    console.pack()

    #Button frame
    button_frame = tkinter.Frame(WINDOW)
    button_frame.grid(row = 2, column = 1)

    #Tag Button
    tag_button = tkinter.Button(button_frame, text = 'Tag Anime', width =
                                25, command = lambda: begin_tag(console))
    tag_button.grid(row = 1, column = 1)
    
    #Rank Button
    rank_button = tkinter.Button(button_frame, text = 'Rank Anime on PTW', width =
                                 25, command = lambda: begin_rank(console))
    rank_button.grid(row = 1, column = 2)

def begin_tag(console):
    '''
    Performs tag methods for anime in a
    user's MAL page.
    '''

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
    
def begin_rank(console):
    '''
    Creates a ranking of anime on the
    user's PTW list.
    '''
    from pckg.src.anime import anime

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
    browser, list_url = login()
    
    #Get anime in each tab
    for tab in TABS:
        #Skip all anime tab - avoid double counting
        if tab == "All Anime":
            continue

        #Go to user's MAL anime list
        anime_list, urls = goto_anime_list(browser, list_url, tab)

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
                temp.append(anime(browser, name, url, ID, tab))

            #Replace related anime and recommendations with objects
            for ani in temp:
                ani.replace_anime(animes, "related")
                ani.replace_anime(animes, "recommendations")

            #Now add to full list
            animes += temp

    #Rank
    rank(animes)
    browser.close()

def on_closing():
    '''
    Closes the tkinter window
    and exits the program.
    '''
    
    WINDOW.destroy()
    sys.exit()

if __name__ == "__main__":
    #Initiate Setup
    WINDOW = tkinter.Tk()
    WIDTH = 500  
    HEIGHT = 500  
    X = 100
    Y = 100

    #Update Window and Run
    WINDOW.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, X, Y))
    WINDOW.title("MALBot")
    WINDOW.protocol("WM_DELETE_WINDOW", on_closing)

    setup()
    WINDOW.mainloop()
