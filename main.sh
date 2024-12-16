#!/bin/sh
# Example main file
. ./build.sh
pip install "${OS_API_ENDPOINT}/api/octostar/meta/octostar-python-client.tar.gz"

# Your entrypoint here
#streamlit run --server.port 8501 --server.address 127.0.0.1 --server.enableCORS true --server.fileWatcherType none streamlit_app.py
python main.py