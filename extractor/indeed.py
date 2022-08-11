from requests import get
from bs4 import BeautifulSoup


def get_pages_count(keyword):
    base_url = "https://kr.indeed.com/jobs?q="
    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print("Can not request pages")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        pagination = soup.find("ul", class_="pagination-list")
        if pagination == None:
            return 1
        pages = pagination.find_all("li", recursive=False)
        count = len(pages)
        if count >= 5:
            return 5
        else:
            return count


def extract_indeed_jobs(keyword):
    pages = get_pages_count(keyword)
    print("Founding", pages, "Pages")
    results = []
    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs"
        final_url = f"{base_url}?q={keyword}&start={page*10}"
        response = get(final_url)
        print("Requesting", final_url)

        if response.status_code != 200:
            print("Can not request pages")
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            job_list = soup.find("ul", class_="jobsearch-ResultsList")
            jobs = job_list.find_all('li', recursive=False)
            for job in jobs:
                zone = job.find("div", class_="mosaic-zone")
                if zone == None:
                    anchor = job.select_one("h2 a")
                    title = anchor['aria-label']
                    link = anchor['href']
                    company = job.find("span", class_="companyName")
                    location = job.find("div", class_="companyLocation")
                    job_data = {
                        'link': f"https://kr.indeed.com{link}",
                        'company': company.string.replace(",", ""),
                        'location': location.string.replace(",", ""),
                        'position': title.replace(",", "")
                    }
                    results.append(job_data)

    return results
