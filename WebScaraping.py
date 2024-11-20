import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time



async def getReviews():

    url = "https://www.amazon.in/Dervin-Transparent-Eyeglasses-Protection-Anti-blue/dp/B0BC11K6JK/?_encoding=UTF8&pd_rd_w=hcDwR&content-id=amzn1.sym.509965a2-791b-4055-b876-943397d37ed3%3Aamzn1.symc.fc11ad14-99c1-406b-aa77-051d0ba1aade&pf_rd_p=509965a2-791b-4055-b876-943397d37ed3&pf_rd_r=9AR0QTHWGQB844HXSZ8X&pd_rd_wg=HCr9M&pd_rd_r=06a09836-850e-4bac-adc3-9c5316019cc0&ref_=pd_hp_d_atf_ci_mcx_mr_ca_hp_atf_d&th=1&psc=1"

    service=Service("C:\Drivers\chromedriver.exe")
    options=webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver=webdriver.Chrome(service=service,options=options)

    try:
        driver.get(url)
        time.sleep(5)

        reviews = driver.find_elements(By.CSS_SELECTOR, ".card-padding")
        review_texts = [review.text for  review in reviews]

        if not review_texts:
            print("No reviews found")
            return None
        
        return "\n".join(review_texts)
    finally:
        driver.quit()
    
