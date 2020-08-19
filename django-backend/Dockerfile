FROM python

ENV PYTHONUNBUFFERED 1

RUN pip install pipenv
COPY Pipfile Pipfile.lock /
RUN pipenv install
COPY . /

CMD ["pipenv","run","python","manage.py","runserver","0.0.0.0:9000"]