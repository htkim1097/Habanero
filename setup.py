from cx_Freeze import setup, Executable
from os import path

app_root = path.dirname(path.abspath(__file__)) + "\\"
img_path = app_root + "images\\"
 
exe = [Executable('App.py')]
 
setup(
    name='Threads',
    version='1.0',
    author='me',
    options = {
        "build_exe" : {
            "packages" : ['threading','time','tkinter','PIL','os','socket','Color','Msg','Config','copy','datetime','base64','io'],
            "include_files" : [img_path, app_root + "Config.py", app_root + "Color.py", app_root + "Msg.py"]
        }
        
    },
    executables = exe
)