# -*- coding: utf-8 -*-
"""sitemap webscraping.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hZekIVS0PYTpPfxBov2bjMiFFDwHxN_N
"""

# Installing required libaries
!pip install requests
!pip install BeautifulSoup4
!pip install pandas
!pip install lxml

#import required models
import requests
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd

"""# **Ugaoo.com**
Ugaoo is an online platform that specializes in selling a variety of indoor plants at different price points. They offer a wide range of indoor plants, catering to various preferences and budgets.

When scraping the Ugaoo website, you'll use web scraping techniques to extract information such as plant names, descriptions, prices, and any other relevant details displayed on their product pages. This data extraction can help gather insights into the types of indoor plants they offer, their pricing structure, and potentially customer reviews or ratings. Just make sure to review and comply with the website's terms of use and any legal considerations related to web scraping.
"""

# Checking the sitemap of website
sitemap_url = "https://www.ugaoo.com/sitemap.xml"
response = requests.get(sitemap_url)

# Check the response status
if response.status_code == 200:
  sitemap_content = response.content
else:
  print(f"Failed to fetch sitemap from {sitemap_url}")

# Parse the sitemap XML
sitemap_xml = etree.fromstring(sitemap_content)
nsmap = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap_urls = sitemap_xml.xpath("//s:sitemap/s:loc/text()", namespaces=nsmap)
for sitemap in sitemap_urls:
  print(sitemap)

def product_scrap():
    # Enter the sitemap URL
    sitemap_url = "https://www.ugaoo.com/sitemap.xml"
    response = requests.get(sitemap_url)

    # Check the response status
    if response.status_code == 200:
        sitemap_content = response.content
    else:
        print(f"Failed to fetch sitemap from {sitemap_url}")
        return

    # Parse the sitemap XML
    sitemap_xml = etree.fromstring(sitemap_content)
    nsmap = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    sitemap_urls = sitemap_xml.xpath("//s:sitemap/s:loc/text()", namespaces=nsmap)
    # Get product details from the first URL
    url_find = sitemap_urls[:1]

    # Parse and print URLs from linked sitemaps
    product_details = {'product_name': [], 'product_url': [], 'Rating': [], 'Actual Price': [], 'Discount Price': [],
                       'In-Box': [], 'perks': [], 'About Product': [], 'Testimonial': [], 'preception': [],
                       'Brief Detail': []}
    for sitemap_url in url_find:
        response = requests.get(sitemap_url)
        try:
            if response.status_code == 200:
                sitemap_content = response.content
                sitemap_xml = etree.fromstring(sitemap_content)
                urls = sitemap_xml.xpath("//s:loc/text()", namespaces=nsmap)
                new = urls[700:800]  # Adjust the range as needed
                # Checking the product details only for URLs
                index = 0
                while index < len(new):
                    url = new[index]
                    try:
                        response = requests.get(url)
                        product_details['product_url'].append(url)
                        if response.status_code == 200:
                            page_content = response.text
                            soup = BeautifulSoup(page_content, "html.parser")

                            # Getting the title of Product
                            item = soup.find('h1', class_='h2')
                            if item:
                                item_name = item.text.replace('\n', '').strip()
                                product_details['product_name'].append(item_name)
                            else:
                                print('Title not found')

                            # Getting rating of Product
                            for div in soup.find_all('div', class_='jdgm-rev-widg__summary-stars'):
                                if 'aria-label' in div.attrs:
                                    rating = div['aria-label']
                                    product_details['Rating'].append(rating)
                                else:
                                    print('Rating not found')

                            # Getting the Product Price
                            item_price = soup.find('span', class_='price-item price-item--sale')
                            if item_price:
                                price = item_price.text.replace('/n', '').strip()
                                product_details['Discount Price'].append(price)
                            else:
                                product_details['Discount Price'].append('Price not found')

                            # Getting the list of perks which comes with product
                            options = soup.find('div', class_="guarantees-main")
                            if options:
                                text = options.get_text(separator=' ', strip=True)
                                perks = text.replace('\n ', ' , ')
                                product_details['perks'].append(perks)
                            else:
                                product_details['perks'].append('Perks not available')

                            # Getting the list of details about the product
                            about = soup.find('span', class_="metafield-multi_line_text_field")
                            if about:
                                about_item = about.text
                                product_details['About Product'].append(about_item)
                            else:
                                product_details['About Product'].append('Product details not available')

                            # Getting the Testimonial of product
                            testimonials = soup.find_all('div', class_="rte typeset2")
                            if testimonials:
                                combined_testimonials = '\n'.join(testimonial.get_text(strip=True) for testimonial in
                                                                testimonials)
                                product_details['Testimonial'].append(combined_testimonials)
                            else:
                                product_details['Testimonial'].append('Testimonial not available')

                            product_precreption = []
                            for product_desc in soup.find_all('span', class_='accordion__title'):
                                if product_desc:
                                    collection_bio = product_desc.text.strip()
                                    product_precreption.append(collection_bio)
                                else:
                                    product_precreption.extend('none')

                            product_details['preception'].append(product_precreption)

                            real_price = soup.find('s', class_="price-item price-item--regular")
                            if real_price:
                                actual_rate = real_price.text.replace('\n', '').strip()
                                product_details['Actual Price'].append(actual_rate)
                            else:
                                product_details['Actual Price'].append('No discount')

                            box_detail = []
                            with_box = soup.find('div', class_="content_section")
                            if with_box:
                                box = with_box.text.replace('\n', ' ').strip()
                                box_detail.append(box)
                            else:
                                box_detail.append('none')
                            product_details['In-Box'].append(box_detail)

                            brief_detail = []
                            detail = soup.find('div', class_="prod-bottom-desc")
                            if detail:
                                detail_box = detail.text.replace('\n', ' ').strip()
                                brief_detail.append(detail_box)
                            else:
                                brief_detail.append('none')
                            product_details['Brief Detail'].append(brief_detail)
                        else:
                            print(f"Failed to fetch the details from {url}")
                    except Exception as e:
                        print(f"Failed to process URL {url}: {e}")
                    finally:
                        index += 1
            else:
                print(f"Failed to fetch sitemap from {sitemap_url}")
        except Exception as e:
            print("Failed:", e)
    return product_details

#saving data into a pandas dataframe
data_df = pd.DataFrame.from_dict(product_scrap(), orient='index').T
data_df

"""# checking the description of items"""

def contect_scrap():
  from typing_extensions import Text
  sitemap_url = "https://www.ugaoo.com/sitemap.xml"
  response = requests.get(sitemap_url)

  #checking the response status
  if response.status_code ==200:
    sitemap_content = response.content

    #Parse the sitemap XML
    sitemap_xml = etree.fromstring(sitemap_content)
    nsmap = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    sitemap_urls = sitemap_xml.xpath("//s:sitemap/s:loc/text()", namespaces=nsmap)

    #getting product details from first url
    url_find = sitemap_urls[1:2]

    # Parse and print URLs from linked sitemaps
    data = {"About": [],
            "Contact": set(),
            "offering": set(),
            "Subscription":set(),
            "FAQ":[],
            "Privacy Policy": set(),
            "Dr_green":[]}

    for sitemap_url in url_find:
      response = requests.get(sitemap_url)
      if response.status_code == 200:
        try:
          sitemap_content = response.content
          sitemap_xml = etree.fromstring(sitemap_content)
          urls = sitemap_xml.xpath("//s:loc/text()", namespaces=nsmap)

          #checking the product details only for 50 url
          for url in urls:

            #pass the request to url
            response = requests.get(url)

            #check the status code
            if response.status_code == 200:
              page_content = response.text
              #parse the Beautifulsoup library
              soup = BeautifulSoup(page_content, "html.parser")


              #Getting the About section from website
              collection_element = soup.find_all('h2', class_="image-with-text__heading h1")
              text = soup.find_all('div',class_="image-with-text__text typeset rte")
              if collection_element and text:
                for content, text in zip(collection_element, text):
                  content_text = content.text
                  data['About'].append(content_text)
                  content_t = text.text
                  data['About'].append(content_t)
              else:
                pass

              #Getting the Office Address in all india
              office_text = soup.find_all('ul',class_="contact__list list-unstyled")
              other_office = soup.find_all('div',class_="multicolumn-card__info")

              if office_text:
                for location in office_text:
                  address = location.text.replace('\n',' ').strip()
                  data['Contact'].add(address)
              #Adding the the Office address in the set
              if other_office:
                for office in other_office:
                  other_address = office.text.replace('Map ↗',' ').replace('\n',' ').strip()
                  data['Contact'].add(other_address)


              #Getting what special things they are offering
              offer = soup.find_all('div',class_="grid grid--2-col grid--1-col-mobile grid--3-col-tablet grid--4-col-desktop")
              if offer:
                for fact in offer:
                  best = fact.text.replace('\n',' ').strip()
                  data['offering'].add(best)

              # Getting festival special offers
              detail_offering = soup.find('div',class_="page-width section-template--15634890391684__d99ad2c9-10be-4d58-a044-fc6d4265e7d1-padding")
              if detail_offering:
                festive_special = detail_offering.text.replace('\n','').strip()
                data['offering'].add(festive_special)


              #Getting the frequenctly Asking Question
              questions = soup.find_all('div', class_="faq page-width page-width--inner")
              if questions:
                for question in questions:
                # Find FAQ section title
                  faq_title = question.find('h2', class_='title h2')
                  if faq_title:
                    title = faq_title.text.replace('\n', '')
                    if title not in data['FAQ']:
                      data['FAQ'].append(title)

                    # Find FAQ questions and answers
                      faq_question = question.find_all('summary')
                      faq_answer = question.find_all('div', class_="rte typeset")
                      for all_faq_question, all_faq_answer in zip(faq_question, faq_answer):
                        if all_faq_question and all_faq_answer:
                          quest = all_faq_question.text.replace('\xa0','').strip()
                          if quest not in data['FAQ']:
                            data['FAQ'].append(quest)
                            answer = all_faq_answer.text.replace('\xa0','').strip()
                          if answer not in data['FAQ']:
                            data['FAQ'].append(answer)

              dr = soup.find('div',class_="page-width section-template--15634892062852__d1e3ae70-0e12-494d-8581-cdce69aa9788-padding")
              if dr:
                dr_green = dr.text.replace('\n','').strip()
                data['Dr_green'].append(dr_green)

              sub = soup.find_all('div',class_="farm-setup")
              if sub:
                for subscription in sub:
                  data['Subscription'].add(subscription.text.replace('\n\n','').replace('\n','').strip())

              privacy = soup.find('section',class_="staticSection section-container")
              if privacy:
                policy = privacy.text.replace('\n','').strip()
                data['Privacy Policy'].add(policy)
        except Exception as e:
            print("Erorr found",e)
    return data

description =contect_scrap()

print(description)

"""# **Ntropy.com**
Ntropy is a company that specializes in developing advanced tools for understanding and organizing financial data from various sources around the world. Their goal is to break down the barriers created by data being stored in separate systems and formats, making it challenging to work with efficiently.

To scrape the Ntropy website means to extract data from their web pages automatically. You could use web scraping tools to gather information from their site, such as details about their services, mission, and how they aim to revolutionize financial data management. This data extraction can be useful for research, analysis, or understanding more about what Ntropy offers. However, it's essential to ensure that you follow ethical guidelines and any terms of service related to web scraping when gathering this information.
"""

url = 'https://www.ntropy.com/blog/better-lending-decisions-faster-financing'
response = requests.get(url)
page_content = response.text
doc = BeautifulSoup(page_content,'html.parser')
bio = []
href_list =  doc.find_all('div',class_="pb-12 lg:pb-20 wrapper")
for new in href_list:
  tag = new.find_all('div',class_="flex-col items-start lg:grid lg:grid-cols-blog gap-x-6")
  for all in tag:
    print(all.text)
# for new in href_list:
#   inl = new.text
# print(href_list.text)

def ntropy_scrap():
  from typing_extensions import Text
  sitemap_url = "https://www.ntropy.com/sitemap.xml"
  response = requests.get(sitemap_url)

  #checking the response status
  if response.status_code ==200:
    sitemap_content = response.content

    #Parse the sitemap XML
    sitemap_xml = etree.fromstring(sitemap_content)
    nsmap = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    sitemap_urls = sitemap_xml.xpath("//s:sitemap/s:loc/text()", namespaces=nsmap)

    # Parse and print URLs from linked sitemaps
    data = {"about":[],
            "Privacy_policy":[],
            "Product":[],
            "blog":[]
            }

    for sitemap_url in sitemap_urls:
      response = requests.get(sitemap_url)
      if response.status_code == 200:
        try:
          sitemap_content = response.content
          sitemap_xml = etree.fromstring(sitemap_content)
          urls = sitemap_xml.xpath("//s:loc/text()", namespaces=nsmap)

          #checking the product details only for 50 url
          for url in urls:

            #pass the request to url
            response = requests.get(url)

            #check the status code
            if response.status_code == 200:
              page_content = response.text
              #parse the Beautifulsoup library
              soup = BeautifulSoup(page_content, "html.parser")


              #Getting the About section from website
              phase = soup.find_all('h3', class_="text-h3 text-white")
              if phase:
                for first_phase in phase:
                  data['about'].append(first_phase.text)
              phase2 = soup.find('div', class_="grid grid-cols-1 gap-5 pt-16 pb-20 md:pb-24 md:pt-20 lg:pb-40 lg:pt-30 wrapper lg:grid-cols-3")
              if phase2:
                for second_phase in phase2:
                  data['about'].append(second_phase.text)
              phase3 = soup.find('h4', class_="text-h4 mb-32")
              if phase3:
                for third_phase in phase3:
                  data['about'].append(third_phase.text)
              phase4 = soup.find('div', class_="flex flex-col gap-20 py-10 md:gap-8 md:pb-28 lg:hidden")
              if phase4:
                for fourth_phase in phase4:
                  data['about'].append(fourth_phase.text)

              privacy = soup.find('main', class_="max-w-6xl pb-10 wrapper md:pb-15 lg:pb-30")
              if privacy:
                for policy in privacy:
                  data['Privacy_policy'].append(policy.text.replace(' \xa0','').strip())

              product_row =  soup.find('div', class_="flex-col flex h-[360px] sm:h-[400px] lg:h-[720px] lg:max-w-[540px] py-10 md:py-20 sm:justify-center justify-start max-lg:wrapper")
              context = soup.find('h4',class_="text-h4 md:pr-0 pr-11 max-w-[1140px]")
              benefit = soup.find_all('div', class_="max-w-[500px]")
              more_benefit = soup.find_all('section', id="benefits")
              if product_row:
                product_context = context.text
                text_with_spaces = ' '.join(product_row.stripped_strings)
                product_benefit = ' '.join(' '.join(element.stripped_strings) for element in benefit)
                product_more = ' '.join(' '.join(element.stripped_strings) for element in more_benefit)
                if text_with_spaces not in data['Product']:
                  data['Product'].append(text_with_spaces)
                  data['Product'].append(product_context)
                  data['Product'].append(product_benefit)
                  data['Product'].append(product_more)

              paragraph =[]
              page = soup.find_all('div',class_="pb-12 lg:pb-20 wrapper")
              # details = soup.find('main',class_="max-w-6xl pb-10 wrapper md:pb-15 lg:pb-30")
              if page:
                for page_context in page:
                  # heading = page_context.find_all('h2',class_="text-h5 leading-snug col-start-1 col-end-2 mb-4 max-w-[320px]")
                  title = page_context.find_all('h1',class_="text-h2")
                  para = page_context.find_all('div',class_="flex-col items-start lg:grid lg:grid-cols-blog gap-x-6")

                  for head,graph in zip(title, para):
                    paragraph.append(head.text)
                    # paragraph.append(sub_title.text.replace('\xa0','').replace('\u2060','').strip())
                    paragraph.append(graph.text.replace('\xa0','').replace('\u2060','').strip())

              data['blog'].append(paragraph)


        except Exception as e:
            print("Erorr found",e)
        return data

ntropy_scrap()

#Sacing data as csv
import csv
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category', 'Content'])
        for category, content in data.items():
            for item in content:
                writer.writerow([category, item])

if __name__ == "__main__":
    data = ntropy_scrap()
    save_to_csv(data, 'ntropy_data.csv')