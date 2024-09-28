import time
from time import sleep
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
from openpyxl import load_workbook
from datetime import date
from glob import glob
from shutil import move
import tabula
from PyPDF2 import PdfReaderrt 

class seiRJ:

    def __init__(self, navegador : webdriver.Firefox):
        self.navegador = navegador
            

    def loginSEI(self,login, senha):
        
        self.navegador.get("https://sei.rj.gov.br/sip/login.php?sigla_orgao_sistema=ERJ&sigla_sistema=SEI")
        
        usuario = self.navegador.find_element(By.XPATH, value='//*[@id="txtUsuario"]')
        usuario.send_keys(login)

        senha = self.navegador.find_element(By.XPATH, value='//*[@id="pwdSenha"]')
        senha.send_keys(senha)

        exercicio = Select(self.navegador.find_element(By.XPATH, value='//*[@id="selOrgao"]'))
        exercicio.select_by_visible_text('SEFAZ')

        btnLogin = self.navegador.find_element(By.XPATH, value='//*[@id="Acessar"]')
        btnLogin.click()

        self.navegador.maximize_window()
        time.sleep(5)

        self.navegador.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        
        self.trocarCoordenacao()          
        
    def trocarCoordenacao(self, nomeCoordenacao):
        coordenacao = self.navegador.find_elements(By.XPATH, "//a[@id = 'lnkInfraUnidade']")[1]
        print(coordenacao)
        if coordenacao.get_attribute("innerHTML") != nomeCoordenacao:
            print(coordenacao)
            coordenacao.click()
            WebDriverWait(self.navegador,5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Trocar Unidade')]")))
            self.navegador.find_element(By.XPATH, "//td[text() = '"+nomeCoordenacao+"' ]").click()    

    def abrirPastas(self):
        self.navegador.switch_to.default_content()
        WebDriverWait(self.navegador,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
        listaDocs = WebDriverWait(self.navegador,5).until(EC.presence_of_element_located((By.ID, "divArvore")))
        pastas = listaDocs.find_elements(By.XPATH, '//a[contains(@id, "joinPASTA")]')
        
        for doc in pastas[:-1]:
            doc.click() 
            sleep(4)
            
        self.navegador.switch_to.default_content()