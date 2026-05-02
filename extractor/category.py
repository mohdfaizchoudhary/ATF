
# import json
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# def scrape_gem_forcefully():
#     url = "https://bidplus.gem.gov.in/advance-search"
#     output_file = 'gem_categories.json'
    
#     options = Options()
#     driver = webdriver.Chrome(options=options)
#     wait = WebDriverWait(driver, 20)

#     try:
#         driver.get(url)
#         print("1. Page load ho gaya...")

#         # Step 1: Tab click
#         tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab0"]')))
#         tab.click()
#         print("2. Tab click ho gaya.")
#         time.sleep(2)
        
#         # Step 2: Dropdown click
#         category_box = wait.until(EC.element_to_be_clickable((By.ID, "select2-categorybid-container")))
#         category_box.click()
#         print("3. Dropdown open ho gaya.")
#         time.sleep(3) 

#         categories_set = set()
#         last_count = 0
#         no_new_data_count = 0

#         print("4. Scraping start... (Using JS Force)")

#         while True:
#             # JavaScript se saare LI elements ka text nikalna
#             # Ye method Selenium ke normal element finder se 10x zyada fast aur reliable hai
#             js_script = """
#             var items = document.querySelectorAll('#select2-categorybid-results li');
#             var texts = [];
#             for (var i = 0; i < items.length; i++) {
#                 texts.push(items[i].innerText);
#             }
#             return texts;
#             """
#             current_texts = driver.execute_script(js_script)

#             for text in current_texts:
#                 val = text.strip()
#                 if val and val not in ["Searching…", "Select Category", "No results found"]:
#                     categories_set.add(val)

#             current_count = len(categories_set)
            
#             if current_count > last_count:
#                 # Real-time save
#                 with open(output_file, 'w', encoding='utf-8') as f:
#                     json.dump(sorted(list(categories_set)), f, indent=4, ensure_ascii=False)
                
#                 last_count = current_count
#                 no_new_data_count = 0
#                 print(f"Pragati: {current_count} categories saved.", end="\r")
#             else:
#                 no_new_data_count += 1

#             # Step 3: Scroll Down using JS
#             scroll_js = "document.querySelector('.select2-results__options').scrollTop += 500;"
#             driver.execute_script(scroll_js)
            
#             time.sleep(0.6) # Thoda sa time load hone ke liye

#             # Agar 20 baar scroll karne par bhi naya data na mile toh exit
#             if no_new_data_count > 20:
#                 break

#         print(f"\n\nKaam Pura! Final Count: {len(categories_set)}")
#         print(f"File '{output_file}' check karo.")

#     except Exception as e:
#         print(f"\nError: {e}")
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     scrape_gem_forcefully()




import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


def scrape_gem_forcefully():
    url = "https://bidplus.gem.gov.in/advance-search"
    output_file = 'gem_categories.json'
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # 🔥 UPDATED CHROME LOGIC (Render + Local)
    if os.environ.get("RENDER"):
        options.binary_location = "/opt/render/project/src/chrome-linux64/chrome"
        service = Service("/opt/render/project/src/chromedriver-linux64/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 20)

    try:
        driver.get(url)
        print("1. Page load ho gaya...")

        # Step 1: Tab click
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab0"]')))
        tab.click()
        print("2. Tab click ho gaya.")
        time.sleep(2)
        
        # Step 2: Dropdown click
        category_box = wait.until(EC.element_to_be_clickable((By.ID, "select2-categorybid-container")))
        category_box.click()
        print("3. Dropdown open ho gaya.")
        time.sleep(3) 

        categories_set = set()
        last_count = 0
        no_new_data_count = 0

        print("4. Scraping start... (Using JS Force)")

        while True:
            js_script = """
            var items = document.querySelectorAll('#select2-categorybid-results li');
            var texts = [];
            for (var i = 0; i < items.length; i++) {
                texts.push(items[i].innerText);
            }
            return texts;
            """
            current_texts = driver.execute_script(js_script)

            for text in current_texts:
                val = text.strip()
                if val and val not in ["Searching…", "Select Category", "No results found"]:
                    categories_set.add(val)

            current_count = len(categories_set)
            
            if current_count > last_count:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(sorted(list(categories_set)), f, indent=4, ensure_ascii=False)
                
                last_count = current_count
                no_new_data_count = 0
                print(f"Pragati: {current_count} categories saved.", end="\r")
            else:
                no_new_data_count += 1

            # Scroll
            scroll_js = "document.querySelector('.select2-results__options').scrollTop += 500;"
            driver.execute_script(scroll_js)
            
            time.sleep(0.6)

            if no_new_data_count > 20:
                break

        print(f"\n\nKaam Pura! Final Count: {len(categories_set)}")
        print(f"File '{output_file}' check karo.")

    except Exception as e:
        print(f"\nError: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_gem_forcefully()