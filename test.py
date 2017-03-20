from scrapers.DrugInfo import DrugInfoScraper

d = DrugInfoScraper()

s = d.search('카리메트', set_detail=True)
print(s)
