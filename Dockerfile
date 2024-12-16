FROM octostar/streamlit-apps-gpu:latest

WORKDIR /app

RUN apt-get update && apt-get install -y python3-venv
RUN python3 -m venv /app/venv

COPY . /app
RUN chmod +x build.sh
RUN source /app/venv/bin/activate && ./build.sh

ENTRYPOINT ["/bin/bash", "-c", "source /app/venv/bin/activate && /app/main.sh"]

EXPOSE $CODE_SERVER_PORT

