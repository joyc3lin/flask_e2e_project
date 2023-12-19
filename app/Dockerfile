# pull a specific version of python from the docker hub
FROM python:3.10-slim-buster
# creating new virtual OS 
WORKDIR /app
# puts files in directory and places it in virtual OS
COPY . /app/
# installs requprements.txt file
RUN pip install -r requirements.txt
# exposes port 5000 to virtual OS to enable communication
EXPOSE 5000
# run command to run web application
CMD ["python", "app.py"]