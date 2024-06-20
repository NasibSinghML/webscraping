#Approach

Fetching Website Content: Used the requests library to fetch the HTML content of each website.

Parsing HTML: Used BeautifulSoup to parse the HTML and extract various elements.

Meta Information Extraction: Extracted meta titles and descriptions from the HTML <title> and <meta> tags.

Social Media Links Extraction: Identified and extracted social media links while ignoring certain patterns 
using regex.

Technology Stack Detection: Checked for the presence of specific JavaScript libraries and CMS indicators.

Payment Gateways Detection: Searched for mentions of known payment gateways in the website content.

Language Detection: Extracted the language attribute from the <html> tag.

Website Categorization: Used keyword matching in the meta description and body text to categorize the website.

Database Storage: Used mysql-connector-python to insert the extracted data into a MySQL database.

#Challenges

Variety of Link Formats: Social media links can appear in various formats, such as full URLs (https://www.instagram.com/username), relative URLs (/username), or even encoded URLs (/redirect?url=https%3A%2F%2Fwww.instagram.com%2Fusername). Handling these different formats robustly requires preprocessing and sometimes decoding of URLs.

Detection and Avoidance of Non-Social Links: Not all URLs containing social media domain names are direct links to social media profiles. Some may be internal links, redirects, or other unrelated content. It’s crucial to filter out such links to ensure only relevant social media profiles are extracted.

Handling Different URL Formats: Ensuring URLs are properly formatted before processing.
Regex Complexity: Crafting regex patterns to accurately identify and ignore specific social media links.


Dynamic Content: Some websites rely heavily on JavaScript to render content, which was not fetched by the requests library.

Data Consistency: Ensuring the extracted data is consistent and correctly formatted before insertion into the database.

Retrieving Social Links from the Same URL: Encountered difficulties in retrieving social media links when multiple links from the same social media platform were present on the same URL. This required handling duplicate detection and ensuring only unique links were stored.

Matching Words: Encountered errors in matching words for categories and technologies due to variations in wording and context.
