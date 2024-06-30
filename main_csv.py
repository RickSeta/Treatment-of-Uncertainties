import facade as fa
import csv as csv


pops = [ "ac", "al", "am", "ap", "ba", "ce", "df", "es", "go", "ma", "mg", "ms", "mt", "pa", "pb", "pe", 
    "pi", "pr", "rj", "rn", "ro", "rr", "rs", "sc", "se", "sp", "to" ]

deduced_num_of_lines = len(pops)*(len(pops) - 1)
count = 0
with open("pops_as_queues.csv", "w", newline='') as csvfile:
    field_names = ["conexao", "tempo de espera (ms)", "taxa de chegada(pkts/ms)", "tempo de servico (ms)", "taxa de atendimento (pkts/ms)", "utilizacao", "numero de pacotes"]
    writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=";")
    writer.writeheader()
    for i in pops:
        filtered_pops = filter(lambda p: p != i, pops)
        for j in filtered_pops:
            count += 1
            print(f"{count} of {deduced_num_of_lines}:  {i} -> {j}")
            data = fa.treatment_as_queue(i, j)
            if data != None:
                writer.writerow({
                    "conexao" : f"{i} -> {j}",
                    "tempo de espera (ms)" : str(data["waiting_time"]).replace('.',','),
                    "taxa de chegada(pkts/ms)" : str(data["arrival"]).replace('.',','),
                    "tempo de servico (ms)" : str(data["service_time"]).replace('.',','),
                    "taxa de atendimento (pkts/ms)" : str(data["service_rate"]).replace('.',','),
                    "utilizacao" : str(data["utilizacao"]).replace('.',','),
                    "numero de pacotes" : str(data["packet_number"]).replace('.',','),
            })
