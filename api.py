

from collections import defaultdict
import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt

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

def plot_histograma_sub_rotina(min_hist, max_hist, histogram_data):

    bin_edges = np.arange(min_hist , max_hist,  np.floor((max_hist - min_hist) / 5))
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
    plt.savefig('histograma_rtt_' + str(min_hist) + '.png')
    plt.show()

def plot_histograma(rtt):
    histogram_data = defaultdict(int)

    for entry in rtt:
        for key, value in entry["val"].items():
            histogram_data[float(key)] += value

    min_hist = min(histogram_data.keys()) - 1
    max_hist = max(histogram_data.keys()) - 1
    half_hist = max_hist / 2

    plot_histograma_sub_rotina(min_hist, half_hist, histogram_data)
    
    plot_histograma_sub_rotina(half_hist, max_hist, histogram_data)
 
