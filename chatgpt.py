from selenium import webdriver
import time
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import json
import nltk
from nltk.tokenize import sent_tokenize
import random
num = 0
all_items = []

def count_words(text_list):
    total_words = 0
    for text in text_list:
        words = text.split()
        total_words += len(words)
    return total_words

def type_like_a_person(element, text):
    for char in text:
        time.sleep(random.uniform(0.01, 0.05))  # Задержка между символами
        element.send_keys(char)
        
json_folder = 'json_data'
combined_json_file = 'output.json'
combined_json_path = os.path.join(json_folder, combined_json_file)

# Read data from the combined JSON file
with open(combined_json_path, "r", encoding="utf-8") as combined_json_file:
    all_items = json.load(combined_json_file)

selected_items = random.sample(all_items, 20) # Ограничение в 20 сообщений в день

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')


driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': """
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
    """
})
driver.get('https://chat.openai.com/')
time.sleep(10)
driver.execute_script("window.open('')")
driver.switch_to.window(driver.window_handles[1])
driver.get('https://cryptotalk.org/topic/358811-блокировка-диапазона-ip-адресов/?tab=comments#comment-16227988')
driver.delete_all_cookies()

cookies_path_ctt = 'cryptotalk.dat'
with open(cookies_path_ctt, 'rb') as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            pass

driver.switch_to.window(driver.window_handles[0])

cookies_path = 'my_cookies_chat_gpt.dat'
with open(cookies_path, 'rb') as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            pass

driver.get('https://chat.openai.com/')
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="prompt-textarea"]')))
text_input = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')

for item in selected_items:
    text = item['Text']
    link = item['Href']
    print(text)
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//*[@id="prompt-textarea"]')))
    text_input = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
    text_input.send_keys(f'напиши свое мнение об "{text}". Ты эксперт в этой теме, пиши на русском, и соблюдай субординацию, не используй матерные слова минимум  100 слов обязательно')
    text_input.send_keys(Keys.RETURN)
    time.sleep(30)  # Увеличьте эту задержку по необходимости
    # Ждем, пока новый тег <p> станет видимым на странице (ожидание не более 10 секунд)  # Добавим дополнительную задержку перед поиском элемента <p>
    chat_elements = driver.find_elements(By.XPATH, '//div[@data-message-author-role="assistant"]')
    # Проверка наличия новых элементов <p>
    if chat_elements:
        latest_chat_element = chat_elements[-1]
        # Получаем data-message-id из атрибута
        latest_message_id = latest_chat_element.get_attribute("data-message-id")
        # Находим тег <p> внутри последнего чата
        p_elements = latest_chat_element.find_elements(By.XPATH, './/p')
        info_list = []
        for p_element in p_elements:
            info_list.append(p_element.text)
        
    special_sentences = ['К сожалению,', 'последнего обновления', 'январе 2022 года']  # Замените этот список на свой

# Привести предложения для поиска к нижнему регистру
    special_sentences_lower = [sentence.lower() for sentence in special_sentences]

# Привести предложения в info_list к нижнему регистру
    info_list_lower = [sentence.lower() for sentence in info_list]

    # Добавить вывод для отладки
    print("special_sentences_lower:", special_sentences_lower)
    print("info_list_lower:", info_list_lower)

    if any(sentence in ' '.join(info_list_lower) for sentence in special_sentences_lower):
        selected_items += random.sample(all_items, 1)
        time.sleep(10)
        continue
    else:
        print('прошли дальше')

    words_count = count_words(info_list)
    if words_count < 100:
        print('слов меньше 100')
        WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//*[@id="prompt-textarea"]')))
        text_input = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        text_input.send_keys(f'добавь пару предложений')
        text_input.send_keys(Keys.RETURN)
        time.sleep(30)
        chat_elements = driver.find_elements(By.XPATH, '//div[@data-message-author-role="assistant"]')
    # Проверка наличия новых элементов <p>
        if chat_elements:
            latest_chat_element = chat_elements[-1]
            # Получаем data-message-id из атрибута
            latest_message_id = latest_chat_element.get_attribute("data-message-id")
            # Находим тег <p> внутри последнего чата
            p_elements = latest_chat_element.find_elements(By.XPATH, './/p')
            for p_element in p_elements:
                info_list.append(p_element.text)

    driver.switch_to.window(driver.window_handles[1])
    driver.get(link)
    while True:
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[2]/ul/li[1]/span/a")))
        except TimeoutException:
            driver.get(link)
            time.sleep(5)
            continue
        button_input = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[2]/ul/li[1]/span/a")
        button_input.click()
        time.sleep(5)
       
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[3]/div[5]/form/div/div[2]/div/div[1]/div[1]/div/div/div/div')))
            text_input = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[3]/div[5]/form/div/div[2]/div/div[1]/div[1]/div/div/div/div')
        except TimeoutException:
            try:
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[3]/div[3]/form/div/div[2]/div/div[1]/div[1]/div/div/div/div')))
                text_input = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[3]/div[3]/form/div/div[2]/div/div[1]/div[1]/div/div/div/div')
            except TimeoutException:
                print('сработала эта строка')
                driver.get(link)
                time.sleep(5)
                continue

        text_input.click()
        for i in info_list:
            type_like_a_person(text_input, str(i))
        time.sleep(5)
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[3]/div[5]/form/div/div[2]/ul/li[2]/button')))
            button_click_last = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[3]/div[5]/form/div/div[2]/ul/li[2]/button')
        except TimeoutException:
            try:
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[3]/div[3]/form/div/div[2]/ul/li[2]/button')))
                button_click_last = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[3]/div[3]/form/div/div[2]/ul/li[2]/button')
            except TimeoutException:
                driver.get(link)
                time.sleep(5)
                continue
        
        button_click_last.click()
        num += 1
        print(f"Сообщение {num} написали")
        time.sleep(5)
        link_present = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[3]/div[3]/form/article[last()]/div[2]/div/div[1]/div[1]/ul/li[2]/a/i'))
    )

        # Click on the link
        link_share = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div/div[2]/div/div[1]/div[3]/div[3]/form/article[last()]/div[2]/div/div[1]/div[1]/ul/li[2]/a/i')
        link_share.click()

        # Wait for the input element to be present
        link_value = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="text"]'))
    )

    # Get the value attribute
        link_copy = link_value.get_attribute("value")
        result_data = {'LinkCopy': link_copy}

        with open('links.json', 'w', encoding='utf-8') as json_result_file:
            json.dump(result_data, json_result_file, ensure_ascii=False, indent=2)

        time.sleep(5)
        driver.switch_to.window(driver.window_handles[0])
        # Remove processed item from the combined JSON file
        all_items = [i for i in all_items if i != {'Text': text, 'Href': link}]

        # Save the updated list to the combined JSON file
        with open(combined_json_path, 'w', encoding='utf-8') as combined_json_file:
            json.dump(all_items, combined_json_file, ensure_ascii=False, indent=2)
        time.sleep(100)
        break
        
        # Optionally, y

print("Код отработал успешно!")
    # print(f"Text: {text}")
    # print(f"Link: {link}")
    # print("=" * 50)


# cookies_path = 'my_cookies_chat_gpt.dat'
# cookies = driver.get_cookies()

# with open(cookies_path, 'wb') as f:
#     pickle.dump(cookies, f)
