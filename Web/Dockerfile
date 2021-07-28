From python:3.7
COPY . .
RUN pip install -r requirements.txt && \
python -m nltk.downloader punkt && \
python -m nltk.downloader stopwords
EXPOSE 5000/tcp
