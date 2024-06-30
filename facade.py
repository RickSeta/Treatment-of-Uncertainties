from api import *
import urllib3 as url

def treatment_as_queue(origin, destination, plot=False):

#origin = input("Insira o código do estado de origem que deseja analisar\n")
#destination = input("Insira o código do estado de destino que deseja analisar\n")
#-----------------------------------------------------------------------------------------------------

    url.disable_warnings()
    time_window = "84600"

    sent = etapa1(origin, destination, "atraso", "packet-count-sent", time_window)

    duplicate = etapa1(origin, destination, "atraso", "packet-duplicates", time_window)

    rtt = etapa1(origin, destination, "atraso", "histogram-rtt", time_window)

    loss_rate = etapa1(origin, destination, "atraso", "packet-loss-rate", time_window)

    #-----------------------------------------------------------------------------------------------------
    if (sent != None and duplicate != None and rtt != None and loss_rate != None):

        sent2 = etapa2(sent, "packet-count-sent")

        duplicate2 = etapa2(duplicate, "packet-duplicates")

        rtt2 = etapa2(rtt, "histogram-rtt")

        loss_rate2 = etapa2(loss_rate, "packet-loss-rate")

        #-----------------------------------------------------------------------------------------------------
        arrival_rate = arrival(loss_rate2, sent2, duplicate2)

        waiting_time = waiting(rtt2)

        service_time = waiting_time/(1 + arrival_rate * waiting_time)

        utilizacao = arrival_rate * service_time

        packet_number = arrival_rate * waiting_time



        #-----------------------------------------------------------------------------------------------------
        
        if (plot):
            print(f'waiting_time: {waiting_time}')
            print(f'arrival: {arrival_rate}')
            print(f'service_time: {service_time}')
            print(f'service_rate: {1/service_time}')
            print(f'utilizacao: {utilizacao}')
            print(f'packet_number: {packet_number}')
            plot_histograma(rtt2)
        
        return {
            "waiting_time" : waiting_time,
            "arrival" : arrival_rate,
            "service_time" : service_time,
            "service_rate" : 1/service_time,
            "utilizacao" : utilizacao,
            "packet_number" : packet_number
        }
    else:
        return None