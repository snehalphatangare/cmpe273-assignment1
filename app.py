from flask import Flask
app = Flask(__name__)

import base64
import sys
import github

from sys import argv
from github import Github

def readFileContents(repoPath,fileName):
    try :
        #Get the name of repository from url
        #Get last index of character /
        lastBackSlashIndex= repoPath.rfind("/")
        repoName = repoPath[lastBackSlashIndex+1:]
        #Get the github username from url
        secondLastBackSlashIndex=repoPath.rfind("/",0,lastBackSlashIndex)
        userName = repoPath[secondLastBackSlashIndex+1:lastBackSlashIndex]
        #print "***username="+ userName
                
        g = Github()
        r = g.get_user(userName).get_repo(repoName) 
                
        file_contents=r.get_file_contents(fileName)
        #print "file_contents", base64.b64decode(file_contents.content)
        return base64.b64decode(file_contents.content)
    except github.GithubException, exception:
        #FALLBACK
        #If an exception occurs during access to Github then get the configurations from the local github repository
        try:
            backupFilePath= "/home/snehal/cmpe273-assignment1/"+fileName
            backupConfigFile = open(backupFilePath)
            return backupConfigFile.read()
        except:
            return "Unexpected error..Sorry for inconvenience"
    except:
        return "Unexpected error:", sys.exc_info()[0]

@app.route("/v1/<fileName>")
def getConfigurations(fileName):
    script,repoURL = argv
    return readFileContents(repoURL,fileName)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')