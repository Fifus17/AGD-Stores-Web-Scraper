from django.shortcuts import render

from .Scraping import RTVEuroScraper

def render_site(request):
    scraper = RTVEuroScraper.RTVEuroScraper()
    data = {'products': scraper.scrape("mikser")}
    # print(data)
    return render(request, 'index.html', data)
