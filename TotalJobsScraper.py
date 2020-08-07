import requests
import re
import lxml
from bs4 import BeautifulSoup


# TotalJobs Web Scraper Using BeautifulSoup

pages = []
jobs = []
urls = []

keywords = ["Marketing+Director", "App+Developer", "Web+Developer", "Marketing+Analyst", "Marketing+Lead", "Marketing+Executive"]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

for keyword in keywords:
    url_link = "https://www.totaljobs.com/jobs/"+keyword+"?page=%s"
    urls.append(url_link)

for url in urls:
    # Increment pageNum up to 10 to scrape all pages of all given Keywords
    for i in range(1,11):
      pages.append(url % i)

print("Amount of pages to parse:", len(pages))
if len(pages) > 0:
  for page in pages:
    response = requests.get(page, headers = headers)
    page_html = response.text
    page_soup = BeautifulSoup(page_html, 'xml')

    # Find the business 'capsule' of information per page
    job_listings = page_soup.find_all("div", attrs = {"class":"col-sm-12"})
    for listing in job_listings:
        company_name = listing.find("li", attrs={"title": "hiring organization"})
        job_title = listing.find("h2")
        website = listing.find("a")
        # Get only values for companies and not other elements with same attributes
        if website != '[]' and job_title is not None and company_name is not None:
            company_name = company_name.find("a").getText()
            job_title = job_title = listing.find("h2").getText()
            web_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                 str(website))
            jobs.append({"Name": company_name, "Job Title": job_title, "Website": str(web_url[0])})

        print(len(jobs), "listings found")

print(jobs)
for job_listing in jobs:
    print(str("Company: " + job_listing["Name"] + " -- " + job_listing["Job Title"] + " -- " + job_listing["Website"]))