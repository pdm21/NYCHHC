import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Base URL for the pages
BASE_URL = "https://www.nychealthandhospitals.org/doctors/page/{}/?specialty=80"

# Total number of pages (update this if needed)
TOTAL_PAGES = 175

# Keyword to search for
KEYWORD = "forensic"

# List to store the names of doctors
forensic_doctors = []

# Path to ChromeDriver
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"


# Initialize Selenium WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

for page in range(1, TOTAL_PAGES + 1):
    print(f"Processing page {page}...")
    # Construct the URL for the current page
    url = BASE_URL.format(page)

    try:
        # Use Selenium to load the page
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        # Find all doctor info containers
        doctor_info = soup.find_all("div", class_="doctor-info")

        if not doctor_info:
            print("No doctor information found on this page.")
        
        for doctor in doctor_info:
            # Extract the name of the doctor
            name_tag = doctor.find("h3")
            name = name_tag.get_text(strip=True) if name_tag else "Unknown"
            
            # Extract the specialty
            specialty_tag = doctor.find("div", class_="doctor-specialty")
            specialty = specialty_tag.find("p").get_text(strip=True) if specialty_tag else ""

            # Print the content being searched for forensic
            print(f"Specialty content: {specialty}")
            
            # Check if the keyword is in the specialty (case-insensitive)
            if KEYWORD.lower() in specialty.lower():
                forensic_doctors.append(name)

    except Exception as e:
        print(f"Failed to process page {page}: {e}")

# Quit the WebDriver
driver.quit()

# Print the results
print("\nDoctors with 'forensic' in their specialty:")
for doctor in forensic_doctors:
    print(doctor)

print(f"\nTotal doctors found: {len(forensic_doctors)}")
