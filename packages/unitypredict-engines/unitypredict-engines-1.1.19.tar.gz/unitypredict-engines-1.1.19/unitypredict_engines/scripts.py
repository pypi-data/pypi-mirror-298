import sys, os, shutil
from .unitypredictcli import UnityPredictCli
from .unitypredictUtils import ReturnValues as Ret
import argparse

def main():
    cliExec = "UnityPredict SDK"
    parser = argparse.ArgumentParser(
            description="Welcome to {}".format(cliExec)
    )
   
    parser.add_argument("--configure", action="store_true", help=f"configure the credentials of {cliExec}")
    parser.add_argument("--list_profiles", action="store_true", help=f"show credentials configured for {cliExec}")
    parser.add_argument("-e", "--engine", action="store_true", help=f"Access the engine specific operations in {cliExec}")
    parser.add_argument("-c", "--create", default=None, help="""create the AppEngine with a name. 
                                                                            Used after the [-e][--engine]""")
    parser.add_argument("-r", "--remove", default=None, help="""remove the AppEngine. 
                                                                            Used after the [-e][--engine]""")
    parser.add_argument("-rn", "--run", default=None, help="""run the AppEngine locally. 
                                                                            Used after the [-e][--engine]""")
    parser.add_argument("-d", "--deploy", default=None, help="""deploy the AppEngine to UnityPredict. 
                                                                            Used after the [-e][--engine]""")

    args = parser.parse_args()

    num_args = len(sys.argv) - 1
    
    if (num_args == 0):
        parser.print_help()
        sys.exit(0)

    cliDriver = UnityPredictCli()

    if args.configure:
        inputApiKey = input("Enter your UnityPredict account API Key: ")
        inputApiKey = inputApiKey.strip()
        ret = cliDriver.configureCredentials(uptApiKey=inputApiKey)
        sys.exit(0)

    if args.list_profiles:
        cliDriver.showProfiles()
        sys.exit(0)

    if args.engine:
        
        if args.create != None:
            ret = cliDriver.createEngine(engineName=args.create)
            if ret == Ret.ENGINE_CREATE_ERROR:
                cliDriver.removeEngine(engineName=args.create)
                print (f"Removing Engine {args.create} due to Engine Creation errors!")
            sys.exit(0)

        elif args.remove != None:
            ret = cliDriver.removeEngine(engineName=args.remove)
            if ret == Ret.ENGINE_REMOVE_SUCCESS:
                print(f"Removed the engine {args.remove} Successfully!!")
            elif ret == Ret.ENGINE_REMOVE_ERROR:
                print(f"Engine {args.remove} not detected!!")
            sys.exit(0)
        
        elif args.run != None:

            print (f"Run engine: {args.run}")
            cliDriver.runEngine(engineName=args.run)
        
        elif args.deploy != None:
            print (f"Deploy {args.deploy}")
            sys.exit(0)

        else:
            print ("Incomplete arguements present. Please check the help section for the usage")
            parser.print_help()
        sys.exit(0)
    


