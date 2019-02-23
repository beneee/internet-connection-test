#!/usr/bin/python

import json
from datetime import date, datetime, timezone
from pathlib import Path
import speedtest
import requests
import sys
import schedule
import time

def writeResultsToFile(file_prefix, test_results):
  today = str(date.today())
  filename = "./results/" + file_prefix + "-results-" + today + ".json"

  # create file if it does not exist
  Path(filename).touch(exist_ok=True)

  with open(filename, 'r+') as log_file:
    file_contents = log_file.read()
    if file_contents == '':
      file_contents = '[]'
    content = json.loads(file_contents)
    content.append(test_results)
    log_file.seek(0)
    log_file.write(json.dumps(content))
    log_file.truncate()

def runSpeedtest():
  servers = [15874]
  s = speedtest.Speedtest()
  s.get_servers(servers)
  s.get_best_server()
  s.download()
  s.upload()
  results_dict = s.results.dict()
  print(results_dict)
  writeResultsToFile("speedtest", results_dict)

def runHttpRequest(url):
  result = { "url": url }
  try:
    r = requests.get(url)
    result["status"] = r.status_code
  except BaseException as err:
    #print(str(err))
    ex_type, ex_value = sys.exc_info()
    result["error"] = {
      "type": ex_type.__name__,
      "message": ex_value
    }
  return result

def runIpv4Ipv6Test():
  results = []
  results.append(runHttpRequest('https://www.google.de/'))
  results.append(runHttpRequest('https://www.unitymedia.de/'))
  
  ipv4Ipv6Results = {
    "timestamp": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
    "results": results
  }
  print(ipv4Ipv6Results)
  writeResultsToFile("ipv4-ipv6-test", ipv4Ipv6Results)

# schedule ipv4ipv6 test
schedule.every().minute.at(":00").do(runIpv4Ipv6Test)

# schedule speedtest
schedule.every().hour.at(":00").do(runSpeedtest)
schedule.every().hour.at(":15").do(runSpeedtest)
schedule.every().hour.at(":30").do(runSpeedtest)
schedule.every().hour.at(":45").do(runSpeedtest)

while True:
  schedule.run_pending()
  time.sleep(1)
