GuardianKey: Securing Your Digital Realm. This is my last year college project where i created a totp based 2fa application which can be executed from a usb drive.
The usb also has a password manager application as well
I used portable python, vs code and developed the application in usb drive. I created a venv(virtual environment) of python installed in the usb drive and installed the required libraries there.
One plus point of this project is nothing goes into the web. All stored-keys and passwords are stored in the usb drive only into a folder called as OP when you run the application.
By this we are creating less dependency and all the files and folder stay with the user only.
constraint is that both the application read the stored-keys/passwords form a text file, and if a encrypt the .txt files then i have to again decrypt them and those decrypted files then also won't be safe.
I have used 7-zip portable to encrypt the files and am looking for other ways to secure the keys and password files.
--------- ---------
Steps to use the application:
1. Insert a usb drive(size of 4gb is more than enough) into your pc and install portable python and create a venv in it(so that it does not conflict with the env of your pc)
2. Open cmd where you portable python is installed and type this command: python -m venv path/to/your/venv/folder. This command creates a venv folder in the specified path
3. After this, we need to install the libraries: pyotp, pyzbar, pyinstaller. Rest are pre-installed
4. Copy and  paste the files into your folder.
5. Now after checking if the code works fine, we convert the code into application using pyinstaller library
6. Open cmd where your project is and use command: pyinstaller --onefile nameofyour.pyfile
7. two folders build and dist, one spec file will be created
8. The application will be in the dist folder. Perform these steps for both the files
--------- ---------
Note: In the code I have named my folder as PROJECT and the keys and passwords are stored in the OP folder.
The application creates the folder while saving the keys/passwrods, if it shows error then create the folder in the dist folder where the .exe file is present
--------- ---------
Note: When we open the application it asks for password in cmd and then opens the gui application, 
this functionality is in the usb_authenticator.py code which is imported in both the code files (otp and password)
--------- ---------
Note: When we run the otp application, it might show the pyzbar library error in the cmd. For that we need to manually add the dll of pyzbar.
Open the .spec file of otp application and add this lines:
- from PyInstaller.utils.hooks import collect_dynamic_libs
- // List of DLLs to include
- binaries = collect_dynamic_libs('pyzbar')
- // And in a = Analysis([])
- change binaries=[] to binaries=binaries

By modifying the spec file above, rebuild the application. To rebuild, open cmd where the spec file is and type: pyinstaller nameofspec.spec. This will rebuild the app with neccessary changes.And the application will work without errors.

In further development, i want to add qrcode functionality where the user does not need to enter the shared-key manually, the qrcode feature will directly capture the shared-key from the qrcode anywhere in the screen
