# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# import requests
# import tempfile
# import os
# import pdfplumber

# def check_states_in_pdf(pdf_url, target_states):
#     try:
#         if not pdf_url or "javascript" in pdf_url.lower() or pdf_url == "N/A":
#             return False
            
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
#         }
        
#         response = requests.get(pdf_url, headers=headers, timeout=15)
        
#         # Ensure it's a PDF
#         if response.status_code == 200 and b"%PDF" in response.content[:10]:
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#                 tmp_file.write(response.content)
#                 tmp_file_path = tmp_file.name
                
#             match_found = False
#             try:
#                 with pdfplumber.open(tmp_file_path) as pdf:
#                     for page in pdf.pages:
#                         text = page.extract_text()
#                         if text:
#                             text_upper = text.upper()
#                             for state in target_states:
#                                 if state in text_upper:
#                                     match_found = True
#                                     break
#                         if match_found:
#                             break
#             finally:
#                 if os.path.exists(tmp_file_path):
#                     try:
#                         os.remove(tmp_file_path)
#                     except:
#                         pass
#             return match_found
            
#     except Exception as e:
#         print(f"Error reading PDF {pdf_url}: {e}")
        
#     return False

# def start_gem_scraping(category_text, states_text):
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--window-size=1920,1080")
#     # Disable images to speed up page loads
#     prefs = {"profile.managed_default_content_settings.images": 2}
#     options.add_experimental_option("prefs", prefs)
#     # Use eager loading so DOM becomes available earlier
#     options.page_load_strategy = 'eager'

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     wait = WebDriverWait(driver, 15)
#     all_final_results = []
    
#     try:
#         driver.get("https://bidplus.gem.gov.in/advance-search")

#         # 1. CATEGORY SELECTION
#         wait.until(EC.element_to_be_clickable((By.ID, 'select2-categorybid-container'))).click()
#         search_input = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input')))
#         search_input.send_keys(category_text)
#         time.sleep(0.8)
#         search_input.send_keys(Keys.ENTER)

#         # 2. STATES SELECTION
#         if states_text:
#             selected_states = [s.strip() for s in states_text.split(',') if s.strip()]
#             for state in selected_states:
#                 try:
#                     state_container = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="adv-search"]/div[2]/div[2]/div/span/span[1]/span')))
#                     state_container.click()
#                     state_input = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input')))
#                     state_input.send_keys(state)
#                     time.sleep(0.6)
#                     state_input.send_keys(Keys.ENTER)
#                 except: continue

#         # 3. SEARCH EXECUTION
#         search_btn = wait.until(EC.element_to_be_clickable((By.ID, "searchByBid")))
#         driver.execute_script("arguments[0].click();", search_btn)
        
#         # 4. PAGINATION LOOP (Saare pages ke liye)
#         page_count = 1
#         while True:
#             try:
#                 # Wait for cards to load
#                 wait.until(EC.presence_of_element_located((By.ID, "bidCard")))
#                 time.sleep(1)
#             except:
#                 break 

#             card_found_on_page = False
#             # div[2] se div[12] tak cards check karna
#             for card_index in range(2, 13): 
#                 card_xpath = f'//*[@id="bidCard"]/div[{card_index}]'
#                 try:
#                     cards = driver.find_elements(By.XPATH, card_xpath)
#                     if not cards: continue
                    
#                     card = cards[0]
#                     if "BID NO:" in card.text.upper():
#                         card_found_on_page = True
#                         lines = card.text.split('\n')
#                         items, dept, sd, ed = "N/A", "N/A", "N/A", "N/A"
                        
#                         for i, line in enumerate(lines):
#                             l = line.upper()
#                             if "ITEMS:" in l: items = line.split(':', 1)[-1].strip()
#                             elif "DEPARTMENT NAME AND ADDRESS:" in l:
#                                 dept = line.split(':', 1)[-1].strip()
#                                 if not dept and i+1 < len(lines): dept = lines[i+1].strip()
#                             elif "START DATE:" in l: sd = line.split(':', 1)[-1].strip()
#                             elif "END DATE:" in l: ed = line.split(':', 1)[-1].strip()

#                         link_elem = card.find_element(By.TAG_NAME, "a")
#                         bid_no = link_elem.text.strip()
#                         bid_link = link_elem.get_attribute("href")

#                         # Check for duplicates before adding
#                         if not any(res['bid_no'] == bid_no for res in all_final_results):
#                             all_final_results.append({
#                                 "category": category_text,
#                                 "bid_no": bid_no,
#                                 "items": items,
#                                 "department": dept,
#                                 "start_date": sd,
#                                 "end_date": ed,
#                                 "link": bid_link
#                             })
#                 except: continue

#                 # --- NEXT PAGE LOGIC ---
#             try:
#                 next_button = driver.find_elements(By.XPATH, "//a[contains(text(), 'Next')] | //a[contains(text(), '»')]")
#                 if next_button and card_found_on_page:
#                     driver.execute_script("arguments[0].scrollIntoView();", next_button[0])
#                     time.sleep(0.6)
#                     driver.execute_script("arguments[0].click();", next_button[0])
#                     page_count += 1
#                     time.sleep(1)
#                 else:
#                     break
#             except:
#                 break

#     except Exception as e:
#         print(f"Scraper Error: {e}")
#     finally:
#         driver.quit()
    
#     return all_final_results


import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import requests
import tempfile
import os
import pdfplumber

def check_states_in_pdf(pdf_url, target_states):
    try:
        if not pdf_url or "javascript" in pdf_url.lower() or pdf_url == "N/A":
            return False
            
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(pdf_url, headers=headers, timeout=15)
        
        if response.status_code == 200 and b"%PDF" in response.content[:10]:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(response.content)
                tmp_file_path = tmp_file.name
                
            match_found = False
            try:
                with pdfplumber.open(tmp_file_path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            text_upper = text.upper()
                            for state in target_states:
                                if state in text_upper:
                                    match_found = True
                                    break
                        if match_found:
                            break
            finally:
                if os.path.exists(tmp_file_path):
                    try:
                        os.remove(tmp_file_path)
                    except:
                        pass
            return match_found
            
    except Exception as e:
        print(f"Error reading PDF {pdf_url}: {e}")
        
    return False


def start_gem_scraping(category_text, states_text):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.page_load_strategy = 'eager'

    # 🔥 UPDATED CHROME LOGIC (Render + Local)
    if os.environ.get("RENDER"):
        options.binary_location = "/opt/render/project/src/chrome-linux64/chrome"
        service = Service("/opt/render/project/src/chromedriver-linux64/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    wait = WebDriverWait(driver, 15)
    all_final_results = []
    
    try:
        driver.get("https://bidplus.gem.gov.in/advance-search")

        # CATEGORY
        wait.until(EC.element_to_be_clickable((By.ID, 'select2-categorybid-container'))).click()
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input')))
        search_input.send_keys(category_text)
        time.sleep(0.8)
        search_input.send_keys(Keys.ENTER)

        # STATES
        if states_text:
            selected_states = [s.strip() for s in states_text.split(',') if s.strip()]
            for state in selected_states:
                try:
                    state_container = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="adv-search"]/div[2]/div[2]/div/span/span[1]/span')))
                    state_container.click()
                    state_input = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input')))
                    state_input.send_keys(state)
                    time.sleep(0.6)
                    state_input.send_keys(Keys.ENTER)
                except:
                    continue

        # SEARCH
        search_btn = wait.until(EC.element_to_be_clickable((By.ID, "searchByBid")))
        driver.execute_script("arguments[0].click();", search_btn)
        
        # PAGINATION
        page_count = 1
        while True:
            try:
                wait.until(EC.presence_of_element_located((By.ID, "bidCard")))
                time.sleep(1)
            except:
                break 

            card_found_on_page = False

            for card_index in range(2, 13): 
                card_xpath = f'//*[@id="bidCard"]/div[{card_index}]'
                try:
                    cards = driver.find_elements(By.XPATH, card_xpath)
                    if not cards:
                        continue
                    
                    card = cards[0]
                    if "BID NO:" in card.text.upper():
                        card_found_on_page = True
                        lines = card.text.split('\n')
                        items, dept, sd, ed = "N/A", "N/A", "N/A", "N/A"
                        
                        for i, line in enumerate(lines):
                            l = line.upper()
                            if "ITEMS:" in l:
                                items = line.split(':', 1)[-1].strip()
                            elif "DEPARTMENT NAME AND ADDRESS:" in l:
                                dept = line.split(':', 1)[-1].strip()
                                if not dept and i+1 < len(lines):
                                    dept = lines[i+1].strip()
                            elif "START DATE:" in l:
                                sd = line.split(':', 1)[-1].strip()
                            elif "END DATE:" in l:
                                ed = line.split(':', 1)[-1].strip()

                        link_elem = card.find_element(By.TAG_NAME, "a")
                        bid_no = link_elem.text.strip()
                        bid_link = link_elem.get_attribute("href")

                        if not any(res['bid_no'] == bid_no for res in all_final_results):
                            all_final_results.append({
                                "category": category_text,
                                "bid_no": bid_no,
                                "items": items,
                                "department": dept,
                                "start_date": sd,
                                "end_date": ed,
                                "link": bid_link
                            })
                except:
                    continue

            # NEXT PAGE
            try:
                next_button = driver.find_elements(By.XPATH, "//a[contains(text(), 'Next')] | //a[contains(text(), '»')]")
                if next_button and card_found_on_page:
                    driver.execute_script("arguments[0].scrollIntoView();", next_button[0])
                    time.sleep(0.6)
                    driver.execute_script("arguments[0].click();", next_button[0])
                    page_count += 1
                    time.sleep(1)
                else:
                    break
            except:
                break

    except Exception as e:
        print(f"Scraper Error: {e}")
    finally:
        driver.quit()
    
    return all_final_results