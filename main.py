from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


try:
    current = pd.read_csv('software_engineer_jobs_USA.csv')
    csv_count = len(current.index)
    print(csv_count)
    num_start = int((csv_count - 1000)/ 15  * 10) 
#232 software engineer - 232 - missing 268 - 150 = 105 
#496 software developer - 264 - missing 236 - 120 = 116 - 115 basically done 500
#772 - 275 after 90 : it's 500

except:
    num_start = 0

url=f"https://www.indeed.com/jobs?q=software+engineer&l=United+States&fromage=14&start={num_start}&pp=gQAPAAABiWyqjzYAAAACCoW-3gAsAQBhAmOspajrr0xDPWQVv-uNSSPjcd6PYbFxUP89ZV2B-ot-V3Ptb-sZcQAAAA&vjk=e235898114b00329"
# url = f"https://www.indeed.com/jobs?q=software+developer&l=United+States&radius=50&fromage=14&start={num_start}&pp=gQAPAAAAAAAAAAAAAAACCtXTVwAwAQAA8ytPVU8rmwV8-5Lh_dm72ptwo5l38DeOqquOlxkIE8hr5vJMhadpti9K4RmQAAA&vjk=aeb09a8b0fd09fc1"
# url = f"https://www.indeed.com/jobs?q=web+developer&l=United+States&radius=50&fromage=14&start={num_start}&pp=gQAPAAAAAAAAAAAAAAACCtXxlgApAQEBBnTG_2N-DGGWMrZzVEZruoUuDRmEeDHTNf_PyPDtN4xQ-oIbyCwAAA&vjk=4a948376a7b0d46e"
driver = webdriver.Chrome()
driver.get(url)

jobs_list = []
job_type_options = ["Full-time", "Contract", "Internship", "Part-Time","Temporary"]
key_technologies = [
    'Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby', 'Swift', 'Go', 'TypeScript', 'SQL', 'NoSQL',
    'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'Ruby on Rails', 'ASP.NET',
    'Spring', 'Express.js', 'REST API', 'GraphQL', 'JSON', 'XML', 'Git', 'Jenkins', 'Docker', 'AWS', 'Azure',
    'Google Cloud', 'Linux', 'Unix', 'Windows', 'MySQL', 'PostgreSQL', 'MongoDB', 'Firebase', 'OAuth',
    'Webpack', 'Bootstrap', 'Sass',  'Material-UI', 'Tailwind CSS', 'Next.js', 'Gatsby', 'Nuxt.js',
    'Laravel', 'CodeIgniter', 'Symfony', 'CakePHP', 'AngularJS', 'Ember.js', 'Backbone.js', 'Meteor.js',
    'Knockout.js', 'Handlebars.js', 'Lodash', 'Underscore.js', 'Materialize CSS', 'Bulma', 'Foundation',
    'Semantic UI', 'Web Components', 'JIRA', 'Bitbucket']

# job_count = int(driver.find_element(By.CSS_SELECTOR, '.jobsearch-JobCountAndSortPane-jobCount').text.split(" ")[0].replace(',',''))
# print(job_count)
# pages[4].click()
time.sleep(2)

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
        job_description_button = job.find_element(By.CSS_SELECTOR, ".resultContent a")
        job_description_button.click()
        time.sleep(3)
        job_description = driver.find_element(By.CSS_SELECTOR, '.jobsearch-jobDescriptionText').text.lower()
        technologies = [key_tech for key_tech in key_technologies if key_tech.lower() in job_description]

        job_info['job_title'] = job_title
        job_info['company_name'] = company_name
        job_info['company_location'] = company_location
        for meta in meta_data:
            if '$' in meta.text:
                job_info['salary'] = meta.text
            elif meta.text in job_type_options:
                job_info['employment_type'] = meta.text
        skills = [] 
        for tech in technologies:
            skills.append(tech)
        job_info['skills'] = skills
        jobs_list.append(job_info)
    click_next.click()
    time.sleep(4)




df = pd.DataFrame(jobs_list)
df.to_csv("software_engineer_jobs_USA.csv",index=False,mode='a',header='None')
print('COMPLETED!')
driver.quit()