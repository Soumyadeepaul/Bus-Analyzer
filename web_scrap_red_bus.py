from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
def web(place1,place2,date):
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
    driver.get('https://www.redbus.in/')
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, '//*[@id="search"]/div/div[1]')
    from_place = driver.find_element(By.XPATH, '//*[@id="src"]')
    from_place.send_keys(place1)
    driver.find_element(By.CLASS_NAME, 'selected').click()
    driver.find_element(By.XPATH, '//*[@id="search"]/div/div[2]')
    to_place = driver.find_element(By.XPATH, '//*[@id="dest"]')
    to_place.send_keys(place2)
    driver.find_element(By.CLASS_NAME, 'selected').click()
    driver.find_element(By.XPATH, '//*[@id="search"]/div/div[3]').click()
    wait = WebDriverWait(driver, 5)
    wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//*[@id="onward_cal"]')))

    # rows=driver.find_elements(By.TAG_NAME,'tr')
    # print(len(rows))

    # today=driver.find_element(By.XPATH,'//*[@id="rb-calendar_onward_cal"]/table/tbody/tr[5]/td[6]')
    # today.click()


    # row column count
    row = len(driver.find_elements(By.XPATH, '//*[@id="rb-calendar_onward_cal"]/table/tbody/tr'))
    col = 7  # 7days in a week

    while 1:
        month = driver.find_element(By.CLASS_NAME, 'monthTitle')
        if 'Jan 2023' == month.text:
            for i in range(3, row + 1):
                for j in range(1, 7 + 1):
                    date = driver.find_element(By.XPATH,
                                               "//*[@id='rb-calendar_onward_cal']/table/tbody/tr[" + str(i) + "]/td[" + str(
                                                   j) + "]")
                    if date.text == '26':
                        date.click()
                        break
            break
        else:
            driver.find_element(By.XPATH, '//*[@id="rb-calendar_onward_cal"]/table/tbody/tr[1]/td[3]').click()

    search = driver.find_element(By.XPATH, '//*[@id="search_btn"]')
    search.click()


    # GOVERNMENT BUS
    def govern(g_data):  # govenment data extracted one by one
        number_of_buses = len(driver.find_elements(By.XPATH, '//*[@id="result-section"]/div[2]/div[2]/ul/div'))
        for j in range(1, number_of_buses + 1):
            bus = driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[1]/div[1]")

            starting_time = driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[2]/div[1]")  # starting time
            try:
                starting_day = driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[2]/div[2]").text
                starting_from = driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[2]/div[3]")  # Start location

            except:
                starting_day = 'Same Day'
                starting_from = driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[2]/div[2]")  # Start location

            total_duration = driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[3]/div")  # Total Duration

            arrival_time = driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[4]/div[1]")  # arrival time
            try:
                arrival_day = driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[4]/div[2]").text  # next day

            except:
                arrival_day = 'Same Day'

            destination = driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[4]/div[3]")  # destination name
            try:
                rating = driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[5]/div[1]/div/span").text  # RATING
            except:
                rating = 'No_Rating'
            try:
                number_of_people_rated = driver.find_element(By.XPATH,
                                                             "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                                                                 j) + "]/li/div/div[1]/div[1]/div[5]/div[2]/span").text  # Rating by number of people
            except:
                number_of_people_rated = '0'
            currency = driver.find_elements(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[6]/div/div")  # PRICE CURRENCY

            price = []
            if len(currency) == 1:
                price.extend([currency[0].text, currency[0].text])
            elif len(currency) == 2:
                price.extend([currency[0].text, currency[0].text[0:4] + currency[1].text])
            else:
                price.extend([currency[1].text, currency[1].text[0:4] + currency[2].text])

            seats_available = driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div[2]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[7]/div[1]")  # seats available

            list1 = ['Government', bus.text, starting_time.text, starting_day, starting_from.text, destination.text,
                     arrival_time.text, total_duration.text, arrival_day, rating, number_of_people_rated, price[0],
                     price[1], seats_available.text]

            g_data = g_data.append(pd.DataFrame([list1], columns=['Bus_Type', 'Bus_Name', 'Starting_Time', 'Starting_Day',
                                                                  'Starting_From', 'Destination', 'Arrival_Time',
                                                                  'Total_Duration', 'Arrival_Day', 'Rating', 'Rated_By',
                                                                  'Bus_Fare', 'Final_Price', 'Seats_Available']),
                                   ignore_index=True)
        return g_data


    # PRIVATE BUS
    def private_government(i, data):  # data fetched one by one
        number_of_buses = len(
            driver.find_elements(By.XPATH, '//*[@id="result-section"]/div[' + str(i) + ']/ul/div'))  # number of div

        wait = WebDriverWait(driver, 5)
        wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(
            i) + "]/ul/div[" + str(number_of_buses) + "]")))

        for j in range(1, number_of_buses + 1):

            bus = driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[1]/div[1]")  # bus
            starting_time = driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[2]/div[1]")  # starting time
            try:
                starting_day = driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[2]/div[2]").text
                starting_from = driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[2]/div[3]")  # Start location

            except:
                starting_day = 'Same Day'
                starting_from = driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[2]/div[2]")  # Start location

            total_duration = driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[3]/div")  # Total Duration
            arrival_time = driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[4]/div[1]")  # arrival time
            try:
                arrival_day = driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[4]/div[2]").text  # arrival day
            except:
                arrival_day = 'Same Day'

            destination = driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[4]/div[3]")  # destination name
            try:
                rating = driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[5]/div[1]/div/span").text  # RATING
            except:
                rating = 'No_Rating'
            try:
                number_of_people_rated = driver.find_element(By.XPATH,
                                                             "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                                                                 j) + "]/li/div/div[1]/div[1]/div[5]/div[2]/span").text  # Rating by number of people
            except:
                number_of_people_rated = '0'
            currency = driver.find_elements(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[6]/div/div")  # PRICE CURRENCY

            price = []
            if len(currency) == 1:
                price.extend([currency[0].text, currency[0].text])
            elif len(currency) == 2:
                if currency[0].text[0:6] == 'Starts':

                    price.extend([currency[1].text, currency[1].text])
                else:
                    price.extend([currency[0].text, currency[0].text[0:4] + currency[1].text])
            else:
                price.extend([currency[1].text, currency[1].text[0:4] + currency[2].text])

            seats_available = driver.find_element(By.XPATH, "//*[@id='result-section']/div[" + str(i) + "]/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[7]/div[1]")  # seats available

            list1 = ['Private', bus.text, starting_time.text, starting_day, starting_from.text, destination.text,
                     arrival_time.text, total_duration.text, arrival_day, rating, number_of_people_rated, price[0],
                     price[1], seats_available.text]

            data = data.append(pd.DataFrame([list1], columns=['Bus_Type', 'Bus_Name', 'Starting_Time', 'Starting_Day',
                                                              'Starting_From', 'Destination', 'Arrival_Time',
                                                              'Total_Duration', 'Arrival_Day', 'Rating', 'Rated_By',
                                                              'Bus_Fare', 'Final_Price', 'Seats_Available']),
                               ignore_index=True)
        return data


    # ONLY PRIVATE BUS
    def only_private(data):  # data fetched one by one
        number_of_buses = len(driver.find_elements(By.XPATH, '//*[@id="result-section"]/div/ul/div'))  # number of div

        wait = WebDriverWait(driver, 5)
        wait.until(EC.element_to_be_clickable(
            driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(number_of_buses) + "]")))

        for j in range(1, number_of_buses + 1):

            bus = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[1]/div[1]")  # bus

            starting_time = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[2]/div[1]")  # starting time
            try:
                starting_day = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[2]/div[2]").text
                starting_from = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[2]/div[3]")  # Start location

            except:
                starting_day = 'Same Day'
                starting_from = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[2]/div[2]")  # Start location

            total_duration = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[3]/div")  # Total Duration
            arrival_time = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[4]/div[1]")  # arrival time
            try:
                arrival_day = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[4]/div[2]").text  # arrival day
                destination = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[4]/div[3]")  # destination name

            except:
                arrival_day = 'Same Day'
                destination = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[4]/div[2]")  # destination name
            try:
                rating = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[5]/div[1]/div/span").text  # RATING
            except:
                rating = 'No_Rating'
            try:
                number_of_people_rated = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                    j) + "]/li/div/div[1]/div[1]/div[5]/div[2]/span").text  # Rating by number of people
            except:
                number_of_people_rated = '0'
            currency = driver.find_elements(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[6]/div/div")  # PRICE CURRENCY

            price = []
            if len(currency) == 1:
                price.extend([currency[0].text, currency[0].text])
            elif len(currency) == 2:
                if currency[0].text[0:6] == 'Starts':

                    price.extend([currency[1].text, currency[1].text])
                else:
                    price.extend([currency[0].text, currency[0].text[0:4] + currency[1].text])
            else:
                price.extend([currency[1].text, currency[1].text[0:4] + currency[2].text])

            seats_available = driver.find_element(By.XPATH, "//*[@id='result-section']/div/ul/div[" + str(
                j) + "]/li/div/div[1]/div[1]/div[7]/div[1]")  # seats available

            list1 = ['Private', bus.text, starting_time.text, starting_day, starting_from.text, destination.text,
                     arrival_time.text, total_duration.text, arrival_day, rating, number_of_people_rated, price[0],
                     price[1], seats_available.text]

            data = data.append(pd.DataFrame([list1], columns=['Bus_Type', 'Bus_Name', 'Starting_Time', 'Starting_Day',
                                                              'Starting_From', 'Destination', 'Arrival_Time',
                                                              'Total_Duration', 'Arrival_Day', 'Rating', 'Rated_By',
                                                              'Bus_Fare', 'Final_Price', 'Seats_Available']),
                               ignore_index=True)
        return data


    try:
        time.sleep(10)
        driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div/div[2]")

        total_buses = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div[2]/div[1]/span[1]/span')
        print(total_buses.text)

        # scrolling
        scroll_time_pause = 2
        # get scroll height
        last_height = driver.execute_script('return document.body.scrollHeight')

        while True:
            # scroll down to buttom
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # wait to load Page
            time.sleep(scroll_time_pause)

            # caculate new height
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height
        driver.execute_script("window.scrollTo(0,0)")
        try:  # government bus available
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@id="result-section"]/div[2]')  # governement bus present

            # government_bus_number=driver.find_element(By.XPATH,'//*[@id="result-section"]/div[2]') #government bus available
            # print(government_bus_number.text)
            i = 2
            while i:
                government_bus_number = driver.find_element(By.XPATH, '//*[@id="result-section"]/div[' + str(i) + ']')
                a = government_bus_number.text
                if 'Book your choice of bus on RTC' in a:
                    i += 1
                else:
                    break
            government_bus_total = i - 2

            # government bus data
            wait = WebDriverWait(driver, 10)
            wait.until(EC.element_to_be_clickable(
                driver.find_element(By.XPATH, "//*[@id='result-section']/div[2]/div/div[2]/div/div[4]/div[2]")))
            driver.find_element(By.XPATH,
                                '//*[@id="result-section"]/div[2]/div/div[2]/div/div[4]/div[2]').click()  # to view bus

            wait = WebDriverWait(driver, 5)
            wait.until(EC.element_to_be_clickable(
                driver.find_element(By.XPATH, '//*[@id="result-section"]/div[2]/div[2]/ul/div[1]')))

            g_data = pd.DataFrame(
                columns=['Bus_Type', 'Bus_Name', 'Starting_Time', 'Starting_Day', 'Starting_From', 'Destination',
                         'Arrival_Time', 'Total_Duration', 'Arrival_Day', 'Rating', 'Rated_By', 'Bus_Fare', 'Final_Price',
                         'Seats_Available'])
            g_data = govern(g_data)
            display(g_data)

            driver.find_element(By.XPATH, '//*[@id="result-section"]/div[2]/div[1]/div[2]/div/div[4]/div[2]').click()
            section = len(driver.find_elements(By.XPATH, "//*[@id='result-section']/div"))  # total number of div
            data = pd.DataFrame(
                columns=['Bus_Type', 'Bus_Name', 'Starting_Time', 'Starting_Day', 'Starting_From', 'Destination',
                         'Arrival_Time', 'Total_Duration', 'Arrival_Day', 'Rating', 'Rated_By', 'Bus_Fare', 'Final_Price',
                         'Seats_Available'])
            i = 1
            while i < section:
                if i == 1:
                    data = private_government(i + government_bus_total + 1, data)
                    i += 1 + 2
                else:
                    data = private_government(i + 1, data)
                    i += 2
            display(data)

            total_data = [g_data, data]
            result = pd.concat(total_data)
            excel_create = pd.ExcelWriter(place1+'_to_'+place2+'.xlsx')
            result.to_excel(excel_create, 'Bus_Detail')
            excel_create.save()

        except:
            data = pd.DataFrame(
                columns=['Bus_Type', 'Bus_Name', 'Starting_Time', 'Starting_Day', 'Starting_From', 'Destination',
                         'Arrival_Time', 'Total_Duration', 'Rating', 'Rated_By', 'Bus_Fare', 'Final_Price',
                         'Seats_Available'])
            data = only_private(data)
            display(data)
            excel_create = pd.ExcelWriter(place1+'_to_'+place2+'.xlsx')
            data.to_excel(excel_create, 'Bus_Detail')
            excel_create.save()
    except:
        print("NO BUS")
