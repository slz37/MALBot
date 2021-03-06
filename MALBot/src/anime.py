from .libs import *

class anime(): 
    def __init__(self, browser, name, url, ID, tab):
        '''
        Instantiate the class and perform
        necessary setup.
        '''

        #Anime properties on list page
        self.ranking = 0
        self.name = name
        self.url = url
        self.ID = ID
        self.status = tab

        #Get rating for user, different structure if not logged in
        try:
            self.user_rating = browser.find_element_by_id("scoreval{}".format(self.ID)).text
        except:
            temp_list = browser.find_elements_by_tag_name("table")
            temp_row = [ani.text for ani in temp_list if "\n" + self.name + " " in ani.text][0]
            temp_row = temp_row.split(self.name + " ")[1]

            #Deal with airing or not yet aired shows
            if temp_row.startswith("Airing"):
                self.user_rating = temp_row.split("Airing ")[1].split(" ")[0]
            elif temp_row.startswith("Not Yet Aired"):
                self.user_rating = temp_row.split("Not Yet Aired ")[1].split(" ")[0]
            else:
                self.user_rating = temp_row.split(" ")[0]
            
        #Set default rating and convert to int if necessary
        if self.user_rating == "-":
            self.user_rating = 0 #use 0 as base
            #self.user_rating = 5 #use average as base
        else:
            self.user_rating = int(self.user_rating)

        #Load anime page
        self._load_page(browser)

        #Initiate empty arrays
        self.related_anime = []
        self.genres = []

        #Properties from anime page
        self.progress = browser.find_element_by_id("myinfo_watchedeps").get_attribute("value")
        self.related_anime = self._get_related_anime(browser)        
        self.genres = self._get_genres(browser)

        titles, users = self._get_recommendations(browser)
        self.recommendations = dict(zip(titles, users))
        
        num_episodes = browser.find_element_by_xpath("//div[contains(.//span, \"Episodes:\")]").text

        #Handle unknown num of episodes
        try:
            self.num_episodes = num_episodes.split(" ")[1]
        except:
            self.num_episodes = "Unknown"
            
        self.duration = self._get_duration(browser)

        #Done now, so return back to list
        self._close_page(browser)

    @staticmethod
    def save(ani, user):
        '''
        Save class state and attributes for
        later use to reduce requests
        to myanimelist.ent
        '''
        
        file = open("{}_anime_list.txt".format(user), "wb")
        pickle.dump(ani, file)
        file.close()

    @staticmethod
    def load(user):
        '''
        Loads a previously parse anime with
        its attributes.
        '''
        
        file = open("{}_anime_list.txt".format(user), "rb")
        anime_list = pickle.load(file)
        file.close()

        return anime_list

    def _load_page(self, browser):
        '''
        Loads the anime's page to grab all
        necessary info.
        '''

        #Load tab
        time.sleep(20)
        browser.execute_script("window.open(\"{}\");".format(self.url))
        browser.switch_to_window(browser.window_handles[1])
        
    def _close_page(self, browser):
        '''
        Closes the anime's page once
        we are done with it.
        '''

        #Close tab
        browser.close()
        browser.switch_to_window(browser.window_handles[0])

    def _get_genres(self, browser):
        '''
        Obtains a formatted string of genres for the
        current anime in list.
        '''

        #Get genres
        genres = []
        genres_unformatted = browser.find_elements_by_css_selector("a[href*=\"genre\"")

        for gen in genres_unformatted:
            genres.append(gen.text)

        return genres

    def _get_related_anime(self, browser):
        '''
        Grabs the related anime from the
        current page.
        '''

        #Get related anime
        related_anime = []

        try:
            related = browser.find_element_by_class_name("anime_detail_related_anime")

            #Now get urls and remove manga
            for anime in related.find_elements_by_css_selector("a"):
                if "manga" not in anime.get_attribute("href"):
                    related_anime.append(anime.text)
        except:
            pass

        return related_anime

    def _get_duration(self, browser):
        '''
        Grabs the duration in minutes of the
        anime to weight by length for movies/OVAs.
        '''

        #Don't know number of episodes
        if self.num_episodes == "Unknown":
            return "Unknown"

        #Grab duration
        duration = browser.find_element_by_xpath("//div[contains(.//span, \"Duration:\")]").text
        duration = duration.split(": ")[1]
        
        #Now format to be only in units of minutes
        minutes = 0
        if "hr" in duration and "min" in duration:
            #Hours
            hours, minute = duration.split(" hr. ")
            minutes += int(hours) * 60

            #Minutes
            minute = minute.split(" min.")[0]
            minutes += int(minute)
        elif "hr" in duration:
            #Hours
            hours = duration.split(" hr.")[0]
            minutes += int(hours) * 60
        elif "min" in duration:
            #Minutes
            minute = duration.split(" min.")[0]
            minutes += int(minute)
        else:
            print("No duration found.")
            return ""

        return minutes * int(self.num_episodes)

    def _get_recommendations(self, browser):
        '''
        Grabs the recommended anime and the number
        of recommendations.
        '''
        import re

        #Regex conventions
        user_convention = re.compile("(?<=\"users\">).+?(?=</span>)")
        title_convention = re.compile("(?<=\"title fs10\">).+?(?=</span>)")
        
        #Get html then users and recommendations
        html_source = browser.page_source
        users = re.findall(user_convention, html_source)
        titles = re.findall(title_convention, html_source)

        #Format users to only numbers - weight autorecs as 1 user
        for i, user in enumerate(users):
            if user == "AutoRec":
                users[i] = 1
            else:
                users[i] = int(user.split(" ")[0])

        #Check for mismatch
        if len(users) != len(titles):
            print("Mismatch between number of recommendations and number of users.")
            sys.exit()

        return titles, users

    def replace_anime(self, animes, attribute):
        '''
        Replaces the names of related anime with the
        anime class object.
        '''

        if attribute == "related":
            #Replace all
            for i, anime in enumerate(self.related_anime):
                anime_object = [x for x in animes if x.name == anime.lower()]

                #Replace if found
                if anime_object:
                    self.related_anime[i] = anime_object[0]
        elif attribute == "recommendations":
            for anime in list(self.recommendations.keys()):
                anime_object = [x for x in animes if x.name == anime.lower()]

                #Replace if found
                if anime_object:
                    self.recommendations[anime_object[0]] = self.recommendations.pop(anime)
