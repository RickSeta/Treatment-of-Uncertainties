

import requests


def etapa1(origem, dst, interface, event, time_range, bw_target_bandwidth=None):
    if bw_target_bandwidth:
        url = f"http://monipe-central.rnp.br/esmond/perfsonar/archive/?source=monipe-{origem}-{interface}.rnp.br&destination=monipe-{dst}-{interface}.rnp.br&event-type={event}&time-range={time_range}&bw-target-bandwidth={bw_target_bandwidth}"
    else: url = f"http://monipe-central.rnp.br/esmond/perfsonar/archive/?source=monipe-{origem}-{interface}.rnp.br&destination=monipe-{dst}-{interface}.rnp.br&event-type={event}&time-range={time_range}"

    return requests.get(url, verify=False).json()[0]['metadata-key']

sent = etapa1("sp", "rj", "atraso", "packet-count-sent", "84600")
duplicate = etapa1("sp", "rj", "atraso", "packet-duplicates", "84600")
rtt =etapa1("sp", "rj", "atraso", "histogram-rtt", "84600")
loss_rate = etapa1("sp", "rj", "atraso", "packet-loss-rate", "84600")



def etapa2(uri, interface=""):
    uri = f"http://monipe-central.rnp.br/esmond/perfsonar/archive/{uri}/{interface}/base"
    return requests.get(uri, verify=False).json()

sent2 = etapa2(sent, "packet-count-sent")

duplicate2 = etapa2(duplicate, "packet-duplicates")

rtt2 = etapa2(rtt, "histogram-rtt")

loss_rate2 = etapa2(loss_rate, "packet-loss-rate")


def arrival(losses, sent, duplicate, time_window=84600):
    sum_loss = 0
    sum_sent = 0
    sum_duplicate = 0
    for element in losses:
        sum_loss += element["val"]
    
    for x in range(len(sent)):
        sum_sent += sent[x]["val"]

    for y in range(len(duplicate)):
        sum_duplicate += duplicate[y]["val"]

    prob_arrival = 1 - (sum_loss/len(losses))
    arrival = prob_arrival * (sum_sent-sum_duplicate)/time_window
    return arrival

print(arrival(loss_rate2, sent2, duplicate2))

# 1711459620, 'val': 10.0}, {'ts': 1711460011, 'val': 10.0}, {'ts': 1711460375                  {'ts': 1711931837, 'val': 10.0}, {'ts': 1711932250, 'val': 10.0}, {'ts': 1711932367, 'val': 10.0}]
