'''
All imports used
'''

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.common.keys import Keys

import re, sys, os, time

import getpass
import psutil as psutil
import pickle
