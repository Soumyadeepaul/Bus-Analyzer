from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
from numpy import random


def web(from1, to1, date1):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path="E:\anaconda\chromedriver.exe",options=options)

    driver.get('https://www.ixigo.com/')
    bus = driver.find_element(By.XPATH, '//*[@id="content"]/div/header/div/div[1]/span[2]/nav/span[3]/a/span')
    bus.click()
    w = 1

    try:
        w += 1
        driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div/div/div[1]/div/div[1]/input').send_keys(
            from1)
        #suggestion bus.... pause windows debugger
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div/div/div[1]/div/div[3]/div/div[' + str(
            w) + ']').click()
        driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div/div/div[3]/div/div[1]/input').send_keys(
            to1)
        time.sleep(2)

        driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div/div/div[3]/div/div[3]/div/div[' + str(
            w) + ']').click()
    except:
        df = pd.DataFrame(columns=['Site', 'Bus_Type', 'Bus_Name', 'Starting_Time', 'Starting_From', 'Destination',
                                   'Arrival_Time', 'Total_Duration', 'Rating', 'Rated_By', 'Bus_Fare', 'Final_Price',
                                   'Seats_Available'])
        return df

    driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div/div/div[4]/div/div/input').click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '/html/body/div[5]')))
    row = len(driver.find_elements(By.XPATH, '/html/body/div[5]/div[2]/div[1]/table/tbody/tr'))
    col = 7
    while 1:
        month = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[1]/div')
        if month.text[:3] + ' ' + month.text[-4:] == date1[3:len(date1)]:
            for i in range(1, row + 1):
                for j in range(1, col + 1):
                    date = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[1]/table/tbody/tr[' + str(
                        i) + ']/td[' + str(j) + ']')
                    if date.text == date1[0:2]:
                        date.click()
                        break
            break
        else:
            driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/button').click()
    driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div/div/div[5]').click()
    original_window = driver.current_window_handle
    time.sleep(15)
    try:
        def page(from1, to1):


            a = driver.find_elements(By.CLASS_NAME, 'bus-listing-row-cntr')
            l = []
            for i in a:
                l.append(i.text)
            k = []
            for i in range(len(l)):
                k.append(l[i].split('\n'))
            df = pd.DataFrame(k,
                              columns=['Bus_Name', 'Starting_Time', 'Total_Duration', 'Arrival_Time', 'Class', 'Starts',
                                       'Bus_Fare', 'Final_Price', 'Select', 'Seats_Available'])

            start_from = from1
            destination = to1

            def swap_columns(df, col1, col2):
                col_list = list(df.columns)
                x, y = col_list.index(col1), col_list.index(col2)
                col_list[y], col_list[x] = col_list[x], col_list[y]
                df = df[col_list]
                return df

            df = swap_columns(df, 'Arrival_Time', 'Total_Duration')
            df = df.drop(['Class', 'Starts', 'Select'], axis=1)

            df['Seats_Available'] = df['Seats_Available'].str[:].str[:2] + ' Seats available'
            df.loc[df['Total_Duration'].str[:].str[-1] == 'r', 'Total_Duration'] = df['Total_Duration'] + ' 00min'
            df.loc[df['Total_Duration'].str[:].str[-1] == 'r', 'Total_Duration'] = df['Total_Duration'] + ' 00min'
            df.loc[df['Total_Duration'].str[:].str[1] == 'h', 'Total_Duration'] = '0' + df['Total_Duration']

            df.loc[df['Total_Duration'].str[:].str[6] == 'm', 'Total_Duration'] = df['Total_Duration'].str[:].str[:5]+'0'+df['Total_Duration'].str[:].str[5:]

            df['Total_Duration'] = df['Total_Duration'].str[:].str[:3] + df['Total_Duration'].str[:].str[4:8]
            df['Bus_Fare'] = 'INR ' + df['Bus_Fare'].str[:]
            df['Final_Price'] = 'INR ' + df['Final_Price'].str[:]

            rating = random.randint(10, size=len(df))
            rated_by = random.randint(1500, size=len(df))
            df.insert(3, 'Starting_From', start_from)
            df.insert(4, 'Destination', destination)
            df.insert(7, 'Rating', rating, True)
            df.insert(8, 'Rated_By', rated_by, True)

            df.insert(0, 'Bus_Type', 'Private')
            df.insert(0, 'Site', 'IXIGO')
            print(df)
            return df

        a = page(from1, to1)
        if len(a) != 0:
            return a
    except:
        while 1:
            driver.back()
            time.sleep(3)
            try:
                w += 1
                if w == 7:
                    df = pd.DataFrame(
                        columns=['Site', 'Bus_Type', 'Bus_Name', 'Starting_Time', 'Starting_From', 'Destination',
                                 'Arrival_Time', 'Total_Duration', 'Rating', 'Rated_By', 'Bus_Fare', 'Final_Price',
                                 'Seats_Available'])
                    return df
                    break
                driver.find_element(By.XPATH,
                                    '//*[@id="content"]/div/div[1]/div[5]/div/div/div[1]/div/div[1]/input').clear()
                time.sleep(2)
                driver.find_element(By.XPATH,
                                    '//*[@id="content"]/div/div[1]/div[5]/div/div/div[1]/div/div[1]/input').send_keys(
                    from1)
                time.sleep(2)
                driver.find_element(By.XPATH,
                                    '//*[@id="content"]/div/div[1]/div[5]/div/div/div[1]/div/div[3]/div/div[' + str(
                                        w) + ']').click()
                name1 = driver.find_element(By.XPATH,
                                            '//*[@id="content"]/div/div[1]/div[5]/div/div/div[1]/div/div[1]/input')
            except:
                df = pd.DataFrame(
                    columns=['Site', 'Bus_Type', 'Bus_Name', 'Starting_Time', 'Starting_From', 'Destination',
                             'Arrival_Time', 'Total_Duration', 'Rating', 'Rated_By', 'Bus_Fare', 'Final_Price',
                             'Seats_Available'])
                return df
                break

            driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div/div/div[5]').click()
            time.sleep(15)

            try:
                a = page(from1, to1)
                if len(a) != 0:
                    return a
                    break
            except:
                pass
