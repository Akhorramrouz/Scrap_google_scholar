from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class Advisor:
    def __init__(self, driver, root_url = "https://scholar.google.com/"):
        self.driver = driver
        self.root_url = root_url
        self.parse_profile()
        
    def get_coauthor_link(self, co_author_html):
        soup = BeautifulSoup(co_author_html, 'html.parser')
        # Find the <a> tag within the <div> element and get the 'href' attribute
        link_element = soup.find('div', class_='gsc_rsb_aa').find('a')
        link = self.root_url + link_element['href']
        return link


    def get_top_coauthors(self):
        # Extract top co-authors
        coauthors = []
        for co_author in self.driver.find_elements(By.CLASS_NAME, "gsc_rsb_aa"):
            co_author_name = co_author.text.split("\n")[0]
            co_author_scholar_link = self.get_coauthor_link(co_author.get_attribute("outerHTML"))
            coauthors.append((co_author_name, co_author_scholar_link))
        return coauthors
    
    
    def get_top_papers(self):
        top_papers = []
        for paper in self.driver.find_elements(By.CLASS_NAME, "gsc_a_tr"):
            link = self.root_url + BeautifulSoup(paper.get_attribute("outerHTML"),'html.parser').find('a')['href']
            title = paper.text.split("\n")[0]
            authors = paper.text.split("\n")[1].split(",")
            number_citations = 0
            if len(paper.text.split("\n")[-1].split()) > 1:
                number_citations = paper.text.split("\n")[-1].split()[0]
                
            publication_year = paper.text.split("\n")[-1].split()[-1]
            # Append the paper data to the list
            top_papers.append({
                'title': title,
                'link': link, 
                'authors': authors,
                'number_citations': number_citations,
                'publication_year': publication_year
            })
        return top_papers

    def parse_profile(self):
        # Parse the HTML
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Extract number of citations and total citations
        citations_all = soup.select('td.gsc_rsb_std')[0].text
        citations_since_2018 = soup.select('td.gsc_rsb_std')[1].text

        #Extract name
        name = self.driver.find_element(By.ID,"gsc_prf_in").text
        
        # Extract h-index
        h_index = soup.select('td.gsc_rsb_std')[2].text

        # Extract research interests
        research_interests = soup.select('div#gsc_prf_int a')
        research_interests = [interest.text for interest in research_interests]

        # Extract affiliation
        affiliation = soup.select('div.gsc_prf_il a')[0].text.strip()

        # Extract homepage link
        try:
            homepage_link = soup.select('div#gsc_prf_ivh a')[0]['href']
        except:
            homepage_link = None
            
            
        #Extract recent papers
        recent_papers = self.get_top_papers()
        
        #Extract co-authors
        co_authors = self.get_top_coauthors()
        
        #Extract scholar link
        scholar_link = self.driver.current_url
        

        # Assign the extracted data to instance variables
        self.scholar_link = scholar_link
        self.name = name
        self.citations_all = int(citations_all)
        self.citations_since_2018 = int(citations_since_2018)
        self.h_index = int(h_index)
        self.research_interests = research_interests
        self.affiliation = affiliation
        self.homepage_link = homepage_link
        self.recent_papers = recent_papers
        self.top_co_authors = co_authors




