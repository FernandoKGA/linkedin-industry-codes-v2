import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#get linkedin industry code info as csv
#https://stackoverflow.com/a/65639685/8370521
#document.querySelector('details:nth-child(11) > div:nth-child(3) > table:nth-child(1)')

#get elements and selenium workflows
#https://www.selenium.dev/documentation/webdriver/waits/#explicit-waits
#https://github.com/SeleniumHQ/seleniumhq.github.io/blob/trunk/examples/python/tests/waits/test_waits.py#L41-L42
#https://github.com/SeleniumHQ/seleniumhq.github.io/blob/trunk/examples/python/tests/getting_started/first_script.py#L10
#https://selenium-python.readthedocs.io/locating-elements.html

#https://translate.google.com/
#https://www.deepl.com/pt-BR/translator#en/pt/Investment%20Advice

#https://csvjson.com/csv2json
#https://codebeautify.org/jsonminifier

driver = webdriver.Chrome()

driver.get("https://translate.google.com.br/?hl=pt-BR&sl=en&tl=pt&op=translate")

csvfile = open("./linkedin_industry_code_v2_all_ptbr.csv", "a", newline="")

xpath_input = "/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[1]/span/span/div/textarea"
xpath_output = "/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div/div[6]/div/div[1]/span[1]/span/span"
xpath_output_fem = "/html/body//c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div/div[7]/div[1]/div[1]/span[1]"

with open("./linkedin_industry_code_v2_all_eng.csv", newline="") as linkedincodes:
    csv_reader = csv.reader(linkedincodes, delimiter=",", quotechar='"')
    csvwriter = csv.writer(csvfile, quotechar='"', doublequote=True)
    # begins = False
    for row in csv_reader:
        (id, label, hierarchy, description) = row
        print(f"Eng: {id},{label},{hierarchy}, {description}")
        # usar só se foi interrompido
        # if not begins:
        #     if id == "66":
        #         begins = True
        #     continue

        text_box_input = driver.find_element(
            by=By.XPATH,
            value=xpath_input,
        )
        text_box_input.send_keys(label)
        time.sleep(4)

        try:
            text_box_output = driver.find_element(
                by=By.XPATH,
                value=xpath_output,
            )
        except NoSuchElementException:
            text_box_output = driver.find_element(
                by=By.XPATH,
                value=xpath_output_fem,
            )
        result_group = text_box_output.text
        text_box_input.clear()

        text_box_input = driver.find_element(
            by=By.XPATH,
            value=xpath_input,
        )
        text_box_input.send_keys(hierarchy)
        time.sleep(4)

        try:
            text_box_output = driver.find_element(
                by=By.XPATH,
                value=xpath_output,
            )
        except NoSuchElementException:
            text_box_output = driver.find_element(
                by=By.XPATH,
                value=xpath_output_fem,
            )
        result_hierarchy = text_box_output.text
        text_box_input.clear()

        text_box_input = driver.find_element(
            by=By.XPATH,
            value=xpath_input,
        )
        text_box_input.send_keys(description)
        time.sleep(4)

        try:
            text_box_output = driver.find_element(
                by=By.XPATH,
                value=xpath_output,
            )
        except NoSuchElementException:
            text_box_output = driver.find_element(
                by=By.XPATH,
                value=xpath_output_fem,
            )
        result_description = text_box_output.text
        text_box_input.clear()
        time.sleep(4)

        print("\n")
        print(
            f'PT-BR: "{id}","{result_group}","{result_hierarchy}","{result_description}"'
        )
        csvwriter.writerow(
            [
                id,
                result_group,
                result_hierarchy,
                result_description,
            ]
        )
        csvfile.flush()
        print("\n")

csvfile.close()
driver.quit()
