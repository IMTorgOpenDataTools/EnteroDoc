#!/usr/bin/env python3
"""
Test the Crawler class.
"""

from backend.services.url_to_pdf import (
    Crawler,
    domains_workflow
)
from backend.services.url import UniformResourceLocator
from backend.services._constants import logger

from pathlib import Path



def test_domains_workflow():
    post_data = {
        'domainUrl':['https://www.jpmorgan.com']
        }
    tmp = domains_workflow(post_data)

    assert tmp == True


#setup
url = 'https://www.jpmorgan.com'
UrlCrawler = Crawler(url, logger)





def test_get_initial_url_list():
    #list_of_search_terms = ['credit', 'card', 'terms', 'conditions']
    list_of_search_terms = ['creditcard`, `fees', 'terms conditions', 'overdraft', 'non in sufficient funds']
    initial_list = UrlCrawler.get_initial_url_list(url, 
                                                   list_of_search_terms
                                                   )
    assert len(initial_list) > 1
"""
def test_get_hrefs_within_depth():
    url = 'https://www.google.com'
    hrefs = get_hrefs_within_depth(url)
    assert len(hrefs) > 0







def test_run_process_steps():
    output_name = Path() / 'pdfs' / 'test'
    url = 'https://www.jpmorgan.com'
    hrefs = get_hrefs_within_depth(url)
    pdfs = url_to_pdf(hrefs, N=4)
    result = save_combine_pdfs(pdfs, output_name)
    
    assert result == True



"""