# App Template
This is a python-oriented template for app developers. New apps developed in python should follow this template.

## Usage Instructions
* Create a new app repository and use this repo as a template.
* Under `.github/workflows/tag.yml`, change `my-app` to your new app name (alias).
* Under `.env.example`, add any environment secrets that your app needs in order to run for local development.
* Under `build.sh`, add any build instructions that should be executed when creating a new image for this app.
* Under `main.sh`, add any launch instructions that should be executed when the image is booting up.
    * You will likely want to also adjust `localdev.py` to add those commands to the `start_app()` method.
    * For multi-server applications (e.g. streamlit + fastapi), you will want to add `nginx` and concat the servers, e.g.:
        ```
        streamlit run --server.port 8501 --server.address 127.0.0.1 --server.enableCORS true --server.fileWatcherType none src/streamlit_app.py &
        python -m src.fastapi_app &
        nginx -g 'daemon off;' -c $(pwd)/nginx.conf
        ```
* Under `.vscode/launch.json`, specify all the modes with which local development can launch the app.
    * If there are multiple servers to this app (e.g. streamlit + fastapi), it is good practice to keep them as separate launch commands
* Under `Dockerfile`, change the base image, if needed.
    * In most cases, you'll want either `octostar/streamlit-apps-gpu` or `octostar/streamlit-apps-no-gpu`
* Under `.python-version`, change the expected python version for this application. Note that this may be fixed depending on the base docker image used to build this application.
    * `octostar/streamlit-apps-gpu` -> 3.10
    * `octostar/streamlit-apps-no-gpu` -> 3.11
* Under `manifest.yaml`, add the app image, alias, secrets schema, and any other manifest-related configs.
* Finally, modify the `README.md` to document your application and make it easier to share, use, and maintain.

Following is the typical `README.md` format that app developers should complete to describe the application, what it does and how to use it.

# ⬛ App Title
Two-three sentences slogan for the app.

## Features
Dotted list of the main app features.

## Installation (app version)
Concise install guide for production, including required app secrets. Conclude with how to open the app (e.g. if it has context menu interactions).

## User Guide
User-friendly description of how the app should be opened, on what entities/files it works and what are the main operations/flows that can be performed with it.

## FAQ
Question/Answer pairs to troubleshoot common issues or limitations of the application.

## Developer Guide
Description of the core structure of the app from a developer's point of view; what to do and what not to do when working with the app.

## Known Limitations
List of known bugs, edge cases or missing features under which the app will not work as expected.