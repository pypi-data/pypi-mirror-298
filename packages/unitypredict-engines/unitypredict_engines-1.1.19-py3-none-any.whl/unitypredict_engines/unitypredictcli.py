import os, json, shutil, subprocess
import requests
from .unitypredictUtils import ReturnValues as Ret
from .UnityPredictLocalHost import UnityPredictLocalHost

class UnityPredictCli:
    def __init__(self) -> None:

        self._uptCredFolder = ".unitypredict"
        self._uptCredFile = "credentials"
        self._userRoot = os.path.expanduser("~")
        self._uptCredDir = os.path.join(self._userRoot, self._uptCredFolder)
        self._uptCredPath = os.path.join(self._uptCredDir, self._uptCredFile)

        # self._uptEntryPointAPI = "https://api.dev.unitypredict.net/api/engines/supportedengines"
        self._uptEntryPointAPI = "https://api.prod.unitypredict.com/api/engines/supportedengines"
        self._uptEntryPointFieName = "EntryPoint.py"

        self._uptBasePlatformName = "SL_CPU_BASE_PYTHON_3.12"
        self._uptLocalMainFileName = "main.py"
        
        # Get API key
        self._uptApiKeyDict = {}
        if os.path.exists(self._uptCredPath):
            with open(self._uptCredPath) as credFile:
                self._uptApiKeyDict = json.load(credFile)
            

    # Private Unitl Functions

    def _fetchEntryPointTemplate(self, apiKey : str, uptProfile: str = "default"):

        print ("Fetching EntryPoint.py template ...")
        headers = {"Authorization": f"Bearer {apiKey}"}
        response = requests.get(self._uptEntryPointAPI, headers=headers)
        if response.status_code != 200:
            print (f"EntryPoint.py template fetch Failure with error code: {response.status_code}")
            print(response.text)
            return Ret.ENGINE_CREATE_ERROR
        
        try:
            suppPlatforms = response.json()
            for suppPlatform in suppPlatforms:
                if suppPlatform["platformKey"] != self._uptBasePlatformName:
                    continue

                entrypointResp = requests.get(suppPlatform["entryPointTemplateUrl"])
                if entrypointResp.status_code != 200:
                    print (f"EntryPoint.py template fetch Failure with error code: {entrypointResp.status_code}")
                    print(entrypointResp.text)
                    return Ret.ENGINE_CREATE_ERROR
                

                entrypointContent = entrypointResp.text
                entryPointFile = os.path.join(os.getcwd(), self._uptEntryPointFieName)

                with open(entryPointFile, "w+")as efile:
                    efile.write(entrypointContent)

                break

        except Exception as e:
            print (f"Exception Occured while fetching EntryPoint: {e}")
            return Ret.ENGINE_CREATE_ERROR
        
        print ("EntryPoint.py template fetch Success!!")
        
        return Ret.ENGINE_CREATE_SUCCESS
    
    def _generateMainFile(self):

        mainFileContent = r"""
from unitypredict_engines import UnityPredictLocalHost
from unitypredict_engines import ChainedInferenceRequest, ChainedInferenceResponse, FileReceivedObj, FileTransmissionObj, IPlatform, InferenceRequest, InferenceResponse, OutcomeValue
import EntryPoint

if __name__ == "__main__":

    
    platform = UnityPredictLocalHost()

    testRequest = InferenceRequest()
    # User defined Input Values
    testRequest.InputValues = {} 
    results: InferenceResponse = EntryPoint.run_engine(testRequest, platform)

    # Print Outputs
    if (results.Outcomes != None):
        for outcomKeys, outcomeValues in results.Outcomes.items():
            print ("\n\nOutcome Key: {}".format(outcomKeys))
            for values in outcomeValues:
                infVal: OutcomeValue = values
                print ("Outcome Value: \n{}\n\n".format(infVal.Value))
                print ("Outcome Probability: \n{}\n\n".format(infVal.Probability))
    
    # Print Error Messages (if any)
    print ("Error Messages: {}".format(results.ErrorMessages))

        """

        try:
            MAIN_FILE_PATH = os.path.join(os.getcwd(), self._uptLocalMainFileName)
            with open(MAIN_FILE_PATH, "w+") as mainf:
                mainf.write(mainFileContent)
        except Exception as e:
            print (f"Exception occured while generating main file: {e}")
            return Ret.ENGINE_CREATE_ERROR
        
        print ("Main file generation Success!!")
        return Ret.ENGINE_CREATE_SUCCESS


    # Binding functions with CLI Flags
    def configureCredentials(self, uptApiKey: str| None, uptProfile: str = "default"):

        if not os.path.exists(self._uptCredDir):

            os.mkdir(self._uptCredDir)
            
        self._uptApiKeyDict[uptProfile] = {
                "UPT_API_KEY": uptApiKey
            }
        
        try:
            with open(self._uptCredPath, "w+") as credFile:
                credFile.write(json.dumps(self._uptApiKeyDict, indent=4))
        except Exception as e:
            print (f"Error in creating file {self._uptCredPath}: {e}")
            return Ret.CRED_CREATE_ERROR
        
        return Ret.CRED_CREATE_SUCCESS
    
    def showProfiles(self):
        
        print ("Credential Profiles: ")
        for keys in self._uptApiKeyDict.keys():
            print(f"{keys}")

    def findEngine(self, engineName: str, uptProfile: str = "default"):
        currPath = os.getcwd()
        enginePath = os.path.join(currPath, engineName)

        if os.path.exists(enginePath):
            return Ret.ENGINE_FOUND
        else:
            return Ret.ENGINE_NOT_FOUND

    
    def createEngine(self, engineName: str, uptProfile: str = "default"):
        
        ret = self.findEngine(engineName=engineName)

        if ret == Ret.ENGINE_FOUND:
            print ("""The engine already exists on the current directory. You can:
                - Change the directory
                - Use [-c][--create] flag to change the name of the engine
                """)
            return ret

        
        currPath = os.getcwd()
        enginePath = os.path.join(currPath, engineName)
        
        # Make Engine Path
        os.mkdir(enginePath)
        
        # Change dir to enginePath
        os.chdir(enginePath)

        
        apiKey = self._uptApiKeyDict[uptProfile]["UPT_API_KEY"]
        print ("Creating Engine Components ...")
        initEngine = UnityPredictLocalHost(apiKey=apiKey)
        
        if not initEngine.isConfigInitialized():
            print ("Engine Components creation Failed!!")
            # Change dir back to parent of enginePath    
            os.chdir(currPath)
            return Ret.ENGINE_CREATE_ERROR

        print ("Engine Components creation Success!!")
        
        # Fetch the entrypoint details
        ret = self._fetchEntryPointTemplate(apiKey=apiKey)
        if ret == Ret.ENGINE_CREATE_ERROR:
            # Change dir back to parent of enginePath    
            os.chdir(currPath)
            return ret
        
        # Generate main file
        ret = self._generateMainFile()
        if ret == Ret.ENGINE_CREATE_ERROR:
            # Change dir back to parent of enginePath    
            os.chdir(currPath)
            return ret
        
        # Change dir back to parent of enginePath    
        os.chdir(currPath)    
        return Ret.ENGINE_CREATE_SUCCESS
    
    def removeEngine(self, engineName: str, uptProfile: str = "default"):

        ret = self.findEngine(engineName=engineName)

        if ret == Ret.ENGINE_FOUND:
            enginePath = os.path.join(os.getcwd(), engineName)
            shutil.rmtree(enginePath)
            return Ret.ENGINE_REMOVE_SUCCESS
        else:
            return Ret.ENGINE_REMOVE_ERROR
    
    def runEngine(self, engineName: str, uptProfile: str = "default"):

        ret = self.findEngine(engineName=engineName)

        if ret == Ret.ENGINE_FOUND:
            enginePath = os.path.join(os.getcwd(), engineName)
            mainFile = os.path.join(enginePath, self._uptLocalMainFileName)
            subprocess.run(["python", mainFile])
        else:
            print (f"Engine {engineName} not found. Could not run engine!!")

            



