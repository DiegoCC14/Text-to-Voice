from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Text_Voice_bot():
	
	driver = None
	count_process = 0

	def __init__( self ):
		self.count_process = 0
		options = webdriver.ChromeOptions()
		options.add_argument('--incognito')
		self.driver = webdriver.Chrome( chrome_options=options )

	def close_driver( self ):
		if self.driver is not None:
			self.driver.quit()
		self.driver = None

	def get_countrys_avalibles( self ):
		self.driver.get( 'https://www.narakeet.com/app/text-to-audio/' )

		WebDriverWait( self.driver , 15).until(
			EC.visibility_of_element_located( ( By.XPATH , './/select[@id="cfgVideoLanguage"]//option[ @value="en-US" ]' ) )
		)
		list_countrys = self.driver.find_elements( By.XPATH , './/select[@id="cfgVideoLanguage"]/option' )
		return [ country.text for country in list_countrys ]

	def get_voices_avalibles( self , country ):
		self.driver.get( 'https://www.narakeet.com/app/text-to-audio/' )
		
		WebDriverWait( self.driver , 15).until(
			EC.visibility_of_element_located( ( By.XPATH , f'.//select[@id="cfgVideoLanguage"]//option[ text()="{country}"]' ) )
		)
		obj_option_country = self.driver.find_element( By.XPATH , f'.//select[@id="cfgVideoLanguage"]//option[ text()="{country}" ]' )
		obj_option_country.click()

		WebDriverWait( self.driver , 15).until(
			EC.visibility_of_element_located( ( By.XPATH , f'.//select[@id="cfgVideoVoice"]/option' ) )
		)
		list_voices_country = self.driver.find_elements( By.XPATH , f'.//select[@id="cfgVideoVoice"]/option' )
		
		return [ { 'name':voices.text ,
			'url':f'https://www.narakeet.com/samples/voices/{voices.get_attribute('value')}.mp3'} for voices in list_voices_country ]

	def texto_to_voice( self , country , voice , text ):
		self.driver.get( 'https://www.narakeet.com/app/text-to-audio/' )

		WebDriverWait( self.driver , 15).until(
			EC.visibility_of_element_located( ( By.XPATH , f'.//select[@id="cfgVideoLanguage"]//option[ text()="{country}"]' ) )
		)
		obj_option_country = self.driver.find_element( By.XPATH , f'.//select[@id="cfgVideoLanguage"]//option[ text()="{country}" ]' )
		obj_option_country.click()

		WebDriverWait( self.driver , 5).until(
			EC.visibility_of_element_located( ( By.XPATH , f'.//select[@id="cfgVideoVoice"]//option[ text()="{voice}" ]' ) )
		)
		obj_option_voice = self.driver.find_element( By.XPATH , f'.//select[@id="cfgVideoVoice"]//option[ text()="{voice}" ]' )
		obj_option_voice.click()

		obj_div_text = self.driver.find_element( By.XPATH , f'.//div[@id="unparsedScriptEditor"]' )
		obj_div_text.send_keys( text )

		obj_button_creae_voice = self.driver.find_element( By.XPATH , f'//*[@id="workflowUploadForm"]//button[@role="create-audio"]' )
		obj_button_creae_voice.click()

		WebDriverWait( self.driver , 25).until(
			EC.element_to_be_clickable( ( By.XPATH , f'//a[@role="audio"]' ) )
		)
		obj_a_download = self.driver.find_element( By.XPATH , f'//a[@role="audio"]' )
		
		return obj_a_download.get_attribute('href')


if __name__ == "__main__":

	bot_Voice = Text_Voice_bot()

	print( bot_Voice.get_countrys_avalibles() )
	input('Espera Paises...')

	print( bot_Voice.get_voices_avalibles( 'Spanish - Mexican' ) )
	input('Espera Voces...')
	
	texto = "Habia una vez en un tranquilo pueblo llamado Serenidad, un pequeno zorro llamado Max. Max era curioso y siempre buscaba nuevas aventuras.\n"
	texto += "Un dia, mientras exploraba el bosque, Max encontro un antiguo mapa escondido entre las hojas caidas. El mapa mostraba un camino hacia el legendario Arbol de los Deseos, un lugar magico donde, segun la leyenda, los suenos se hacian realidad.\n"
	#texto = texto[0:1019] #1019
	
	url_voice = bot_Voice.texto_to_voice( 'Spanish - Mexican' , 'Ramona' , texto )
	print( f'1 ->> {url_voice}' )
	bot_Voice.close_driver()