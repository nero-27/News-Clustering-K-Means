import unittest
from selenium import webdriver
import time


class Testing(unittest.TestCase):

	

	@classmethod
	def setUpClass(cls):
		cls.driver = webdriver.Chrome('E:\Selenium\chromedriver.exe')
		cls.driver.implicitly_wait(10)
		cls.driver.maximize_window()


	#Test Case 1
	def test_open_index(self):
		self.driver.get(' http://127.0.0.1:5000/')
		self.assertTrue(self.driver.title == "Main Page")
		print("Index page loaded succesfully")

	time.sleep(2)

	#Test Case 2
	def test_upload_file(self):
		self.driver.get(' http://127.0.0.1:5000/')
		self.driver.find_element_by_xpath('/html/body/div/div/form/input[1]').send_keys(r'D:\FINAL MINI PROJECT\data.txt')
		existance = self.driver.find_element_by_name('file')
		self.assertTrue(existance)
		print("File uoloaded succesfully")

	time.sleep(2)

	#Test Case 3
	def test_display_clusters(self):
		self.driver.get(' http://127.0.0.1:5000/')
		self.driver.find_element_by_xpath('/html/body/div/div/form/input[1]').send_keys(r'D:\FINAL MINI PROJECT\data.txt')
		self.driver.find_element_by_xpath('/html/body/div/div/form/input[2]').click()
		time.sleep(2)
		self.assertTrue(self.driver.title == "Cluster Table")
		print("Clusters displayed succesfully")

	time.sleep(2)

	#Test Case 4
	def test_plot_clusters(self):
		self.driver.get(' http://127.0.0.1:5000/')
		self.driver.find_element_by_xpath('/html/body/div/div/form/input[1]').send_keys(r'D:\FINAL MINI PROJECT\data.txt')
		self.driver.find_element_by_xpath('/html/body/div/div/form/input[2]').click()
		time.sleep(2)
		self.driver.find_element_by_name('show_clusters').click()
		time.sleep(2)
		self.assertTrue(self.driver.title == "Clusters")
		print("Clusters displayed succesfully")

	time.sleep(2)

	#Test Case 5
	def test_return_home(self):
		self.driver.get(' http://127.0.0.1:5000/')
		self.driver.find_element_by_xpath('/html/body/div/div/form/input[1]').send_keys(r'D:\FINAL MINI PROJECT\data.txt')
		self.driver.find_element_by_xpath('/html/body/div/div/form/input[2]').click()
		time.sleep(2)
		self.driver.find_element_by_name('show_clusters').click()
		time.sleep(2)
		self.driver.find_element_by_name('Home').click()
		time.sleep(2)
		self.assertTrue(self.driver.title == "Main Page")
		print("Clusters displayed succesfully")

	@classmethod
	def tearDownClass(cls):
		cls.driver.close()
		cls.driver.quit()
		print("Tests Completed")
	# def test_index_open(self):
	# 	self.driver.get('http://127.0.0.1:5000/')
	# 	self.title_of_page = driver.title 
	# 	self.assertTrue(title_of_page == "Main Page")
	# 	print("Test Passed")

	
if __name__=="__main__":
    unittest.main()