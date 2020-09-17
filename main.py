from social_distance_spider import SocialDistanceSpider
from write_data_to_file import WriteDataToFile

spider = SocialDistanceSpider("https://sdp.sccgov.org")
categories = spider.parseCategories()

writer = WriteDataToFile(categories)
writer.writeToFile()