FROM postgres:17

ENV POSTGRES_USER=fiap
ENV POSTGRES_PASSWORD=Postgres2022!
ENV POSTGRES_DB=fiap_soat

VOLUME /var/lib/postgresql/data

EXPOSE 5432

CMD ["postgres"]
