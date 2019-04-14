from pckg.src.libs import *
from pckg.src import login, tag, anime, rank
import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_predict

def begin_tag():
    '''
    Performs tag methods for anime in a
    user's MAL page.
    '''

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
    
def write_anime_to_file():
    '''
    Gathers data for each anime on user's
    page and writes the data to file for
    use with machine learning to rank
    anime on the PTW list.
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
    list_url = u"https://myanimelist.net/animelist/Paul"
    
    #Get anime in each tab
    for tab in TABS:
        #Skip all anime tab - avoid double counting
        if tab == "All Anime":
            continue

        #Go to user's MAL anime list
        anime_list = login.goto_anime_list(browser, list_url, tab)

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
                url = anime_list[i].get_attribute("href")
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
    user = list_url.split("/")[-1]
    anime.anime.save(animes, user)

if __name__ == "__main__":
    #Initiate Setup
    ID_PATTERN = re.compile("(?<=/)[\d]+(?=/)")
    data = []
    target = []
    write_anime_to_file()
    sys.exit()

    '''
    boston = load_boston()
    #print boston.DESCR

    X = boston.data
    y = boston.target

    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size = 0.25, random_state = 42)
    '''

    #Write anime to file, load it back, and use naive rankings
##    write_anime_to_file()
##    animes = anime.anime.load()
##    rank.naive_ranking(animes)

    #Load anime, save data parameters to file, and rank using machine learning
    animes = anime.anime.load(user)

    #Select training set
    training_set = [ani for ani in animes if ani.status == "Completed"]

    #Setup training set
    for ani in training_set:
        ani.status = "Plan to Watch"
        target.append(ani.user_rating)
    Xtrain, Xtest, ytrain, ytest = train_test_split(training_set, target, test_size = 0.2, random_state = 42)

    rank.calculate_parameters(Xtrain)
    sys.exit()

    clf = MLPRegressor(solver = 'lbfgs', alpha = 1e-5, hidden_layer_sizes = (5,2), random_state = 1)
    clf.fit(Xtrain, ytrain)

    # Look at the weights
    print ([coef.shape for coef in clf.coefs_])

    ypred = clf.predict(Xtest)
    #print ypred, ytest

    fig = plt.figure(figsize = (6, 6))
    plt.scatter(ytest, ypred)
    plt.xlabel("Actual Value [x$1000]")
    plt.ylabel("Predicted Value [x$1000]")
    plt.show()

    yCVpred = cross_val_predict(clf, X, y, cv = 10) # Complete

    fig = plt.figure(figsize = (6, 6))
    plt.scatter(y, yCVpred)
    plt.xlabel("Actual Value [x$1000]")
    plt.ylabel("Predicted Value [x$1000]")
    plt.show()

    #Train
    #Select PTW as new set
    #Run on PTW set
