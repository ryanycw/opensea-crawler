import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from itertools import zip_longest

def convertText2Int(input):
    intList = input.split(',')
    output = 0
    for id, element in enumerate(intList):
        output += int(element)*pow(10,3*(len(intList)-id-1))
    
    return output

def main():
    url = 'https://opensea.io/collection/0n1-force'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")  
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
    driver.get(url)
    totalMints = convertText2Int(driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/div[2]/div/div/div[2]/div[2]/div/span').text.split(' ')[0])

    soup = BeautifulSoup(driver.page_source, 'lxml')
    filter = soup.find('div', {'data-testid': 'SearchFilter'})
    properties = filter.find_all('div', {'class': 'StringTraitFilterreact__DivContainer-sc-1ud4ti0-0 hEGgft'})

    output = []

    for i, property in enumerate(properties):
        propertyName = property.find('div', {'class': 'Blockreact__Block-sc-1xf18x6-0 gLNyor'})
        options = property.find_all('button', {'class': 'UnstyledButtonreact__UnstyledButton-sc-ty1bh0-0 btgkrL StringTraitFilter--item'})

        itemCol = []
        amountCol = []
        percentageCol = ['Percentage']

        itemCol.append(propertyName.string)
        amountCol.append("Amount")
        for option in options:
            optionName = option.find('div')
            optionCnt = optionName.findNext('div')
            itemCol.append(optionName.string)
            amountCol.append(optionCnt.string)

        amountCal = [int(integer) for integer in amountCol[1:]]
        percentageCol.extend([round(integer/totalMints*100,2) for integer in amountCal])
        output.extend([itemCol, amountCol, percentageCol])

    exportData = zip_longest(*output, fillvalue = '')
    with open(f"data/{url.split('/')[-1]}-Rariry.csv", 'w', newline='') as outputFile:
        wr = csv.writer(outputFile)
        wr.writerows(exportData)
        outputFile.close()

if __name__ == "__main__":
    main()