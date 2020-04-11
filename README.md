# GitEasyPull
## Purpose :bulb:
To Make the Process of Pulling a Git Repo (Any Public Repo on GitHub.com, self or other's) to a local directory on a Windows PC a bit easier.

## Base System's Configurations :wrench:
**Sno.** | **Name** | **Version/Config.**
-------: | :------: | :------------------
1 | Operating System | Windows 10 x64 bit
2 | Python | Version 3.7.0 x64 bit
3 | PyInstaller | Version 3.6
4 | IDE | Pyzo 4.10.2 x64 bit

_Recommendation: Except for Type of OS (Windows), other configurations doesn't matter even if you don't have Python in your system, if you are using the [`executable`](https://github.com/Bhargav43/GitEasyPull/blob/master/GitEasyPull.exe) directly. Try It._

## Mandatory :heavy_exclamation_mark:
**Sno.** | **Requirement** | **Reason**
-------: | :-------------: | :---------
1 | GitHub Account | As the git allows the users to access (pull or clone) the open-source repos of others, a login to registered account is a must.
2 | Git Bash | The Git Bash is a command line intrepretter of Git. This is required as the command in the below program is executed in bash directly in order to avoid slowness of data fetch using web-scrapping.
3 | Internet Connection | This is required is most part of program when it checks whether URL is valid and while pulling the repo to local.

## Imported Modules :package:
Sn | **Module** | **Type** | **Version**
-: | :--------: | :------- | :----------
1 | os | *Built-in* | NA
2 | time | *Built-in* | NA
3 | shutil | *Built-in* | NA
4 | sys | *Built-in* | NA
5 | subprocess | *Built-in* | NA
6 | stat | *Built-in* | NA
7 | requests | *PyPI Installer* | 2.23.0

## [GitEasyPull.py](https://github.com/Bhargav43/GitEasyPull/blob/master/GitEasyPull.py) Code :computer:
```python
import os, time, shutil, sys
from subprocess import Popen, PIPE
import requests
import stat

def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

def ossetup(path, url):
    os.chdir(path)
    repo_name = os.path.split(url)[1] if url[len(url)-1] != '/' else os.path.split(url[:len(url)-1])[1]
    i = 1
    newname = repo_name
    while True:
        try:
            os.mkdir(newname)
            break
        except Exception:
            i+=1
            newname = repo_name+str(i)

    status = gitpull(os.path.join(path, newname), url)

    if not status:
        with open(os.path.join(path, newname)+'\\Notes.txt', 'w') as f:
            content = 'Git Repository Name:\t'+repo_name+'\nRepository URL:\t'+url+'\nClone Timing:\t'+time.strftime('%d-%b-%Y %H:%M:%S')
            f.write(content)
            f.close()
        return False, newname
    else:
        os.chdir(path)
        shutil.rmtree(os.path.join(path, newname), onerror=del_rw)
        return status, -1


def gitpull(path, url):

    try:
        #Initializing
        query = Popen('git init', shell = True, cwd=path, stdout=PIPE, stdin=PIPE)
        status_i, error_i = query.communicate()
        print('\n', status_i.decode('utf-8'))
        query.kill()

        print('*** Please wait!! Pulling the Git Repo May Take a While ***\n')

        #Pulling
        query = Popen('git pull '+url, shell = True, cwd=path, stdout=PIPE, stdin=PIPE)
        status_p, error_p = query.communicate()

    except Exception as e:
        pass

    query.kill()

    if query.returncode == 1:
        print('Network Error. Please check your connection and retry.')
        sys.exit(0)
    elif error_i == error_p == None:
        print(status_p.decode('utf-8'))
        return False
    else:
        if error_i != None:
            return f'Initialization Error: {error_i}'
        else:
            return f'Pulling Error: {error_p}'


def main():
    print('Path to Create Directory in, and pull Repo to...\nExample:\tC:\\Users\\BHARGAV-PC\\Desktop\\Temp')
    while True:
        path = input('Your Path:\t')
        if os.path.exists(path):
            if os.path.isdir(path):
                break
            else:
                print(f'{path} is not a directory. Please re-enter.')
        else:
            print('Invalid Path. Please re-enter.')

    print('\nURL of Repo to Pull from...\nExample:\thttps://github.com/Bhargav43/Sample')
    while True:
        url = input('Your Path:\t')
        if requests.get(url).status_code == 200:
            break
        else:
            print('The URL is either invalid or of a private repo. Please re-enter.')

    status, file = ossetup(path, url)
    if not status:
        print(f'Success!!!\n\nPlease goto << {os.path.join(path, file)} >> for the repo pulled from {url}\n\nPress Any Key to exit.')
    else:
        print(f'{status}')

    input()

if __name__=='__main__':
    main()
```

Haven't added any comments for understanding as it isn't a tough one. Yet you can go thru, and let me know on mails in case if this is useful for you and require clarification/assistance.

## Restricting Conditions :warning:
In order of the flow of control,
#### 1. Local Path Check
_The path of a local directory where the local copy of the git repo is expected, is requested by the program. The built-in module 'os' does the checking for us._
```python
if os.path.exists(path):
    if os.path.isdir(path):
        break
    else:
        print(f'{path} is not a directory. Please re-enter.')
else:
    print('Invalid Path. Please re-enter.')
```

#### 2. URL Check
_The program checks whether the URL provided is valid and is accessable. The pypi module ['requests'](https://pypi.org/project/requests/) does the checking for us._
```python
if requests.get(url).status_code == 200:
    break
else:
    print('The URL is either invalid or of a private repo. Please re-enter.')
```

#### 3. Path's End Char Check
_Usually in laguage like Py, the folder's path ending with a '/' character represents the file/folder inside the present is selected. Here, we want to create a new folder inside the present by default. So, eliminating the extra character so it causes no effect._
```python
os.path.split(url)[1] if url[len(url)-1] != '/' else os.path.split(url[:len(url)-1])[1]
```

#### 4. Existing Folder Restriction
_The duplicate folder name issue is quite common. So, we append a serial digit at the end of the folder name._
```python
while True:
    try:
        os.mkdir(newname)
        break
    except Exception:
        i+=1
        newname = repo_name+str(i)
```

#### 5. Git Commands Issue
_If there would be an issue with the git commands, the created directory, the .git init directory (if successfully gets created) and the additionally created Notes.txt file will automatically be removed with the help of shutil.rmtree() function_ 
##### 5.1. Initializing Errors
_The errors which are returned during the subprocess.Popen().communicate() of 'git init' command's execution._
##### 5.2. Pulling Errors
_The errors which are returned during the subprocess.Popen().communicate() of 'git pull URL' command's execution._
```python
elif error_i == error_p == None:
    print(status_p.decode('utf-8'))
    return False
else:
    if error_i != None:
        return f'Initialization Error: {error_i}'
    else:
        return f'Pulling Error: {error_p}'
```

#### 6. Network Issue
_As the git bash's commands are through the internet, the network breakdown may cause them to stop the pulling in-between which would be an issue. Hence the connection is checked_
```python
if query.returncode == 1:
    print('Network Error. Please check your connection and retry.')
    sys.exit(0)
```

## Sample Output :bar_chart:
```
Path to Create Directory in, and pull Repo to...
Example:        C:\Users\BHARGAV-PC\Desktop\Temp
Your Path:      C:\Users\BHARGAV-PC\Desktop\Temp

URL of Repo to Pull from...
Example:        https://github.com/Bhargav43/Sample
Your Path:      https://github.com/Bhargav43/BackupFiles

 Initialized empty Git repository in C:/Users/BHARGAV-PC/Desktop/Temp/BackupFiles2/.git/

*** Please wait!! Pulling the Git Repo May Take a While ***

remote: Enumerating objects: 57, done.
remote: Counting objects: 100% (57/57), done.
remote: Compressing objects: 100% (54/54), done.
remote: Total 57 (delta 30), reused 12 (delta 2), pack-reused 0
Unpacking objects: 100% (57/57), 5.10 MiB | 437.00 KiB/s, done.
From https://github.com/Bhargav43/BackupFiles
 * branch            HEAD       -> FETCH_HEAD

Success!!!

Please goto << C:\Users\BHARGAV-PC\Desktop\Temp\BackupFiles2 >> for the repo pulled from https://github.com/Bhargav43/BackupFiles

Press Any Key to exit.
```

### Executable File :floppy_disk:
_Executable is aslo called freezing since the file works just great in change of confguration of base system or even after removing python as well. The file be used for distribution with ease and without dependencies. Following is the commands I used for the same. [Click here](https://github.com/Bhargav43/GitEasyPull/blob/master/Freezing%20Notes.txt) for logs related to it._

#### Creating Specifications file :page_facing_up:

```
pyi-makespec --onefile --hidden-import=os --hidden-import=time --hidden-import=shutil --hidden-import=sys --hidden-import=stat --hidden-import=subprocess --hidden-import=requests --icon="H:\Projects\Python Related Stuff\Pyzo Projects\GitEasyPull\Gitpull-icon.ico" --specpath="H:\Projects\Python Related Stuff\Pyzo Projects\GitEasyPull" GitEasyPull.py
```

This has created [BacupFiles.spec](https://github.com/Bhargav43/GitEasyPull/blob/master/GitEasyPull.spec) as follows,
```
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['GitEasyPull.py'],
             pathex=['H:\\Projects\\Python Related Stuff\\Pyzo Projects\\GitEasyPull'],
             binaries=[],
             datas=[],
             hiddenimports=['os', 'time', 'shutil', 'sys', 'stat', 'subprocess', 'requests'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='GitEasyPull',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='H:\\Projects\\Python Related Stuff\\Pyzo Projects\\GitEasyPull\\Gitpull-icon.ico')
```

#### Creating Executable :arrow_forward:

PyPI `Pyinstaller 3.6` was used for creating the executable in PIP environment. Command as follows,
```
pyinstaller --onefile --hidden-import=os --hidden-import=time --hidden-import=shutil --hidden-import=sys --hidden-import=stat --hidden-import=subprocess --hidden-import=requests --icon="H:\Projects\Python Related Stuff\Pyzo Projects\GitEasyPull\Gitpull-icon.ico" --specpath="H:\Projects\Python Related Stuff\Pyzo Projects\GitEasyPull" GitEasyPull.py
```
Which has created me a working executable model as below.

### Finally, the Working Model :metal:

Click for accessing [GitEasyPull.exe](https://github.com/Bhargav43/GitEasyPull/blob/master/GitEasyPull.exe)

# Farewell! :tada::tada:
