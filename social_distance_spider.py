from bs4 import BeautifulSoup
import requests
import math

class SocialDistanceSpider:
  def __init__(self, url):
    self.url = url

  def parseCategories(self):
    '''
    This gets all of the different locations from the social distance website,
    organized by category.
    rtype: [{str, [{str}]}]
    '''
    response = requests.get(self.url)
    data = response.text
    soup = BeautifulSoup(data, "lxml")

    # get container links header and links
    categoriesContainer = soup.find("div", {"class": "facetchecks"})

    # store each link and name of each category in lists
    categories = []
    for linkTag in categoriesContainer.find_all("a"):
      linkName = linkTag.get_text().strip()

      # separate name and number of locations
      name = ""
      numberOfLocations = ""
      # start with last digit of number
      i = len(linkName) - 2
      reachedParan = False
      while i >= 0:
        if reachedParan:
          name = linkName[i] + name
        elif linkName[i] == "(":
          reachedParan = True
        else:
          numberOfLocations = linkName[i] + numberOfLocations
        i -= 1

      categories.append({
        "link": linkTag.get("href").strip(),
        "name": name.strip(),
        "number": numberOfLocations.strip()
      })

    # go through each category and scrape data
    for category in categories:
      link = self.url + category["link"]

      # get max page number for category
      maxPageNumber = math.ceil(int(category["number"]) / 20.0)

      pageLinks = [link]
      linkParts = link.split("Facet?", 1)
      if len(linkParts) == 2:
        for i in range(1, maxPageNumber):
          newLink = linkParts[0] + "Page?paging=" + str(i) + "&" + linkParts[1]
          pageLinks.append(newLink)
      else:
        print("URL page error")

      locations = []
      for pageLink in pageLinks:
        locations += self.parseLocations(pageLinks[0], pageLink)

      # print(locations)

      # group scraped data with its respective category
      category["locations"] = locations

    return categories

  def parseLocations(self, primaryLink, link):
    '''
    This gets the locations on one page of the website.
    type link: str
    rtype: [{str}]
    '''
    session = requests.Session()
    response = session.get(primaryLink)
    response = session.get(link)
    data = response.text
    soup = BeautifulSoup(data, "lxml")

    # get container for location data
    locationsContainer = soup.find("div", {"class": "item-container"})

    locations = []

    for locationTag in locationsContainer.find_all("div", {"class": "normal-text list-item"}):
      # location will store location name, phone number, and address
      location = {}

      locationNameTags = locationTag.find_all("div", {"class": "text-left font-weight-bold"})

      # add location names to locations object
      # some locations have two lines
      locationNames = []
      for locationNameTag in locationNameTags:
        locationNames.append(locationNameTag.get_text().strip())
        
      location["names"] = locationNames

      locationDataTags = locationTag.find("div", {"class": "text-left main-info"}).findChild()

      # divNum keeps track of iteration of for loop, to put data in location
      divNum = 0
      for locationDataDiv in locationDataTags.find_all("div"):
        # if this is the phone number
        if divNum == 0:
          location["phone"] = locationDataDiv.get_text().strip()
        # if this is the first line in the address
        elif divNum == 1:
          location["address1"] = locationDataDiv.get_text().strip()
        # if this is the second line in the address
        elif divNum == 2:
          location["address2"] = locationDataDiv.get_text().strip()

        divNum += 1

      # store location in list locations
      locations.append(location)
      
    return locations