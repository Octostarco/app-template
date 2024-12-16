import os
from dotenv import load_dotenv
from octostar.client import impersonating_launching_user, dev_mode

def runcommand(cmd):
    try:
        os.system(cmd)
    except Exception as e:
        print(e)

def inject_env():
    load_dotenv()
    os.environ['OS_DEV_MODE'] = 'true'
    print("Env injected.")

inject_env()

@impersonating_launching_user()
@dev_mode(os.getenv('OS_DEV_MODE'))
def start_app(client):
    runcommand("python main.py")
    #runcommand("streamlit run streamlit_app.py")

if __name__ == '__main__':
    while True:
        answer = input("Reinstall libs? ")
        match answer:
            case "y":
                runcommand("pip uninstall -y octostar-python-client")
                runcommand("pip uninstall -y streamlit-octostar-research")
                runcommand("pip uninstall -y streamlit-octostar-utils")
                runcommand("pip cache purge")
                download_endpoint = os.environ["OS_API_ENDPOINT"] 
                runcommand(f"pip install {download_endpoint}/api/octostar/meta/octostar-python-client.tar.gz")
                runcommand("pip install streamlit-octostar-research")
                runcommand("pip install streamlit-octostar-utils")
                break
            case _:
                break
    start_app()
    
