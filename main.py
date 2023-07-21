from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd



current = pd.read_csv('software_engineer_jobs_USA.csv')
csv_count = len(current.index)
# num_times_to_run = int(csv_count / 15)
num_start = int(csv_count / 15  * 10)
url=f"https://www.indeed.com/jobs?q=software+engineer&l=United+States&fromage=14&start=10&pp=gQAPAAABiWyqjzYAAAACCoW-3gAsAQBhAmOspajrr0xDPWQVv-uNSSPjcd6PYbFxUP89ZV2B-ot-V3Ptb-sZcQAAAA&vjk=e235898114b00329"
driver = webdriver.Chrome()
driver.get(url)

jobs_list = []
job_type_options = ["Full-time", "Contract", "Internship", "Part-Time","Temporary"]
# job_count = int(driver.find_element(By.CSS_SELECTOR, '.jobsearch-JobCountAndSortPane-jobCount').text.split(" ")[0].replace(',',''))
# print(job_count)
# pages[4].click()

while len(jobs_list) < 105:
    jobs = driver.find_elements(By.CSS_SELECTOR, '.resultContent')
    # pages = driver.find_elements(By.CSS_SELECTOR, ".css-tvvxwd")
    click_next = driver.find_element(By.CSS_SELECTOR, "[aria-label='Next Page']")
    for job in jobs:
        job_info = {}
        job_title = job.find_element(By.CSS_SELECTOR, ".jobTitle").text
        company_name = job.find_element(By.CSS_SELECTOR, ".companyInfo .companyName").text
        company_location = job.find_element(By.CSS_SELECTOR, ".companyInfo .companyLocation").text
        meta_data = job.find_elements(By.CSS_SELECTOR, ".metadata .attribute_snippet")
        job_info['job_title'] = job_title
        job_info['company_name'] = company_name
        job_info['company_location'] = company_location
        meta_info = []
        for meta in meta_data:
            if '$' in meta.text:
                job_info['salary'] = meta.text
            elif meta.text in job_type_options:
                job_info['employment_type'] = meta.text
        jobs_list.append(job_info)
    click_next.click()
    # pages[5].click()
    time.sleep(3)


df = pd.DataFrame(jobs_list)
df.to_csv("software_engineer_jobs_USA.csv",index=False,mode='a',header='None')
print('COMPLETED!')
driver.quit()