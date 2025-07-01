import os
import sys
import importlib

VALID_MODES = ["streamlit"]


def runcommand(cmd):
    os.system(cmd)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else None
    if mode not in VALID_MODES:
        print("Usage: python localdev.py [fastapi|streamlit]")
        sys.exit()

    runcommand("pip install python-dotenv")
    runcommand("pip install black")
    from dotenv import load_dotenv

    load_dotenv()
    os.environ["OS_DEV_MODE"] = "true"
    print("Env injected.")
    answer = input("Reinstall app libs? ")
    match answer:
        case "y":
            runcommand("pip install -r requirements.txt")
        case _:
            pass
    answer = input("Reinstall Octostar libs? ")
    match answer:
        case "y":
            runcommand("pip uninstall -y octostar-python-client")
            runcommand("pip uninstall -y streamlit-octostar-research")
            runcommand("pip uninstall -y streamlit-octostar-utils")
            runcommand("pip cache purge")
            download_endpoint = os.environ["OS_API_ENDPOINT"]
            runcommand(
                f"pip install {download_endpoint}/api/octostar/meta/octostar-python-client.tar.gz"
            )
            runcommand("pip install streamlit-octostar-research")
            runcommand("pip install streamlit-octostar-utils")
        case _:
            pass
    from octostar.client import impersonating_launching_user, dev_mode

    @impersonating_launching_user()
    @dev_mode(os.getenv("OS_DEV_MODE"))
    def start_app(client):
        if mode == "streamlit":
            print("Starting Streamlit app...")
            from streamlit.web.bootstrap import run

            run(
                main_script_path="src/main.py",
                is_hello=False,
                args=[
                    "--server.port=8080",
                    "--server.address=0.0.0.0",
                    "--server.enableCORS=true",
                    "--browser.gatherUsageStats=false",
                ],
                flag_options={},
            )

    start_app()
