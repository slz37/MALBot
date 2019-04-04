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
        self.browser = browser
        self.status = tab
        self.user_rating = self.browser.find_element_by_id("scoreval{}".format(self.ID)).text

        #Load anime page
        self.load_page()

        #Initiate empty arrays
        self.related_anime = []
        self.genres = []

        #Properties from anime page
        self.progress = browser.find_element_by_id("myinfo_watchedeps").get_attribute("value")
        self.related_anime = self.get_related_anime()        
        self.genres = self.get_genres()
        
        num_episodes = self.browser.find_element_by_xpath("//div[contains(.//span, \"Episodes:\")]").text
        self.num_episodes = num_episodes.split(" ")[1]
        self.duration = self.get_duration()

        #Done now, so return back to list
        self.close_page()

    def load_page(self):
        '''
        Loads the anime's page to grab all
        necessary info.
        '''

        #Load tab
        time.sleep(3)
        self.browser.execute_script("window.open(\"{}\");".format(self.url))
        self.browser.switch_to_window(self.browser.window_handles[1])

    def close_page(self):
        '''
        Closes the anime's page once
        we are done with it.
        '''

        #Close tab
        self.browser.close()
        self.browser.switch_to_window(self.browser.window_handles[0])

    def get_genres(self):
        '''
        Obtains a formatted string of genres for the
        current anime in list.
        '''

        #Get genres
        genres = []
        genres_unformatted = self.browser.find_elements_by_css_selector("a[href*=\"genre\"")

        for gen in genres_unformatted:
            genres.append(gen.text)

        return genres

    def get_related_anime(self):
        '''
        Grabs the related anime from the
        current page.
        '''

        #Get related anime
        related_anime = []
        related = self.browser.find_element_by_class_name("anime_detail_related_anime").text
        related_anime_full = related.split("\n")

        #Remove descriptors
        for descriptor in related_anime_full:
            name = descriptor.split(": ", 1)[1]
            related_anime.append(name)

        return related_anime

    def get_duration(self):
        '''
        Grabs the duration in minutes of the
        anime to weight by length for movies/OVAs.
        '''

        #Grab duration
        duration = self.browser.find_element_by_xpath("//div[contains(.//span, \"Duration:\")]").text
        duration = duration.split(": ")[1]
        
        #Now format to be only in units of minutes
        minutes = 0
        if "hr" in duration:
            #Hours
            hours, minute = duration.split(" hr. ")
            minutes += int(hours) * 60

            #Minutes
            minute = minute.split(" min.")[0]
            minutes += int(minute)
        elif "min" in duration:
            #Minutes
            minute = duration.split(" min.")[0]
            minutes += int(minute)
        else:
            print("No duration found.")
            return ""

        return minutes * int(self.num_episodes)

    def replace_related_anime(self, animes):
        '''
        Replaces the names of related anime with the
        anime class object.
        '''

        #Replace all
        for i, anime in enumerate(self.related_anime):
            anime_object = [x for x in animes if x.name == anime.lower()]

            #Replace if found, otherwise put placeholder
            if anime_object:
                self.related_anime[i] = anime_object[0]

    def set_ranking(self, rank):
        '''
        Sets the ranking of the anime on a
        list of plan to watch.
        '''

        self.ranking = rank
