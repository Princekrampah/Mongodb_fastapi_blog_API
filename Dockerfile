FROM python:3.9.12

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# this is to help prevent installing requirements everytime we update our
# source code, this is cause docker has a caching system.
COPY . .

# uvicorn app.main:app --host 0.0.0.0 --port 8000 
CMD [ "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000" ]
