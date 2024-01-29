from django.shortcuts import render
from django.http import HttpResponse
from .Scraping import RTVEuroScraper

def render_site(request):
    search_term = request.POST.get('search', '')
    sort_by = request.GET.get('sort', '')
    sort_direction = request.GET.get('sort_direction', '0')

    # Check if search term is provided
    if search_term:
        scraper = RTVEuroScraper.RTVEuroScraper()
        products = scraper.scrape(search_term)

        # Store scraped data in session storage
        request.session['products'] = products
        request.session['search_term'] = search_term
    else:
        # Retrieve stored data from session storage
        products = request.session.get('products', [])
        search_term = request.session.get('search_term', '')
        sort_direction = request.GET.get('sort_direction', '0')

    if sort_by == 'price':
        products = sorted(products, key=lambda x: int(x['price'].replace(' ', '').replace(',', '')))

        if sort_direction == '1':
            products = list(reversed(products))

    elif sort_by == 'review':
        products = sorted(products, key=lambda x: float(x['review']) if x['review'] != 'No reviews' else -1)

        if sort_direction == '1':
            products = list(reversed(products))

    if sort_by == 'no_review':
        products = sorted(products, key=lambda x: int(x['no_reviews'].replace(' ', '').replace(',', '')))

        if sort_direction == '1':
            products = list(reversed(products))


    data = {'products': products, 'search': search_term, 'sort_direction': sort_direction, 'current_sort': sort_by}
    return render(request, 'index.html', data)
