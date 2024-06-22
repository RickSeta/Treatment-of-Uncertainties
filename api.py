

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