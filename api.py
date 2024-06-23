

import requests


def etapa1(origem, dst, interface, event, time_range, bw_target_bandwidth=None):
    if bw_target_bandwidth:
        url = f"http://monipe-central.rnp.br/esmond/perfsonar/archive/?source=monipe-{origem}-{interface}.rnp.br&destination=monipe-{dst}-{interface}.rnp.br&event-type={event}&time-range={time_range}&bw-target-bandwidth={bw_target_bandwidth}"
    else: url = f"http://monipe-central.rnp.br/esmond/perfsonar/archive/?source=monipe-{origem}-{interface}.rnp.br&destination=monipe-{dst}-{interface}.rnp.br&event-type={event}&time-range={time_range}"

    return requests.get(url, verify=False).json()[0]['metadata-key']




def etapa2(uri, interface=""):
    uri = f"http://monipe-central.rnp.br/esmond/perfsonar/archive/{uri}/{interface}/base"
    return requests.get(uri, verify=False).json()

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

def waiting(rtt):
    sum_rtt = 0

    for element in rtt:
        # O formato é quantidade de tempo(key) : quantos ocorreram durante aquele tempo
        # (Por ser um histograma)
        # logo, é necessário fazer uma média ponderada
        sum_val = 0
        val = element["val"]
        sum_key = 0
        for key in list(val.keys()):
            sum_val += float(key) * val[key]
            sum_key += val[key]
        sum_rtt += sum_val/sum_key

    return sum_rtt/len(rtt)
#-----------------------------------------------------------------------------------------------------

sent = etapa1("sp", "rj", "atraso", "packet-count-sent", "84600")

duplicate = etapa1("sp", "rj", "atraso", "packet-duplicates", "84600")

rtt = etapa1("sp", "rj", "atraso", "histogram-rtt", "84600")

loss_rate = etapa1("sp", "rj", "atraso", "packet-loss-rate", "84600")

#-----------------------------------------------------------------------------------------------------

sent2 = etapa2(sent, "packet-count-sent")

duplicate2 = etapa2(duplicate, "packet-duplicates")

rtt2 = etapa2(rtt, "histogram-rtt")

loss_rate2 = etapa2(loss_rate, "packet-loss-rate")

#-----------------------------------------------------------------------------------------------------
arrival_rate = arrival(loss_rate2, sent2, duplicate2)

waiting_time = waiting(rtt2)

service_time = waiting_time/(1+arrival_rate * waiting_time)

utilizacao = arrival_rate * service_time

packet_number = utilizacao / (1- utilizacao)


# print(f'waiting_time: {waiting_time}')
# print(f'arrival: {arrival_rate}')
# print(f'service_time: {service_time}')
# print(f'service_rate: {1/service_time}')
# print(f'utilizacao: {utilizacao}')
# print(f'packet_number: {packet_number}')

#-----------------------------------------------------------------------------------------------------

