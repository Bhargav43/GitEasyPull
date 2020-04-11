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