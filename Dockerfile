FROM python:3.10.12-slim-bookworm
RUN pip install PyYAML==6.0.2
RUN pip install ipdb==0.13.13
RUN pip install requests==2.32.3
RUN pip install rdflib==7.1.1
RUN pip install veld_spec==24.12.18
ENV PYTHONPATH=/app/
