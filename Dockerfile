FROM python:3.11
RUN useradd welbex
RUN mkdir -p /usr/src/app/welbex/
WORKDIR /usr/src/app/welbex
COPY . /usr/src/app/welbex/
COPY .env /usr/src/app/welbex/
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --without dev --no-root
RUN chmod +x /usr/src/app/welbex/boot.sh
ENTRYPOINT ["./boot.sh"]
EXPOSE 8000