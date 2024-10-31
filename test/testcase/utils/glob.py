# Headers
import pytest
import shutil
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Global variables
home_page_url = "http://127.0.0.1:8000/"    # Home page for ASE project
nqueens_page_url = "http://127.0.0.1:8000/nqueens"
nqueens_solution_page_url = "http://127.0.0.1:8000/nqueens/puzzle"

# Global Selectors
chess_icon_css_selector = ".logo img"   # The chess icon navigating to home page

input_box_id_selector = "id_n"

nqueens_title_xpath_selector = "//table[@class='puzzle-card']//tbody//tr[@class='puzzle-title']//th[text()='N Queens']"
nqueens_navbar_xpath_selector = "//a[@href='/nqueens']"

button_solve_it_yourself_xpath_selector = "//*[contains(@class, 'btn') and contains(@class, 'btn-primary')]"
button_go_to_solution_xpath_selector = "//*[contains(@class, 'btn') and contains(@class, 'btn-success')]"
button_get_a_possible_solution_xpath_selector = "//*[contains(@class, 'btn') and contains(@class, 'btn-success')]"
button_check_your_solution_xpath_selector = "//*[contains(@class, 'btn') and contains(@class, 'btn-primary') and contains(@class, 'mt-3')]"

table_chess_board_xpath_selector = "//table[@id='nqueens-board']"

link_xpath_selector = "//footer//a[1]"