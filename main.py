from Metacritic_Scraper import MetaCriticScraper

new_scraper = MetaCriticScraper("https://www.metacritic.com")
new_scraper.accept_cookies('//button[@id="onetrust-accept-btn-handler"]')
new_scraper.choose_category('game')

new_scraper.sample_scraper('list_of_fighting_links')



