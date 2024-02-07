from django.shortcuts import render
import requests
import bs4

# Create your views here.
def home(request):

    element = None
    items = []

    if request.method == 'POST':
        if 'send' in request.POST:
            web_url = request.POST['url']
            element = request.POST['element']
            resp_data = requests.get(web_url)
            scrap_data = bs4.BeautifulSoup(resp_data.text,'html.parser')
            data = scrap_data.find_all(element)

            for row in data:
                if element == 'img':
                    items.append(row.get('src'))
                elif element == 'p':
                    items.append(row.get_text())
                elif element == 'a':
                    items.append(row.get('href'))
                    # print(items)
                elif element == 'table':
                    tr_data = row.find_all('tr')
                    for row2 in tr_data:
                        td_data = []
                        td_list = row2.find_all('td')
                        for row3 in td_list:
                            try:
                                p_data = row3.find('p')
                                td_data.append(p_data.get_text())
                            except:
                                td_data.append(row3.find_all('p'))
                        items.append(td_data)
                        print(items)

    return render(request,'image_gallery.html',{'obj':items,'e_type':element})