import unittest
from unittest import mock
from Metacritic_Scraper import MetaCriticScraper
from data_cleaning import DataCleaning
from unittest.mock import patch
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InvalidArgumentException
import time
import tracemalloc

"""
Unittest Suite: 
Sample Unittest Suite for the current version  
  
"""
tracemalloc.start()


class MetacriticWebscraperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("teardownClass")

    def setUp(self):
        self.scraper = MetaCriticScraper("https://www.metacritic.com/")
        time.sleep(5)

    @unittest.skip
    def test_get_information_from_page(self):
        """
        Unittest to ensure that information is being collected
        from variety of pages
        Returns: An instance of a dict if True
        Types of pages tested:
        Pages within the Games section of the website
        Pages with an 'expand' button under their descriptions
        Pages with varying Metascores: good, average and bad

        """
        # Good game root = "https://www.metacritic.com/game/xbox/halo-combat-evolved"
        # Bad game root = "https://www.metacritic.com/game/gamecube/charlies-angels"
        # Mixed game root = "https://www.metacritic.com/game/pc/white-shadows
        test_urls = [
            "https://www.metacritic.com/game/gamecube/charlies-angels",
            "https://www.metacritic.com/game/xbox/halo-combat-evolved",
            "https://www.metacritic.com/game/pc/white-shadows",
        ]

        # Iterate through each url in the list
        # to see if it generates a dictionary output
        for url in test_urls:
            self.scraper.driver.get(url)
            time.sleep(2)
            test_input = self.scraper._get_information_from_page()
            self.assertIsInstance(test_input, dict)

    tracemalloc.reset_peak()

    @unittest.skip
    def test_collect_number_of_pages(self):
        """
        Unittest to determine the maximum number of pages in
        each section of the website
        Returns:
        An Integer to be as a value in iterating through each of the
        pages on the website.
        The test uses the method on a page with page numbers on the website,
        and tries to match the expected_output variable with the variable
        that the method returns.
        """
        # TODO: find a way to pass in multiple urls to test the method

        test_page = "https://www.metacritic.com/browse/games/genre/date/racing/all"

        self.scraper.driver.get(test_page)
        test_input = self.scraper.collect_number_of_pages(
            "#main_content > div.browse.new_releases > div.content_after_header > \
                div > div.next_to_side_col > div > div.marg_top1 > div > div > div.pages > ul > \
                li.page.last_page > a"
        )

        expected_output = 17

        self.assertEqual(expected_output, test_input)

    tracemalloc.reset_peak()

    @unittest.skip
    def test_extract_page_links(self):
        '''
        Unittest to test the extract_page_links method 

        '''
        test_page = "https://www.metacritic.com/browse/albums/genre/date/electronic"
        self.scraper.driver.get(test_page)
        test_input = self.scraper.extract_page_links('//a[@class="title"]', "href")

        # Test if the output is a list 
        self.assertIsInstance(test_input, list)
        # Test if the length of the list is 100 on the webpage 
        self.assertEqual(len(test_input), 100)

    @unittest.skip
    def test_land_first_page(self):
        '''
        Unittest to determine if the first page is being found 

        '''
        test_url = "https://www.metacritic.com/"
        home_page = self.scraper.land_first_page(test_url)
        self.assertIsNone(home_page)

    # #TODO: Implement unittests' patch module to simulate the webdriver
    #     with patch('selenium.webdriver.Chrome') as mock_first_page:

    #         mock_first_page.return_value = test_url
    #         test_url = "https://www.metacritic.com/"
    #         home_page = self.scraper.land_first_page(test_url)
    #         mock_first_page.assert_called_with(home_page)

    @unittest.skip
    def test_accept_cookies(self):
        '''
        Unittest to determine if the accept cookies button is being clicked on the webpage

        '''
        self.assertTrue(
            self.scraper.accept_cookies('//button[@id="onetrust-accept-btn-handler"]')
        )

    @unittest.skip
    def test_save_json(self):
        # TODO: Debug this error:
        # TypeError: Object of type TextIOWrapper is not JSON serializable
        with open("test_scraper_output.txt", "r", encoding="utf-8-sig") as test_file:
            content_dict = []
            contents = test_file.readlines()
            for content in contents:
                content_dict.append(eval(content))
            print(content[:5])
            print(type(content))
            test_json = self.scraper.save_json(
                content_dict, sub_category_name="fighting_games"
            )

            print(test_json)
            self.assertTrue(test_json, True)

    @unittest.skip
    def test_record_check(self):

        # Use a sample record like so
        sample_record = {
            "uuid": "c505f129-8923-4f4e-be95-976c2fa3b2c2",
            "title": "YATAGARASU: ATTACK ON CATACLYSM",
            "link_to_page": "https://www.metacritic.com/game/pc/yatagarasu-attack-on-cataclysm",
            "platform": "PC",
            "release_date": "Jul 7, 2015",
            "metacritic_score": "tbd",
            "user_score": "tbd",
            "developer": "Null",
            "description": "Null",
        }

        racing_link = (
            "https://www.metacritic.com/game/pc/need-for-speed-hot-pursuit-remastered"
        )

        # Check this record against the database
        sample_record_check = self.scraper.record_check(
            "Fighting_Games",
            "link_to_page",
        )
        table_not_present = self.scraper.record_check("Racing_Games", "link_to_page")
        # Testing that the method returns a list
        self.assertIsInstance(sample_record_check, list)
        # Testing if the link exists inside the RDS
        self.assertIn(sample_record["link_to_page"], sample_record_check)
        # Testing if a link does not exist inside the RDS
        self.assertNotIn(racing_link, sample_record_check)
        # Testing if the method returns an empty list if the table_name is not present within the database
        self.assertIsInstance(table_not_present, list )

    def tearDown(self):
        self.scraper.driver.quit()

    if __name__ == "__main__":
        unittest.main(argv=[''], verbosity=2, exit=False)
        # unittest.main()
