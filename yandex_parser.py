from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tqdm import tqdm
import csv
import time


with open('data/start_url.txt', 'r') as file:
    start_url = file.read()


def get_description(driver: webdriver.Chrome, url: str) -> list[str]:
    try:
        driver.get(url)
        driver.maximize_window()
        time.sleep(2)

        # get name
        name = driver.find_element(By.CLASS_NAME, value='card-title-view__title-link').text

        # get types of current establishment
        type_tags = driver.find_element(By.CLASS_NAME, value='business-card-title-view__categories'). \
            find_elements(By.TAG_NAME, value='a')
        types_ = [type_.text for type_ in type_tags]
        types_ = ', '.join(types_)

        # get address
        address = browser.find_element(By.CLASS_NAME, value='business-contacts-view__address-link').text

        # get phone
        browser.find_element(By.CLASS_NAME, value='card-phones-view__more').click()
        phone = browser.find_element(By.CLASS_NAME, value='card-phones-view__phone-number')
        phone = phone.text if phone else '-'

        # get site of organization
        site = browser.find_element(By.CLASS_NAME, value='business-urls-view__text')
        site = site.text if site else '-'

        return [name, types_, address, phone, site]

    except (NoSuchElementException, TimeoutException):
        return []


with webdriver.Chrome() as browser:
    browser.get(start_url)
    browser.maximize_window()
    time.sleep(2)

    elements = browser.find_elements(By.CLASS_NAME, value='search-snippet-view')
    print(f"Amount of object in starting: {len(elements)}")

    scroll = browser.find_element(By.XPATH,
                                  value='/html/body/div[1]/div[2]/div[7]/div[2]/div[1]/div[1]/div[1]/div/div[1]/iframe'
                                  )
    for _ in tqdm(range(400)):
        ActionChains(browser).move_to_element(scroll).scroll_by_amount(1, 500).perform()
        time.sleep(3)

    elements = browser.find_elements(By.CLASS_NAME, value='search-snippet-view')
    print(f"Amount of objects on finish: {len(elements)}")

    with open('data/second_part_url.txt', 'r') as file:
        second_part = file.read()

    urls = []
    for element in elements:
        url_ = element.find_element(By.TAG_NAME, value='a').get_attribute('href')
        urls.append(url_ + second_part)

    table = []
    print('Start of extraction of data from urls')
    for cur_url in tqdm(urls):
        descr = get_description(browser, cur_url)
        table.append(descr)

final_table = [x for x in table if len(x) > 0]
print(f'Final amount of records: {len(final_table)}')

headers = ['название', 'тип', 'адрес', 'телефон', 'сайт']
with open('data/contacts_from_yandex.csv', 'a', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(headers)
    writer.writerows(final_table)
    print('file is created')
