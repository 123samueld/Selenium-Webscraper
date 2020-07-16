### Webscraper for Hostelworld.com ###

#Modules
import os
import os.path
import datetime
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#Chrome webdriver
driver = webdriver.Chrome("C:\webdrivers\chromedriver.exe")

#Create folder for the data
os.chdir('Downloads')
today = datetime.datetime.now().date()
folder = today.strftime('%d'+ '.'+ '%m'+ '.'+'%Y')
os.mkdir(folder)


def scraper():
	today = datetime.datetime.now().date()
	date1int = today + datetime.timedelta(days=1)
	date2int = today + datetime.timedelta(days=2)

	date1 = date1int.strftime('%Y-%m-%d')
	date2 = date2int.strftime('%Y-%m-%d')

	mid = "&to="
    
    #Hong Kong
	hongkong1 = "https://www.hostelworld.com/s?q=Hong%20Kong,%20Hong%20Kong%20China&country=Hong%20Kong%20China&city=Hong%20Kong&type=city&id=6562&from="
	hongkong2 = "&guests=1&page=1"
	hongkong = (hongkong1 + date1 + mid + date2 + hongkong2)
    
    #London
	london1 = "https://www.hostelworld.com/s?q=London,%20England&country=England&city=London&type=city&id=3&from="
	london2 = "&guests=1&page=1"
	london = (london1 + date1 + mid + date2 + london2)
    
    #New York
	newyork1 = "https://www.hostelworld.com/s?q=New%20York,%20New%20York,%20USA&country=USA&city=New%20York&type=city&id=13&from=2020-05-04&to="
	newyork2 = "&guests=1&page=1"
	newyork = (newyork1 + date1 + mid + date2 + newyork2)
    
    #Paris
	paris1 = "https://www.hostelworld.com/s?q=Paris,%20Ile-de-France,%20France&country=France&city=Paris&type=city&id=14&from="
	paris2 = "&guests=1&page=1"
	paris = (paris1 + date1 + mid + date2 + paris2)
    
    #Sydney
	sydney1 = "https://www.hostelworld.com/s?q=Sydney,%20New%20South%20Wales,%20Australia&country=Australia&city=Sydney&type=city&id=81&from="
	sydney2 = "&guests=1&page=1"
	sydney = (sydney1 + date1 + mid + date2 + sydney2)
    
    #Tokyo
	tokyo1 = "https://www.hostelworld.com/s?q=Tokyo,%20Japan&country=Japan&city=Tokyo&type=city&id=452&from="
	tokyo2 = "&guests=1&page=1"
	tokyo = (tokyo1 + date1 + mid + date2 + tokyo2)
    
    

	cities = [hongkong, london, newyork, paris, sydney, tokyo]
    
    #Names of cities to name files with
	cityNameDict = {1: 'Hong Kong', 2: 'London', 3: 'New York', 4: 'Paris', 5: 'Sydney', 6: 'Tokyo'};
    #Counter for city naming dictionary
	counter = 0

    
	for city in cities:
		startUrl = city
        
        #Counting through city names
		counter = counter + 1
        
        #Set which URL to scrape
		driver.get(startUrl)
        
        #Scroll to the bottom of the page
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        
        #Check if the city has more than 1 page worth of hostel data
		try:
            
            #If more than one page of hostels proccess them
			driver.find_element_by_css_selector("#__layout > div > div.search > div.page-inner > div > div > div.pagination.pagination > div.pagination-item.pagination-last")
            
            #Click to go to the end of the page list
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#__layout > div > div.search > div.page-inner > div > div > div.pagination.pagination > div.pagination-item.pagination-last"))).click()
			time.sleep(10)
            
            #Get the number of the last page and convert to a string
			maxPagesLink = driver.find_element_by_css_selector("#__layout > div > div.search > div.page-inner > div > div > div.pagination.pagination > div.pagination-item.pagination-current").text
			maxPagesInt = int(maxPagesLink) + 1
			maxPages = str(maxPagesInt)
        
            #Prepare the url to get updating page numbers
			preUrl = startUrl[:-1]
            
            #Prepare a blank list to collect the data
			pageData = []
        
            #Loop through pages the number of times per max number of pages
			for page in range(1, maxPagesInt):

        
                #Combine prepared URL with the page number the loop is currently on
				url = preUrl + str(page)
				time.sleep(random.randint(0,5))
				driver.get(url)
        
                #Find each property card
				cards=WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.property-card")))
        
                #Loop through each property card
				for card in cards:
        
                    #Loop through each data item on the property card
					try:
        
                        #Find the data item
						title = card.find_element_by_css_selector("h2.title.title-6>a").text
        
                        #Append the data to the list
						pageData.append(title)
                                       
                        #Collect prices
						allPrices = card.find_elements_by_class_name("price-col")
						for prices in allPrices:
							pageData.append(prices.text)
					except:
                        #Pass on to the next part of the program once all data items have been collected 
						continue
        
            
            #Save the file to the folder
			savePath = 'C:/Users/lenovo/Downloads/' + folder 
			cityName = str(cityNameDict.get(counter))
			completeName = os.path.join(savePath, cityName+".txt")  
			cityFile = open(completeName, "w")       
			toFile = str(pageData)
			cityFile.write(toFile)
			cityFile.close()

        #If the city has only one page    
		except NoSuchElementException:
        
            #Go to it's page
			url = startUrl
			time.sleep(random.randint(0,5))
			driver.get(url)
            
            #Prepare a blank list to collect the data
			pageData = []
     
            #Find each property card
			cards=WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.property-card")))
        
            #Loop through each property card
			for card in cards:
        
                #Loop through each data item on the property card
				try:
                    #Collect hostel names
					title = card.find_element_by_css_selector("h2.title.title-6>a").text
					pageData.append(title)
                    
                    #Collect prices
					allPrices = card.find_elements_by_class_name("price-col")
					for prices in allPrices:
						pageData.append(prices.text)
                                           
				except:
                        #Pass on to the next part of the program once all data items have been collected 
					continue

			#Save the file to the folder
			savePath = 'C:/Users/lenovo/Downloads/' + folder 
			cityName = str(cityNameDict.get(counter))
			completeName = os.path.join(savePath, cityName+".txt")  
			cityFile = open(completeName, "w")       
			toFile = str(pageData)
			cityFile.write(toFile)
			cityFile.close()


scraper()