FROM python:3.10
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN apt-get update && apt-get install -y ca-certificates
RUN pip install --no-cache-dir --upgrade -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]