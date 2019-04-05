from .libs import *
import getpass
import psutil as psutil

def detect_free_browser():
    '''
    Checks system processes for
    a free browser to use.
    '''
    
    chrome = False
    firefox = False
    opera = False
    edge = False

    for proc in psutil.process_iter():
        proc_name = proc.name()

        #Check if browser open
        if proc_name == "chrome.exe":
            chrome = True
        elif proc_name == "firefox.exe":
            firefox = True
        elif proc_name == "MicrosoftEdge.exe":
            opera = True
        elif proc_name == "opera.exe":
            edge = True
        else:
            continue

    #Browser hierarchy
    if not chrome:
        return "Chrome"
    elif not firefox:
        pass #Not working right now
        #return "Firefox"
    elif not opera:
        return "Opera"
    else:
        return None

def choose_free_browser():
    '''
    Selects a browser that is not currently
    in use by the user to run the program.
    '''
    sys.path.append(os.path.join(os.path.dirname(__file__) + "\\drivers"))
    
    free_browser = detect_free_browser()
    if free_browser == "Chrome":
        '''
        Works when no sessions open
        '''
        
        #Driver options
        WINDOW_SIZE = "1920, 1080"
        options = ChromeOptions()

        #Choose driver
        try:
            CHROME_PATH = "C:\\Users\\" + getpass.getuser() + \
                          "\\AppData\\Local\\Google\\Chrome\\User Data\\"
        except:
            print("Could not find Chrome path.")
            sys.exit
            
        DRIVER_PATH = os.path.join(os.path.dirname(__file__), "..\..\drivers\chromedriver")
        options.add_argument("user-data-dir={}".format(CHROME_PATH))
    
        #Window properties
        #options.add_argument("--headless")  
        options.add_argument("--window-size=%s" % WINDOW_SIZE)

        #Initiate driver and load page
        browser = webdriver.Chrome(
            executable_path = DRIVER_PATH,
            chrome_options = options
            )
    elif free_browser == "Firefox":
        '''
        Freezes when loading page
        '''
        
        #Driver options
        WINDOW_SIZE = "1920, 1080"
        options = FirefoxOptions()
        
        #Choose driver
        try:
            FIREFOX_PATH = "C:\\Users\\" + getpass.getuser() + \
                       "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\03nhhp88.default"
        except:
            print("Could not find Firefox path.")
            sys.exit

        DRIVER_PATH = os.path.join(os.path.dirname(__file__), "..\..\drivers\geckodriver")
        ffprofile = webdriver.FirefoxProfile(FIREFOX_PATH)

        #Window properties
        #options.add_argument("--headless")
        options.add_argument("--window-size=%s" % WINDOW_SIZE)

        #Initiate driver and load page
        browser = webdriver.Firefox(
            options = options,
            executable_path = DRIVER_PATH,
            firefox_profile = ffprofile
            )
    elif free_browser == "Opera":
        '''
        Works when no sessions open
        '''
        
        #Driver options
        WINDOW_SIZE = "1920, 1080"
        options = OperaOptions()

        options.binary_location = "C:\\Users\\" + getpass.getuser() + \
                                  "AppData\\Local\\Programs\\Opera\\58.0.3135.131\\opera.exe"

        #Choose driver
        try:
            OPERA_PATH = "C:\\Users\\" + getpass.getuser() + \
                          "\\AppData\Roaming\\Opera Software\\Opera Stable"
        except:
            print("Could not find Opera path.")
            sys.exit
            
        DRIVER_PATH = os.path.join(os.path.dirname(__file__), "..\..\drivers\operadriver")
        options.add_argument("user-data-dir={}".format(OPERA_PATH))
    
        #Window properties
        #options.add_argument("--headless")  
        options.add_argument("--window-size=%s" % WINDOW_SIZE)

        #Initiate driver and load page
        browser = webdriver.Opera(
            executable_path = DRIVER_PATH,
            options = options
            )
    else:
        print("No free browser.")
        sys.exit()

    browser.get(u"https://myanimelist.net/")

    #Skip privacy policy
    try:
        browser.find_element_by_xpath("//html//body//div[7]//div//div[2]//div//button").click()
    except:
        pass
    
    return browser

def verify_login():
    '''
    Checks the html after attempting to
    login to confirm whether login
    was successful.
    '''
    
    #Check for logout form
    forms = browser.find_elements_by_xpath("//form[@action=\"https://myanimelist.net/logout.php\"]")
    if forms:
        print("Login successful")
        return
    else:
        print("Please login to MAL before running this program.")
        sys.exit()

def goto_anime_list(tab = ""):
    '''
    Moves to anime list and gathers the urls and
    names of all anime in list. If list default
    is not all anime, this will only grab the
    ones from the current tab.
    '''
    time.sleep(3)

    #Go to specified tab, otherwise default
    if tab:
        browser.get(LIST_URL + "?status={}&tag=".format(TABS[tab]))
    else:
        browser.get(LIST_URL)

    #Get anime and urls
    anime_list = browser.find_elements_by_class_name("animetitle")
    urls = browser.find_elements_by_xpath("//*[@class=\"animetitle\"]")

    return urls, anime_list

def get_user_list_url():
    '''
    Once logged in, grabs the url
    of the user's anime list.
    '''

    url = browser.find_element_by_xpath("//*[@class=\"header-profile-link\"]").text

    return url

#Regex patterns
ID_PATTERN = re.compile("(?<=/)[\d]+(?=/)")

#MAL Anime List Tabs
TABS = {
        "Currently Watching": 1,
        "Completed": 2,
        "On Hold": 3,
        "Dropped": 4,
        "Plan to Watch": 6,
        "All Anime": 7
        } 

browser = choose_free_browser()
verify_login()

LIST_URL = u"https://myanimelist.net/animelist/{}".format(get_user_list_url())


def login():
    ##############
    # DEPRECATED #
    ##############
    
    '''
    First method for obtaining user credentials
    and logging in to MAL. Replaced with grabbing cookies
    from browser instead, so user does not have to enter
    their credentials to an untrusted source.
    '''
    
    #User info
    MAL_PAYLOAD = {
        "user_name": input("MAL Username: "),
        "password": input("MAL Password: "),
        }

    #Regex patterns
    ID_PATTERN = re.compile("(?<=/)[\d]+(?=/)")

    #MAL Anime List Tabs
    TABS = {
            "Currently Watching": 1,
            "Completed": 2,
            "On Hold": 3,
            "Dropped": 4,
            "Plan to Watch": 6,
            "All Anime": 7
            } 

    #Urls
    LOGIN_URL = u"https://myanimelist.net/login.php"
    LIST_URL = u"https://myanimelist.net/animelist/{}".format(MAL_PAYLOAD["user_name"])

    #Driver Options - Hide Window
    CHROMEDRIVER_PATH = "chromedriver"
    WINDOW_SIZE = "1920, 1080"
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    #Initiate driver and load page
    browser = webdriver.Chrome(
        executable_path = CHROMEDRIVER_PATH,
        chrome_options = chrome_options
        )
    browser.get(LOGIN_URL)

    #Skip privacy policy
    try:
        browser.find_element_by_xpath("//html//body//div[7]//div//div[2]//div//button").click()
    except:
        pass

    #Login
    username = browser.find_element_by_id("loginUserName")
    password = browser.find_element_by_id("login-password")
    username.send_keys(MAL_PAYLOAD["user_name"])
    password.send_keys(MAL_PAYLOAD["password"])
    time.sleep(3)
    browser.find_element_by_xpath("//input[@value=\"Login\"]").click()

    verify_login()
