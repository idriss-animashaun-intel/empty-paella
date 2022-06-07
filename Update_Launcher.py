import os
import urllib.request
import zipfile
import shutil
import time


Empty_Paella_directory = os.getcwd()
Empty_Paella_file = Empty_Paella_directory+"\\Empty-Paella.exe"
Old_Empty_Paella_directory = Empty_Paella_directory+"\empty-paella_exe-master"

proxy_handler = urllib.request.ProxyHandler({'https': 'http://proxy-dmz.intel.com:912'})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)


def installation():
    urllib.request.urlretrieve("https://github.com/idriss-animashaun-intel/empty-paella/archive/refs/heads/master.zip", Empty_Paella_directory+"\empty-paella_luancher_new.zip")
    print("*** Updating Launcher Please Wait ***")
    zip_ref = zipfile.ZipFile(Empty_Paella_directory+"\empty-paella_luancher_new.zip", 'r')
    zip_ref.extractall(Empty_Paella_directory)
    zip_ref.close()
    os.remove(Empty_Paella_directory+"\empty-paella_luancher_new.zip")

    src_dir = Empty_Paella_directory + "\empty-paella-master"
    dest_dir = Empty_Paella_directory
    fn = os.path.join(src_dir, "Empty-Paella.exe")
    shutil.copy(fn, dest_dir)

    shutil.rmtree(Empty_Paella_directory+"\empty-paella-master")

    time.sleep(5)
    
def upgrade():
    print("*** Updating Launcher Please Wait ***")    
    print("*** Removing old files ***")
    time.sleep(20)
    os.remove(Empty_Paella_file)
    time.sleep(10)
    installation()


### Is Empty_Paella already installed? If yes get file size to compare for upgrade
if os.path.isfile(Empty_Paella_file):
    local_file_size = int(os.path.getsize(Empty_Paella_file))
    # print(local_file_size)

    url = 'https://github.com/idriss-animashaun-intel/empty-paella/raw/master/Empty-Paella.exe'
    f = urllib.request.urlopen(url)

    i = f.info()
    web_file_size = int(i["Content-Length"])
    # print(web_file_size)

    if local_file_size != web_file_size:# upgrade available
        upgrade()

### Empty_Paella wasn't installed, so we download and install it here                
else:
    installation()

if os.path.isdir(Old_Empty_Paella_directory):
        print('removing Empty_Paella_exe-master')
        time.sleep(5)
        shutil.rmtree(Old_Empty_Paella_directory)

print('Launcher up to date')