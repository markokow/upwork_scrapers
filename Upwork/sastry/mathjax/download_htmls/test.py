from selenium import webdriver  
import time  
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

urls_list = [
"https://www.toppr.com/guides/business-mathematics-and-statistics/calculus/methods-of-integration/",
"https://www.toppr.com/guides/chemistry-formulas/ammonium-iodide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ammonium-hydroxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ammonium-dichromate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ammonium-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ammonium-carbonate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ammonium-bromide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ammonium-bicarbonate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ammonium-acetate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ammonia-formula/",
"https://www.toppr.com/guides/chemistry-formulas/acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/aluminum-phosphate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/aluminum-iodide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/aluminium-fluoride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/aluminium-formula/",
"https://www.toppr.com/guides/chemistry-formulas/aluminium-bromide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/aluminium-sulfide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/aluminium-oxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/molecular-formula/",
"https://www.toppr.com/guides/chemistry-formulas/mole-fraction-formula/",
"https://www.toppr.com/guides/chemistry-formulas/molarity-formula/",
"https://www.toppr.com/guides/chemistry-formulas/molar-volume-formula/",
"https://www.toppr.com/guides/chemistry-formulas/molar-mass-formula/",
"https://www.toppr.com/guides/chemistry-formulas/molality-formula/",
"https://www.toppr.com/guides/chemistry-formulas/methyl-acetate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/methane-formula/",
"https://www.toppr.com/guides/chemistry-formulas/mercury-ii-sulfate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/mercury-ii-nitrate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/mercury-ii-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/mass-percent-formula/",
"https://www.toppr.com/guides/chemistry-formulas/manganese-ii-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/maltose-formula/",
"https://www.toppr.com/guides/chemistry-formulas/malic-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/maleic-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/magnesium-sulfate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ionic-compound-formula/",
"https://www.toppr.com/guides/chemistry-formulas/iodous-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/iodide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/iodic-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/internal-energy-formula-2/",
"https://www.toppr.com/guides/chemistry-formulas/cobalt-nitrate-ii-formula/",
"https://www.toppr.com/guides/chemistry-formulas/citric-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/boyles-law-formula/",
"https://www.toppr.com/guides/chemistry-formulas/chromic-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/chromate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/cholesterol-formula/",
"https://www.toppr.com/guides/chemistry-formulas/charles-law-formula/",
"https://www.toppr.com/guides/chemistry-formulas/carbonous-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/enthalpy-formula/",
"https://www.toppr.com/guides/chemistry-formulas/empirical-formula/",
"https://www.toppr.com/guides/chemistry-formulas/electron-dot-formula/",
"https://www.toppr.com/guides/chemistry-formulas/dinitrogen-trioxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/dinitrogen-pentoxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/carbonate-ion-formula/",
"https://www.toppr.com/guides/chemistry-formulas/borax-formula",
"https://www.toppr.com/guides/chemistry-formulas/bond-order-formula/",
"https://www.toppr.com/guides/chemistry-formulas/boiling-point-formula/",
"https://www.toppr.com/guides/chemistry-formulas/bismuth-iii-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/magnesium-hydroxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/magnesium-acetate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/carbon-disulfide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/camphor-formula/",
"https://www.toppr.com/guides/chemistry-formulas/calcium-iodide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/calcium-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/bromic-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/number-of-moles-formula/",
"https://www.toppr.com/guides/chemistry-formulas/octane-formula/",
"https://www.toppr.com/guides/chemistry-formulas/osmotic-pressure-formula/",
"https://www.toppr.com/guides/chemistry-formulas/oxalate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/oxalic-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/nitrogen-dioxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/normality-formula/",
"https://www.toppr.com/guides/chemistry-formulas/nitrite-formula/",
"https://www.toppr.com/guides/chemistry-formulas/nickel-sulphate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/nickel-nitrate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/lithium-oxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/magnesium-iodide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/lithium-iodide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/magnesium-oxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/magnesium-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/lead-ii-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/lithium-hydroxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/lead-iv-acetate/",
"https://www.toppr.com/guides/chemistry-formulas/lead-iv-oxide/",
"https://www.toppr.com/guides/chemistry-formulas/limiting-reactant-formula/",
"https://www.toppr.com/guides/chemistry-formulas/lithium-bromide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/lithium-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/iron-iii-hydroxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/hypobromous-acid/",
"https://www.toppr.com/guides/chemistry-formulas/hyponitrous-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/hypochlorous-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/hydrazine-formula/",
"https://www.toppr.com/guides/chemistry-formulas/glutaric-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ionic-strength-formula/",
"https://www.toppr.com/guides/chemistry-formulas/iron-iii-nitrate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/iron-iii-oxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ionization-energy-formula/",
"https://www.toppr.com/guides/chemistry-formulas/iron-ii-oxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ethane-formula/",
"https://www.toppr.com/guides/chemistry-formulas/ethyl-acetate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/cobalt-ii-sulfate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/combined-gas-law-formula/",
"https://www.toppr.com/guides/chemistry-formulas/condensed-structural-formula/",
"https://www.toppr.com/guides/chemistry-formulas/copper-chemical-formula/",
"https://www.toppr.com/guides/chemistry-formulas/copper-i-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/copper-ii-carbonate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/degree-of-unsaturation-formula/",
"https://www.toppr.com/guides/chemistry-formulas/density-of-gas-formula/",
"https://www.toppr.com/guides/chemistry-formulas/cyanide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/copper-ii-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/copper-ii-nitrate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/copper-sulfate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/daltons-law-formula/",
"https://www.toppr.com/guides/chemistry-formulas/dinitrogen-monoxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/dimethylglyoxime-formula/",
"https://www.toppr.com/guides/chemistry-formulas/dilution-formula/",
"https://www.toppr.com/guides/chemistry-formulas/diffusion-formula/",
"https://www.toppr.com/guides/chemistry-formulas/dichloroacetic-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/chlorine-gas-formula/",
"https://www.toppr.com/guides/chemistry-formulas/chlorate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/chemical-reaction-formula/",
"https://www.toppr.com/guides/chemistry-formulas/chemical-formula/",
"https://www.toppr.com/guides/chemistry-formulas/chemical-compound-formulas/",
"https://www.toppr.com/guides/chemistry-formulas/barium-hydroxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/barium-fluoride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/barium-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/barium-bromide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/barium-acetate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/aluminium-hydroxide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/aluminium-chloride-formula/",
"https://www.toppr.com/guides/chemistry-formulas/aluminium-carbonate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/activation-energy-formula/",
"https://www.toppr.com/guides/chemistry-formulas/acetaldehyde-formula/",
"https://www.toppr.com/guides/chemistry-formulas/acetone-formula/",
"https://www.toppr.com/guides/chemistry-formulas/acetonitrile-formula/",
"https://www.toppr.com/guides/chemistry-formulas/acetylene-formula/",
"https://www.toppr.com/guides/chemistry-formulas/acetamide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/calcium-bromide-formula/",
"https://www.toppr.com/guides/chemistry-formulas/calcium-acetate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/caffeine-chemical-formula/",
"https://www.toppr.com/guides/chemistry-formulas/cadmium-sulfate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/cadmium-nitrate-formula/",
"https://www.toppr.com/guides/chemistry-formulas/butyric-acid-formula/",
"https://www.toppr.com/guides/chemistry-formulas/butane-formula/",
"https://www.toppr.com/guides/chemistry-formulas/butan-1-ol-formula/",
"https://www.toppr.com/guides/chemistry-formulas/bromine-formula/",
]
from time import sleep
for url in urls_list:
    # driver = webdriver.Chrome(r"C:\Users\USER\Downloads\chromedriver.exe")
    driver = webdriver.Firefox()
    driver.get(url)   
    get_source = driver.page_source
    
    
    print('Started Writing into file')
    
    filename = url.split('/')[-2]
    
    # with open('Downloads/'+filename+'.html', 'w', encoding = 'utf-8') as f:
    #     f.write(get_source)

    print(url,' completed')
    sleep(3)
    print(driver.title)
    web_string = driver.find_element(By.XPATH, '//*[@id="content"]').text
    # web_string = driver.find_element(By.XPATH, '//*[@id="wrap-main"]').text
    # print(driver.find_element(By.ID, 'wrap-main').text.encode('utf-8'))

    with open("Output.txt", "w", encoding='utf-8') as text_file:
        text_file.write(web_string)

    driver.quit()

    # print(get_source.encode('utf-8'))

    soup = BeautifulSoup(get_source.encode('utf-8','ignore'), "lxml")
    soup = soup.encode('utf-8')


    break
print ("############################# ALL COMPLETED ####################################")


