import os
import urllib.request
import zipfile
import shutil
import time
from subprocess import Popen


Empty_Paella_master_directory = os.getcwd()
Empty_Paella_directory = Empty_Paella_master_directory+"\\Empty-Paella-updates"
Empty_Paella_file = Empty_Paella_directory+"\\main\\main.exe"
Empty_Paella_rev = Empty_Paella_directory+"\\Rev.txt"


def installation():
    print("*** Downloading new version ***")
    urllib.request.urlretrieve("https://gitlab.devtools.intel.com/ianimash/Empty-Paella/-/archive/updates/Empty-Paella-updates.zip", Empty_Paella_master_directory+"\\Empty-Paella_new.zip")
    print("*** Extracting new version ***")
    zip_ref = zipfile.ZipFile(Empty_Paella_master_directory+"\\Empty-Paella_new.zip", 'r')
    zip_ref.extractall(Empty_Paella_master_directory)
    zip_ref.close()
    os.remove(Empty_Paella_master_directory+"\\Empty-Paella_new.zip")
    time.sleep(5)
    
def upgrade():    
    print("*** Removing old files ***")
    shutil.rmtree(Empty_Paella_directory)
    time.sleep(10)
    installation()


def main(autoinstall=0):
    ### Is Empty-Paella already installed? If yes get file size to compare for upgrade
    if os.path.isfile(Empty_Paella_file):
        local_file_size = int(os.path.getsize(Empty_Paella_rev))
        # print(local_file_size)
        ### Check if update needed:
        f = urllib.request.urlopen("https://gitlab.devtools.intel.com/ianimash/Empty-Paella/-/raw/updates/Rev.txt") # points to the exe file for size
        i = f.info()
        web_file_size = int(i["Content-Length"])
        # print(web_file_size)
        if local_file_size != web_file_size:# upgrade available
            if autoinstall:
                print("*** New upgrade available! Upgrading now *** ")
                upgrade()
            else:
                updt = input("*** New upgrade available! enter <y> to upgrade now, other key to skip upgrade *** ")
                if updt == "y": # proceed to upgrade
                    upgrade()
                elif updt == "Y":
                    upgrade()
    ### Empty-Paella wasn't installed, so we download and install it here                
    else:
        if autoinstall:
            print("*** Installing Empty-Paella for the first time ***")
            installation()
        else:
            install = input("Welcome to Empty-Paella! If you enter <y> Empty-Paella will be downloaded in the same folder where this file is.\nAfter the installation, this same file you are running now (\"Empty-Paella.exe\") will the one to use to open Empty-Paella :)\nEnter any other key to skip the download\n -->")
            if install == "y":
                installation()
            elif install == "Y":
                installation()
    print('Ready')
    ### We open the real application:
    try:
        Popen(Empty_Paella_file)
        print("*** Opening Empty-Paella ***")
        if not autoinstall:
            time.sleep(20)
    except:
        print('Failed to open application, Please open manually in subfolder')
        pass


def main_with_autoinstall():
    main(autoinstall=1)

if __name__ == "__main__":
    main()
