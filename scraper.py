import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
from dotenv import load_dotenv
import re
import pandas as pd
import time
# from urllib.parse import urlparse, parse_qs
load_dotenv()

# MySQL database connection
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Function to fetch website content with retry mechanism
def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we notice bad responses
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


# Function to extract meta title
def extract_meta_title(soup):
    meta_title = soup.find('title').text if soup.find('title') else ''
    return meta_title
#functu=ion to get meta description
def extract_meta_description(soup):
    try:
        meta_description = ''
        for meta in soup.find_all('meta'):
            name_attr = meta.get('name', '').strip().lower()
            if name_attr == 'description':
                meta_description = meta.get('content', '').lower()
                break
        # print(f"Meta Description: {meta_description}")
        return  meta_description
    except Exception as e:
        print(f"Error extracting meta information: {e}")
        return '', ''
    #
# Function to extract social media links
def extract_social_media_links(soup, processed_domains):
    social_media_links = []
    # url_pattern = re.compile(r'https?://[^\s]+', re.IGNORECASE)
    
    # Social media domains to look for
    social_media_domains = [
        '.instagram.com',
        '.linkedin.com',
        '.facebook.com',
        '.twitter.com',
        '.youtube.com',
        '.github.com',
        '.reddit.com',
        '.thread.com',
        '.x.com',
        '.tiktok.com',
        '.pinterest.com',
        '.snapchat.com',
        '.youtube.com'
    ]
    
    def should_ignore(url):
        for domain in social_media_domains:
            # Check if the URL starts with the domain pattern
            if re.match(rf'^https?://(www\.)?{re.escape(domain)}', url):
                return True    
            return False

    # Check for links in 'a' tags
    for link in soup.find_all('a', href=True):
        href = link['href']
        if any(domain in href for domain in social_media_domains) and not should_ignore(href):
            domain = re.findall(r'https?://([^/]+)/', href)
            if domain and domain[0] not in processed_domains :
                social_media_links.append(href)
                processed_domains.add(domain[0])


    
    # for link in soup.find_all('a', href=True):
    #     href = link['href']
    #     parsed_url = urlparse(href)
    #     query_params = parse_qs(parsed_url.query)
    #     location = query_params.get('location', [''])[0]

    #     if location and match_pattern(location):
    #         domain = re.findall(r'https?://([^/]+)/', location)
    #         if domain and domain[0] not in processed_domains:
    #             social_media_links.append(location)
    #             processed_domains.add(domain[0])

    # return ' , '.join(social_media_links)          

    # # Check for links in elements with specific IDs or classes
    # social_media_id_class = [
    #     'social', 'social-media', 'social-link', 'social-icon', '-link'
    # ]

    # for id_class in social_media_id_class:
    #     for element in soup.find_all(attrs={'id': id_class}):
    #         for link in element.find_all('a', href=True):
    #             href = link['href']
    #             if any(domain in href for domain in social_media_domains) and not should_ignore(href):
    #                 domain = re.findall(r'https?://([^/]+)/', href)
    #                 if domain and domain[0] not in processed_domains:
    #                     social_media_links.append(href)
    #                     processed_domains.add(domain[0])

    #     for element in soup.find_all(attrs={'class': id_class}):
    #         for link in element.find_all('a', href=True):
    #             href = link['href']
    #             if any(domain in href for domain in social_media_domains) and not should_ignore(href):
    #                 domain = re.findall(r'https?://([^/]+)/', href)
    #                 if domain and domain[0] not in processed_domains:
    #                     social_media_links.append(href)
    #                     processed_domains.add(domain[0])

    return ' , '.join(social_media_links)   

# Function to identify tech stack
# Function to extract CMS from a website
def detect_cms(soup):
    cms = None
    # Check for WordPress
    if soup.find('meta', attrs={'name': 'generator', 'content': re.compile('WordPress')}):
        cms = 'WordPress'
    # Check for Joomla
    elif soup.find('meta', attrs={'name': 'generator', 'content': re.compile('Joomla')}):
        cms = 'Joomla'
    # Check for Drupal
    elif soup.find('meta', attrs={'name': 'generator', 'content': re.compile('Drupal')}):
        cms = 'Drupal'
    # Check for Magento
    elif soup.find('script', attrs={'src': re.compile('mage/requirejs/mixins')}):
        cms = 'Magento'
    # Check for Shopify
    elif soup.find('link', attrs={'href': re.compile('cdn.shopify.com')}):
        cms = 'Shopify'
    # Check for Squarespace
    elif soup.find('meta', attrs={'name': 'generator', 'content': re.compile('Squarespace')}):
        cms = 'Squarespace'
    # Check for Wix
    elif soup.find('meta', attrs={'name': 'generator', 'content': re.compile('Wix')}):
        cms = 'Wix'
    return cms

def extract_tech_stack(soup):
    scripts = [script['src'] for script in soup.find_all('script', src=True)]

    tech_stack = set()
    for script in scripts:
        if 'php' in script:
            tech_stack.add('php')
        if 'jquery' in script:
            tech_stack.add('jQuery')
        if 'angular' in script:
            tech_stack.add('Angular')
        if 'react' in script:
            tech_stack.add('React')
        if 'vue' in script:
            tech_stack.add('Vue.js')
        if 'js' in script:
            tech_stack.add('Javascript')
        if 'aspnet' in script:
            tech_stack.add('ASP.NET MVC')
        if 'spring' in script:
            tech_stack.add('Spring MVC')
        if 'rails' in script:
            tech_stack.add('Ruby on Rails')
        if 'django' in script:
            tech_stack.add('Django')
        if 'laravel' in script:
            tech_stack.add('Laravel')
    # Detect CMS and add to tech stack
    cms = detect_cms(soup)
    if cms:
        tech_stack.add(cms)   
        
    return ', '.join(tech_stack)

# Function to extract payment gateways
def extract_payment_gateways(soup):
    html_content = soup.prettify().lower()
    payment_gateways = []

    # Known payment gateway identifiers
    payment_keywords = [
        'paypal', 'upi', 'net banking', 'stripe', 'razorpay', 'square', 'authorizenet', 'apple card',
        'braintree', 'payu', 'worldpay', 'skrill', 'payoneer', 'adyen', 'alipay', 'wechat pay', 'apple pay'
    ]

    # Check for keywords in the entire HTML content
    for keyword in payment_keywords:
        if keyword in html_content:
            payment_gateways.append(keyword.title())
        else:
            None

    return ', '.join(payment_gateways)

# Function to determine website language
def extract_website_language(soup):
    html_tag = soup.find('html')
    return html_tag.get('lang', 'en') if html_tag else 'en'

# Function to categorize the website
def extract_website_category(soup):
    # meta_description = ''
    try:
        meta_description = extract_meta_description(soup)
        body_text = soup.get_text().lower()

        # Check meta description first
        if meta_description :
            if 'payments' in meta_description:
                return 'payment_website'
            elif 'e-commerce' in meta_description or 'shopping' in meta_description:
                return 'E-commerce'
            elif 'blog' in meta_description or 'news' in meta_description:
                return 'Blog/News'
            elif 'portfolio' in meta_description or 'projects' in meta_description:
                return 'Portfolio'
            elif 'corporate' in meta_description or 'business' in meta_description:
                return 'Corporate'
            elif 'education' in meta_description or 'learning' in meta_description:
                return 'Educational'
            elif 'videos' in meta_description or 'friends' in meta_description:
                return 'socialmedia'
            elif 'entertainment' in meta_description or 'games' in meta_description:
                return 'Entertainment'
            
        body_text = soup.get_text().lower()
        if 'shopping cart' in body_text or 'add to cart' in body_text:
            return 'E-commerce'
            
        elif 'payments' in meta_description or 'banking' in meta_description:
            return 'payment_website'
            
        # elif 'blog post' in body_text or 'read more' in body_text:
        #     return 'Blog/News'
            
        elif 'portfolio' in body_text or 'projects' in body_text:
            return 'Portfolio'
        elif 'about us' in body_text or 'our team' in body_text:
            return 'Corporate'
        elif 'course' in body_text or 'learning' in body_text:
            return 'Educational'
        elif 'game' in body_text or 'movie' in body_text:
            return 'Entertainment'    
    except Exception as e:
        print(f"Error extracting meta : {e}")
    return 'other '
def save_to_database(url, data):
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        cursor = connection.cursor()

        # Insert data into database
        insert_query = """
            INSERT INTO SCRAPERDATA (url, social_media_links, tech_stack, meta_title, 
                                  meta_description, payment_gateways, language, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        website_data = (url, data.get('social_media_links', ''),
            data.get('tech_stack', ''),
            data.get('meta_title', ''),
            data.get('meta_description', ''),
            data.get('payment_gateways', ''),
            data.get('language', ''),
            data.get('category', ''))
        cursor.execute(insert_query, website_data)

        connection.commit()
        print(f"Data inserted for {url}")

    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")



def main():
    filename = "websites.csv"  # Adjust filename as per your actual file name
    processed_domains = set()
    total_processed = 0

    try:
        df = pd.read_csv(filename)
        urls = df['websitedomain'].tolist()[:100]  # Get top 100 websites doamin column

        for url in urls:
            if not url.startswith('http'):
                url = 'http://' + url

            html_content = fetch_website_content(url)
            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                meta_title = extract_meta_title(soup)
                meta_description = extract_meta_description(soup)
                social_media_links = extract_social_media_links(soup, processed_domains)
                tech_stack = extract_tech_stack(soup)
                payment_gateways = extract_payment_gateways(soup)
                language = extract_website_language(soup)
                category = extract_website_category(soup)

                data = {
                    'meta_title': meta_title,
                    'meta_description': meta_description,
                    'social_media_links': social_media_links,
                    'tech_stack': tech_stack,
                    'payment_gateways': payment_gateways,
                    'language': language,
                    'category': category
                }
                save_to_database(url, data)
                total_processed += 1  # count data inserted in database
    except Exception as e:
        print(f"Error processing domains from CSV: {e}")

    print(f"Total websites processed: {total_processed}")

# Main execution
if __name__ == "__main__":
    main()


