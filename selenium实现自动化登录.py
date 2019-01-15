# coding:utf-8
# author:YJ沛

from selenium import webdriver
import time
import os


ulr="https://pan.baidu.com/disk/home?#/all?path=%2F&vmode=list"

driver = webdriver.Chrome()
driver.get(ulr)
driver.implicitly_wait(5)
driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__footerULoginBtn"]').click()
driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__userName"]').send_keys('455758882')
driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__password"]').send_keys('5691772123')


driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__submit"]').click()

time.sleep(20)



os.chdir('D:\BaiduNetdiskDownload')
print(os.getcwd())
print(os.listdir(os.getcwd()))
file_list = os.listdir(os.getcwd())

for file in file_list:
    # 上传文件
    print("点击上传按钮")
    driver.find_element_by_xpath('//*[@id="h5Input0"]').click()

    print("上传文件")
    time.sleep(3)
    # driver.find_element_by_xpath('//*[@id="h5Input1"]').click()
    driver.find_element_by_name('html5uploader').send_keys('D:\BaiduNetdiskDownload\\'+file)
    print('D:\BaiduNetdiskDownload\\'+file)



driver.quit()
