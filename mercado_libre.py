from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json


# Lastarria hasta San Antonio
URL_LASTARRIA = "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/_DisplayType_M_OrderId_PRICE_PriceRange_350000CLP-600000CLP_NoIndex_True_item*location_lat:-33.44267359934872*-33.43447268091936,lon:-70.64565900195365*-70.62902930606131"

# Parque bustamante y vaticano chico
URL_PARQUEBUSTAMANTE =  "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/_DisplayType_M_OrderId_PRICE_PriceRange_350000CLP-600000CLP_NoIndex_True_item*location_lat:-33.44381951748974*-33.43561870737608,lon:-70.63385728228812*-70.61722758639579"

# Desde Eliodor yañez con av providencia hasta pedro de valdivia
URL_PROVIDENCIA_SALVADOR = "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/_DisplayType_M_OrderId_PRICE_PriceRange_350000CLP-600000CLP_NoIndex_True_item*location_lat:-33.43857940965276*-33.43037810425487,lon:-70.62565340020832*-70.60902370431599"

# Pedro de valdivia a los leones
URL_PROVIDENCIA_PEDROVALDIVIA = "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/_DisplayType_M_OrderId_PRICE_PriceRange_350000CLP-600000CLP_NoIndex_True_item*location_lat:-33.42926732544433*-33.42106514005666,lon:-70.6230110759364*-70.60638138004407"

# Interior entre manuel montt y los leones
URL_PROVIDENCIA_INTERIOR = "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/_DisplayType_M_OrderId_PRICE_PriceRange_350000CLP-600000CLP_NoIndex_True_item*location_lat:-33.43445360697042*-33.42625191165838,lon:-70.61622809858423*-70.5995984026919"

# Barrio italia
URL_BARRIO_ITALIA = "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/_DisplayType_M_OrderId_PRICE_PriceRange_350000CLP-600000CLP_NoIndex_True_item*location_lat:-33.4466025966135*-33.438402049578656,lon:-70.62506434885682*-70.60843465296449"

# Pocuro
URL_PROVIDENCIA_TOBALABA = "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/_DisplayType_M_OrderId_PRICE_PriceRange_350000CLP-600000CLP_NoIndex_True_item*location_lat:-33.427930559450594*-33.41972824775662,lon:-70.6050144741189*-70.58838477822657"

# Escuela militar:
URL_ESCUELA_MILITAR = "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/_DisplayType_M_OrderId_PRICE_PriceRange_350000CLP-600000CLP_NoIndex_True_item*location_lat:-33.419991598007066*-33.411788536280774,lon:-70.5903678738834*-70.57373817799106"

# Manquehue
URL_MANQUEHUE = "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/_DisplayType_M_OrderId_PRICE_PriceRange_350000CLP-600000CLP_NoIndex_True_item*location_lat:-33.4126504593428*-33.40444670420356,lon:-70.57882698280014*-70.5621972869078"

# Vitacura
URL_VITACURA = "https://listado.mercadolibre.cl/inmuebles/departamentos/arriendo/_DisplayType_M_OrderId_PRICE_PriceRange_350000CLP-600000CLP_NoIndex_True_item*location_lat:-33.40759075994785*-33.39938652696916,lon:-70.60169222140992*-70.58506252551759"


def scrape_all():
    print("Scraping Mercado Libre")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    content_list = []
    content_list.append(scrape_content(driver, URL_LASTARRIA, "Lastarria"))
    content_list.append(scrape_content(driver, URL_PARQUEBUSTAMANTE, "Parque Bustamante"))
    content_list.append(scrape_content(driver, URL_PROVIDENCIA_SALVADOR, "Salvador"))
    content_list.append(scrape_content(driver, URL_PROVIDENCIA_PEDROVALDIVIA, "Pedro de Valdivia"))
    content_list.append(scrape_content(driver, URL_PROVIDENCIA_INTERIOR, "Interior Providencia"))
    content_list.append(scrape_content(driver, URL_BARRIO_ITALIA, "Barrio Italia"))
    content_list.append(scrape_content(driver, URL_PROVIDENCIA_TOBALABA, "Tobalaba"))
    content_list.append(scrape_content(driver, URL_ESCUELA_MILITAR, "Escuela Militar"))
    content_list.append(scrape_content(driver, URL_MANQUEHUE, "Manquehue"))
    content_list.append(scrape_content(driver, URL_VITACURA, "Vitacura"))
    
    driver.quit()
    return content_list
    
def get_links(driver, url):
    driver.get(url)
    
    # Wait for the page to load and locate all the main elements
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-search-map-list"))
    )
    divs = driver.find_elements(By.CLASS_NAME, "ui-search-map-list")
    
    # Collect data from the main page
    data_list = []
    for div in divs:
        try:
            link = div.find_element(By.CLASS_NAME, 'ui-search-result__main-image-link.ui-search-link').get_attribute("href")
            title = div.find_element(By.CLASS_NAME, "ui-search-result__content-link").text
            data_list.append([link, title])
        except Exception as e:
            print(f"Error extracting data from main page element")
    
    return data_list

def get_details(driver, link, zone):
    try:
        driver.get(link)
        
        content_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div'))
        )
        
        title = content_div.find_element(By.XPATH, '//*[@id="header"]/div/div[2]/h1').text
        rent = int(content_div.find_element(By.XPATH, '//*[@id="price"]/div/div/div/span/span/span[2]').text.replace(".", ""))
        expenses = content_div.find_element(By.XPATH, '//*[@id="maintenance_fee_vis"]/p').text
        expenses = int(expenses.split(" ")[-1].replace(".", ""))
        total_price = rent + expenses
        size = int(content_div.find_element(By.XPATH, '//*[@id="highlighted_specs_res"]/div/div[1]/span').text.split(" ")[0])
        
        return {'Title': title, 'Link': link, 'Price': total_price, 'Size': size, 'Zone': zone}               
    except Exception as e:
        print(f"Error extracting data from link {link}")
        return None

def write_json(content_dict, name):
    with open(f'Files/{name}.json', 'w', encoding="utf-8") as file:
        json.dump(content_dict, file, ensure_ascii=False, indent=4)

def read_json(name):
    try:
        with open(f'Files/{name}.json', 'r', encoding="utf-8") as file:
            content_dict = json.load(file)
        return content_dict
    except:
        return {}
        
def scrape_content(driver, url, zone):
    content_dict = read_json(zone)
    new_dict = {}
    try:
        while True:
            data_list = get_links(driver, url)
            
            for data in data_list:
                if data[1] in content_dict.keys():
                    continue
                details_dict = get_details(driver, data[0], zone)
                print(details_dict)
                if (details_dict != None) and (details_dict['Size'] >= 45):
                    content_dict[details_dict['Title']] = details_dict
                    new_dict[details_dict['Title']] = details_dict
                elif details_dict != None:
                        content_dict[details_dict['Title']] = {}
            try:
                driver.get(url)
        
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="root-app"]/div/div[3]/section/div[8]/div[1]/div/div[2]/div[2]/nav/li[3]/a'))
                )
                element.click()
            except:
                print("Element does not exist or did not load in time.")
                break
    except Exception as e:
        print(f"Error during scraping")
    
    write_json(content_dict, zone)
    return new_dict
