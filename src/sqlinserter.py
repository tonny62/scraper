# TODO : Write sql inserter to insert the dictionary of data to database
import configparser
import mysql.connector

def getconfig():
    configurator = configparser.ConfigParser()
    configurator.read("cnf/config.cnf")
    
    credentials = configurator['DEFAULT']

    return credentials

def get_connection():
    try:
        credentials = getconfig()
        cnx = mysql.connector.connect(user=credentials['ID'], 
                password=credentials['PASSWORD'], 
                host=credentials['HostName'], 
                database=credentials['DatabaseName'], charset='utf8', use_unicode=True)
    except:
        raise
    return cnx

def insert_into_db(companyDict1):
    cnx = get_connection()
    try:
        cursor = cnx.cursor()
        data = (companyDict1.get('companynameEN'), 
                companyDict1.get('companynameTH'), 
                companyDict1.get('jpNo'), 
                companyDict1.get('url'), 
                companyDict1.get('address'))
        query = '''INSERT INTO `company`(`companynameEN`,
                `companynameTH`, `jpNo`, `url`, `address`)
            VALUES ('{}', '{}', '{}', '{}', '{}')'''.format(*data)
        cursor.execute(query)
        cnx.commit()
    finally:
        cnx.close()
