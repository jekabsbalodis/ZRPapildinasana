import ftplib
from getpass import getpass
from Constants import FILE_NAME_PROMPT, FTP_PORT_PROMPT, FTP_PORT_PROMPT_ERROR, FTP_PROMPT, PASSWORD_PROMPT, USERNAME_PROMPT
from helpers import intInput, stringInput

userName = stringInput(USERNAME_PROMPT)
passWord = getpass(PASSWORD_PROMPT)
ftpAddress = stringInput(FTP_PROMPT)
ftpPort = intInput(FTP_PORT_PROMPT, FTP_PORT_PROMPT_ERROR)

fileName = stringInput(FILE_NAME_PROMPT)
with open(fileName, 'rb') as file:
    with ftplib.FTP_TLS() as ftps:
        ftps.connect(ftpAddress, ftpPort)
        ftps.login(userName, passWord)
        ftps.prot_p()
        ftps.dir()
        ftps.storbinary('STOR antidopinga_vielas.csv', file)
        ftps.dir()
        ftps.quit()
