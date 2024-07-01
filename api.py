

from collections import defaultdict
import random
import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt

def etapa1(origem, dst, interface, event, time_range, bw_target_bandwidth=None):
    if bw_target_bandwidth:
        url = f"http://monipe-central.rnp.br/esmond/perfsonar/archive/?source=monipe-{origem}-{interface}.rnp.br&destination=monipe-{dst}-{interface}.rnp.br&event-type={event}&time-range={time_range}&bw-target-bandwidth={bw_target_bandwidth}"
    else: url = f"http://monipe-central.rnp.br/esmond/perfsonar/archive/?source=monipe-{origem}-{interface}.rnp.br&destination=monipe-{dst}-{interface}.rnp.br&event-type={event}&time-range={time_range}"

    try:
        return requests.get(url, verify=False).json()[0]['metadata-key']
    except:
        return None

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

def plot_histograma_sub_rotina(min_hist, max_hist, histogram_data, divisions, origin, destiny, plot, save):

    bin_edges = np.linspace(min_hist, max_hist, divisions + 1)
    bin_labels = [f"{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}" for i in range(len(bin_edges)-1)]
    binned_data = {label: 0 for label in bin_labels}

    for value, frequencia in histogram_data.items():
        for i in range(len(bin_edges) - 1):
            if bin_edges[i] <= value < bin_edges[i + 1]:
                binned_data[bin_labels[i]] += frequencia
                break

    df = pd.DataFrame(list(binned_data.items()), columns=['Intervalo', 'frequencia'])
    df = df.sort_values('Intervalo')

    plt.figure(figsize=(10, 6))
    plt.bar(df['Intervalo'], df['frequencia'], align='center')
    plt.xlabel('Value Intervalos')
    plt.ylabel('frequencia')
    plt.title('Histograma rtt')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    if save:
        plt.savefig(f'histograma_rtt_{origin}_{destiny}_{min_hist}.png')
    if plot:
        plt.show()

def plot_histograma(rtt, origin, destiny, plot=True, save=False):
    histogram_data = defaultdict(int)

    for entry in rtt:
        for key, value in entry["val"].items():
            histogram_data[float(key)] += value

    min_hist = min(histogram_data.keys()) - 1
    max_hist = max(histogram_data.keys()) - 1
    half_hist = max_hist / 2

    plot_histograma_sub_rotina(half_hist, max_hist, histogram_data, 7, origin, destiny, plot, save)
    plot_histograma_sub_rotina(min_hist, half_hist, histogram_data, 7, origin, destiny, plot, save)

def states_2by2():

    estados = ['ac', 'al', 'ap', 'am', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mt', 'ms', 'mg', 'pa', 'pb', 'pr', 'pe', 'pi', 'rj', 'rn', 'rs', 'ro', 'rr', 'sc', 'sp', 'se', 'to']
    for x in range (0,len(estados)):
        for y in range (1, len(estados)):
            if x != y:
                print(f'{estados[x]} -> {estados[y]}')
                sent = etapa1(estados[x], estados[y], "atraso", "packet-count-sent", "84600")
                duplicate = etapa1(estados[x], estados[y], "atraso", "packet-duplicates", "84600")
                rtt = etapa1(estados[x], estados[y], "atraso", "histogram-rtt", "84600")
                loss_rate = etapa1(estados[x], estados[y], "atraso", "packet-loss-rate", "84600")

                if (sent == None or duplicate == None or rtt == None or loss_rate == None):
                    continue
                
                sent2 = etapa2(sent, "packet-count-sent")
                duplicate2 = etapa2(duplicate, "packet-duplicates")
                rtt2 = etapa2(rtt, "histogram-rtt")
                loss_rate2 = etapa2(loss_rate, "packet-loss-rate")
                arrival_rate = arrival(loss_rate2, sent2, duplicate2)
                waiting_time = waiting(rtt2)
                service_time = waiting_time/(1+arrival_rate * waiting_time)
                utilizacao = arrival_rate * service_time
                packet_number = utilizacao / (1- utilizacao)
                print(f'waiting_time: {waiting_time}')
                print(f'arrival: {arrival_rate}')
                print(f'service_time: {service_time}')
                print(f'service_rate: {1/service_time}')
                print(f'utilizacao: {utilizacao}')
                print(f'packet_number: {packet_number}')
                plot_histograma(rtt2, estados[x], estados[y],False, True)
                print('------------------------------------------------------------')

 
