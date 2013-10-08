from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait 
from xml.dom import minidom
import time, os, string, requests, re, sys

site_domain = "http://yoursite.com/"
xml_file_name = "sitemap.xml"
browser = "phantomjs" # options: phantomjs, firefox, chrome, ie

def _slugify(text, delim=u'-'):
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    result = []
    for word in _punct_re.split(text.lower()):
        if word:
            result.append(word)
    return "-".join(result)
 
class SiteCapture:
	driver = ""
	save_folder = ""
	domain = ""
	site_map = ""

	def __init__(self, driver, domain, site_map, save_folder):
		self.driver = driver
		if (driver == "phantomjs"):
			try:
				self.driver = webdriver.PhantomJS('phantomjs')
			except:
				print("Could not load a driver")
				sys.exit()
		elif (driver == "chrome"):
			try:
				self.driver = webdriver.Chrome('drivers/chromedriver')
			except:
				print("Could not load a driver")
				sys.exit()
		elif (driver == "firefox"):
			self.driver = webdriver.Firefox()
		elif (driver == "ie"):
			self.driver = webdriver.Ie('drivers/iedriver')

		self.domain = domain
		self.site_map = site_map
		self.save_folder = save_folder

	def take_screenshot(self, page_url):
		path = os.path.abspath(self.save_folder)
		if not os.path.exists(path):
			os.makedirs(path)
		file_name = _slugify(page_url.replace(self.domain, "").replace(":", ""))
		if (file_name == ""):
			file_name = "home"
		full_path = path + "\\" + file_name + ".png"
		print("Saving " + page_url + " as " + full_path)
		self.driver.get_screenshot_as_file(full_path)
		return full_path

	def run(self):
		xml = requests.get(self.domain + self.site_map)
		xmldoc = minidom.parseString(xml.content)
		itemlist = xmldoc.getElementsByTagName('url')
		print (len(itemlist))
		for item in itemlist:
			page_url = (item.getElementsByTagName('loc')[0].firstChild.data)
			page_url = page_url.replace("http://www.marianist.com/", site_domain) # REMOVE THIS!!!
			try:
				self.driver.get(page_url)
				self.take_screenshot(page_url)
			except:
				print("Could not load " + page_url)


capture = SiteCapture(browser, site_domain, xml_file_name, "screenshots/")
capture.run()