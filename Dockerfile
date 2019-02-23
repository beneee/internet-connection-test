FROM python:3.7.2

RUN pip install speedtest-cli
RUN pip install requests
RUN pip install schedule

RUN mkdir results

COPY run_speedtest.py /

CMD [ "python", "./run_speedtest.py" ]
