#!/usr/bin/env python3
"""
Test exporting to pdf.
"""

from backend.services.export_pdf import (
    url_to_pdf,
    save_combine_pdfs,
    save_individual_pdfs
)

from pathlib import Path



def test_create_pdfs():
    output_name = Path() / 'tests' / 'pdfs' / 'test'
    hrefs = ['https://www.google.com/imghp?hl=en&tab=wi',
             'https://www.gstatic.com/policies/terms/pdf/20220105/it7r24p9/google_terms_of_service_en_us.pdf', 
            'https://maps.google.com/maps?hl=en&tab=wl', 
            'https://play.google.com/?hl=en&tab=w8', 
            'https://drive.google.com/?tab=wo', 
            'https://www.google.com/intl/en/about/products?tab=wh', 
            'https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ', 
            'https://mail.google.com/mail/?tab=wm', 
            'https://news.google.com/?tab=wn'
            ]

    #comment-out
    with open('./tests/data/jpmorgan_hrefs.txt', 'r') as file:
        hrefs = [line.rstrip() for line in file]

    unique_hrefs = list(set(hrefs))
    pdfs = url_to_pdf(unique_hrefs, N=4)
    result = save_individual_pdfs(pdfs, output_name)
    #result = save_combine_pdfs(pdfs, output_name)
    
    assert result == True