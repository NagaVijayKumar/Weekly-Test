from selenium import webdriver 
import os
import webbrowser
import numpy as np
import time

user1=input("Enter Your Id:")
pass1=input("Enter Exam Pasword:")
num_wt=int(input("Number of Weekly_Test with results:"))
num_sub=int(input("Enter number of Subjects:"))

sms_url='http://intranet.rguktn.ac.in/SMS/'
logout_url='http://intranet.rguktn.ac.in/SMS/signout.php'
wt_url='http://intranet.rguktn.ac.in/SMS/results/wt.php'
profile_url='http://intranet.rguktn.ac.in/SMS/profile.php'


path_to_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
chrome_options = webdriver.ChromeOptions()      
chrome_options.add_argument('headless')       
chrome_options.add_argument('disable-gpu')      
chrome_options.add_argument('window-size=1200x600')  
chrome_options.add_argument("--log-level=3") 
prefs = {"profile.managed_default_content_settings.images":2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(path_to_desktop+'\\chromedriver.exe')
driver.get(sms_url)
try:
	username=driver.find_element_by_id("user1")
	password=driver.find_element_by_id("passwd1")
	username.send_keys(user1)
	password.send_keys(pass1)
	driver.find_element_by_class_name("btn").click()
	time.sleep(3)
	s=driver.get(wt_url)
	time.sleep(4)
	items=[]
	
	for i in range(1,num_wt+1):
		l=[]
		subjects=[]
		for j in range(2,num_sub+2):
			#/html/body/div/div/section[2]/div[1]/div/div/div[2]/table[1]/tbody/tr[2]/td[13]
			path=f"/html/body/div/div/section[2]/div[1]/div/div/div[2]/table[{i}]/tbody/tr[{j}]/td[13]"
			sub_path=f"/html/body/div/div/section[2]/div[1]/div/div/div[2]/table[1]/tbody/tr[{j}]/td[2]"
			sub=driver.find_element_by_xpath(sub_path).text
			subjects.append(sub)
			tb=driver.find_element_by_xpath(path).text
			tb=int(tb)
			items.append(tb)
		# data=tb.text.encode('utf-8').strip()
		# rows=tb.find_element_by_tag_name("tr")
			#print(tb)
		#matrix.append(l)
		#print(f"{l}\n")
	matrix=np.array(items).reshape(num_wt,num_sub)
	print(f"weekly Test Marks\nRows are subjects and Columns are Weekly Tests\n{matrix}\n")
	matrix=np.transpose(matrix)
	matrix=np.sort(matrix,axis=1)
	#print(matrix)
	if(num_wt>5):
		matrix=np.delete(matrix,np.s_[0:num_wt-5],axis=1)
	print(f"Best of Five in All Subjects\n{matrix}\n")
	means=np.mean(matrix,axis=1)
	#print(means)
	#print(subjects)
	print("Final Average Marks\n\n")
	for i in range(0,num_sub):
		print(f"{subjects[i]}\t\t:{means[i]}\n")
	#/html/body/div/div/section[2]/div[1]/div/div/div[2]/table[1]/tbody/tr[2]/td[2]

except AssertionError as e:
	print ("please check details and enter the weekly tests you attended")


