import requests
import time
import re
import lxml
from bs4 import BeautifulSoup

# Yellow Pages Web Scraper Using BeautifulSoup
pages = []
companies = []
urls = []

# You can have your own keywords to search if you want
keywords = ["Accountants", "Dentists", "Pharmacies", "Doctors+Medical+Practitioners", "Solicitors", "Estate+Agents", "Hotels", "Function+Rooms+And+Banqueting", "Electricians", "Plumbers", "Gas+Engineers", "Taxis+And+Private+Hire+Vehicles", "Garage+Services", "Carpenters+And+Joiners", "Taxis+And+Private Hire Vehicles", "Cafes+And+Coffee+Shops", "Restaurants", "Architects", "Builders",
            "Skip+Hire", "Car+Body+Repairs", "Tyres", "Barbers", "Fencing+Services", "Dry+Cleaners", "Vets"]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

for keyword in keywords:             #You could make a variable to choose your own location here ↓
    url_link = 'https://www.yell.com/ucs/UcsSearchAction.do?find=Y&keywords='+keyword+'&location=uk&pageNum=%s' 
    urls.append(url_link)

for url in urls:
    # Increment pageNum up to 10 to scrape all pages of all given Keywords
    for i in range(1,11):
      pages.append(url % i)

print(len(pages), "Pages to scrape")

if len(pages) > 0:
    try:
      for page in pages:
        response = requests.get(page, headers = headers)
        page_html = response.text
        page_soup = BeautifulSoup(page_html, 'xml')

        # Find the business 'capsule' of information per page
        business_listings = page_soup.find_all("div", attrs={
            "class": "col-sm-15 col-md-14 col-lg-15 businessCapsule--mainContent"})  # 25 per page
        for listing in business_listings:
            # Locate company url within a HTML <a> tag href by Stringifying it and applying a url finding regex command
            name = listing.find("span", attrs={"class": "businessCapsule--name"}).getText()
            number = listing.find("span", attrs={"class": "business--telephoneNumber"}).getText()
            website = str(listing.find("a", attrs={"rel": "nofollow noopener"}))
            web_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                 website)
            companies.append({"Name": name, "Number": number,
                              "Website": str(web_url)})
            print(len(companies), "listings found")
        time.sleep(20) # Keep Yell.com happy and not overload the requests bruh
    except:
        print('Page Not Found!')

print(companies)
for company in companies:
    print(str("Company: " + company["Name"] + " -- " + company["Number"] + " -- " + company["Website"]))
