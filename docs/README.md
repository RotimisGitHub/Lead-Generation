What My Program Does

I built this program to automate lead acquisition from Google Maps. It scrapes business data—such as name, address, phone number, website, rating, and reviews—for a given industry in a specific city. The idea is to streamline the process of gathering potential clients for outreach, whether for marketing, sales, or networking purposes.
Initially, I faced a limitation: Google Maps only displays up to 55 businesses per search. That meant I was missing out on many potential leads in larger cities. To get around this, I needed a way to divide cities into smaller sections and search within each one separately.

How I Overcame the 55-Business Limit with Google Maps API
To bypass this restriction, I used the Google Places API to get the geographical coordinates (latitude and longitude) of a city. Instead of searching the entire city at once, I divided it into quadrants by splitting the coordinates into smaller sections.
Here’s how I did it:
1. Get the city’s general coordinates using ‘findplacefromtext’ from Google Places API.
2. Calculate the grid system by dividing the city into smaller squares based on latitude and longitude.
3. Generate specific search URLs for Google Maps using the midpoints of these grid sections. Each section has its own Google Maps search URL, effectively bypassing the 55-business limit.
This approach allowed me to capture leads from an entire city instead of being capped at 55.

How I Used Object-Oriented Programming (OOP) and Scalability
I structured my code using OOP principles to make it more modular and scalable. Here are the key components:
* Lead Class → Stores business details like name, address, phone, website, rating, and reviews.
* GridCoordinates Class → Represents a section of the city with its corresponding Google Maps search URL.
* LeadAcquisition Class → Handles the main logic, including:
    * Retrieving city coordinates and dividing them into sections.
    * Scraping businesses from each quadrant.
    * Automating browser actions using Selenium.
This structure makes it easy to expand and maintain. If I need to modify how I collect leads or add new data points, I can update individual classes without breaking the entire system.

How Other Scripts Help Complete the Task
I rely on two additional modules (ScrapingFunctions and AutomationFunctions), which contain prewritten functions for:
* Extracting text, attributes, and links from HTML.
* Handling Selenium interactions, like clicking elements, scrolling, and managing browser sessions.
* Storing data in a structured format for further processing.
This modular approach helps keep my main script clean while allowing me to reuse functions across different projects.

What Works Well
Scalability → I can easily change the number of city divisions to control how many sections I scrape. Bypassing Search Limits → Using Google Maps API lets me scrape beyond the 55-business restriction. Automation Efficiency → Automating scrolling and element interaction ensures I collect all available leads.

What I Could Improve

Database Integration – Currently, I don’t store leads in a structured database. I should implement:
* SQLite or PostgreSQL to store and retrieve data more efficiently.
* A method to prevent duplicates and track scraped businesses.
 More Reliable Scrolling – The infinite scroll function could be improved by:
* Detecting when new elements are loaded before continuing.
* Implementing better error handling to prevent timeouts.

* Current Error: "ConnectionRefusedError: [Errno 61] Connection refused" is caused due to too many attempts of using selenium. I could use the vpnJumper in the future when I'm able to.
