from api import *

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
   
plot_histograma(rtt2)