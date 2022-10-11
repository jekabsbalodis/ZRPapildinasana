INCLUDE_PROMPT = 'Vai medikamentu iekļaut sarakstā (\"Jā\"/\"Nē\")? '
INCLUDE_ERROR = 'Lūdzu ievadi tikai \"Jā\" vai \"Nē\"!'

PROHIBITED_OUT_PROMPT = 'Vai medikamentu aizliegts lietot sacensībās un ārpus tām? (\"Jā\"/\"Nē\"/\"Jā*\"/\"Ar nosacījumu\")? '
PROHIBITED_IN_PROMPT = 'Vai medikamentu aizliegts lietot sacensību laikā (\"Jā\"/\"Nē\"/\"Jā*\"/\"Ar nosacījumu\")? '
PROHIBITED_ERROR = 'Lūdzu ievadi tikai \"Jā\", \"Nē\", \"Jā*\" vai \"Ar nosacījumu\"!'

DELTA_DATE_FROM_PROMPT = 'Ievadi datumu, no kura kura vēlies redzēt pievienotos medikamentus (\"Formāts YYYY-MM-DD\") '

USERNAME_PROMPT = 'Ievadi lietotāja vārdu! '
PASSWORD_PROMPT = 'Ievadi paroli! '
FTP_PROMPT = 'Ievadi servera adresi! '
FTP_PORT_PROMPT = 'Ievadi servera portu! '
FTP_PORT_PROMPT_ERROR = 'Lūdzu ievadi skaitļus'
RESOURCE_ID_PROMPT = 'Ievadi resursa ID numuru! '
API_PROMPT = 'Ievadi data.gov.lv API atslēgu! '
FILE_NAME_PROMPT = 'Ievadi nosaukumu failam, kuru augšupielādēt! '

YES = 'Jā'
YES_FOR_SOME_SPORTS = 'Jā*'
YES_WITH_EXCEPTIONS = 'Ar nosacījumu'
NO = 'Nē'

PROHIBITED_CLASSES = ['S0', 'S1', 'S2', 'S3', 'S4',
                      'S5', 'M1', 'M2', 'M3', 'S6', 'S7', 'S8', 'S9', 'P1']
PROHIBITED_CLASS_PROMPT = 'Lūdzu ievadi Aizliegto vielu un metožu saraksta klasi vai klases!\n' + \
    str(PROHIBITED_CLASSES) + '\n'
PROHIBITED_CLASS_ERROR = 'Lūdzu neaizmirsti norādīt aizliegto vielu un metožu klasi!'

NOTES_PROMPT = 'Ievadi informāciju, kuru saglabāt laukā \"Piezīmes\"!\n'
NOTES_PROMPT_EN = 'Ievadi šo informāciju angliski!\n'

P1 = {'sports_in_competition_lv': 'lokšaušana (WA), autosports (FIA), biljards (WCBS), šautriņu mešana (WDF), golfs (IGF), šaušana (ISSF, IPC), slēpošana/snovbords - atsevišķas disciplīnas (FIS), zemūdens sporta veidi - atsevišķas disciplīnas (CMAS)',
      'sports_out_competition_lv': 'lokšaušana (WA), šaušana (ISSF, IPC)',
      'sports_in_competition_en': 'archery (WA), automobile (FIA), billiards (WCBS), darts (WDF), golf (IGF), shooting (ISSF, IPC), skiing/snowboarding - specific disciplines (FIS), underwater sports - specific disciplines(CMAS)',
      'sports_out_competition_en': 'archery (WA), shooting (ISSF, IPC)'}
