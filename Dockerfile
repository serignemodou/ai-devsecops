FROM python:3.12-slim

RUN apt-get update && apt-get install -y wget
RUN wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.50.0_Linux-64bit.deb
RUN dpkg -i trivy_0.50.0_Linux-64bit.deb

WORKDIR /app
COPY src/ai_image_scanner/agent.py .

RUN pip install requests

ENTRYPOINT ["python", "agent.py"]