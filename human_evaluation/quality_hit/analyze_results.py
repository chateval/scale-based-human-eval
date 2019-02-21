import sys
import csv
from itertools import combinations

def read_results(mturk_file):
    mturk_dict = dict()
    with open(mturk_file, 'r', encoding='utf8') as f:
        csvreader = csv.reader(f)
        headers = next(csvreader)
        
        for i, row in enumerate(csvreader):
            mturk_dict[i] = {key: value for key, value in zip(headers, row)}
    return mturk_dict

def calculate_results(mturk_dict, stat_name):
    stat = dict()

    for rowid, row_dict in mturk_dict.items():
        for i in range(1, 6):
            prompt = row_dict["Input.input" + str(i)]
            prompt_id = row_dict["Input.sentid" + str(i)]

            for j in range(1, 6):
                system_name = row_dict["Input.sysid" + str(i) + str(j)][:-2]
                response_id = int(row_dict["Input.sysid" + str(i) + str(j)][-1])
                
                judgment = row_dict["Answer." + stat_name + str(i) + str(j)]
                if judgment == "Yes":
                    judgment = 1
                else:
                    judgment = 0

                try:
                    stat[system_name][prompt_id][response_id].append(judgment)
                except KeyError:
                    try:
                        stat[system_name][prompt_id][response_id] = [judgment]
                    except KeyError:
                        try:
                            stat[system_name][prompt_id] = dict()
                            stat[system_name][prompt_id][response_id] = [judgment]
                        except KeyError:
                            stat[system_name] = dict()
                            stat[system_name][prompt_id] = dict()
                            stat[system_name][prompt_id][response_id] = [judgment]

    ## Calculates average disagreement
    diffs = []
    diff_dist = [0 for i in range(2)]
    for sys_name, prompts in stat.items():
        for prompt_id, responses in prompts.items():
            for response_id, judgments in responses.items():
                if len(judgments) > 1:
                    combs = combinations(list(range(len(judgments))), 2)
                    for c in combs:
                        diffs.append(abs(judgments[c[0]] - judgments[c[1]]))
                        diff_dist[abs(judgments[c[0]] - judgments[c[1]])] += 1

    '''
    try:
        print("Average disagreement: " + str(round(sum(diffs)/len(diffs), 3)))
    except ZeroDivisionError:
        a = 1
    '''

    print("Pairwise Agreement: ")
    try:
        print(diff_dist)
        print([round(d/sum(diff_dist), 3) for d in diff_dist])
        print()
    except ZeroDivisionError:
        a = 1

    systems = sorted(list(stat.keys()))

    ## Calculates average per sentence id
    done = [0 for i in range(len(systems))]
    not_done = [0 for i in range(len(systems))]
    avg_stat = [[] for i in range(len(systems))]
    for sys_name, prompts in stat.items():
        for prompt_id, responses in prompts.items():
            for response_id, judgments in responses.items():
                ## Keeps track of how many sentences are done
                if len('judgments') == 2:
                    done[systems.index(sys_name)] += 1
                else:
                    not_done[systems.index(sys_name)] += 1
                avg_stat[systems.index(sys_name)].append(sum(judgments)/len(judgments))
    ## Calculates overall averages
    avg = [round(sum(s)/len(s), 3) for s in avg_stat]

    #print("DONE: " + str(done))
    #print("NOT DONE: " + str(not_done))

    #print("\nAVERAGES:")
    for i in range(len(systems)):
        print(systems[i] + ": " + str(avg[i]))
    return avg, systems
            
                
            



def main(mturk_file):
    mturk_dict = read_results(mturk_file)

    print("\n## GRAMMAR ##")
    grammar, systems = calculate_results(mturk_dict, 'grammar')
    print("\n## COHERENCE ##")
    means, systems = calculate_results(mturk_dict, 'coherence')
    print("\n## INTERESTING ##")
    simps, systems = calculate_results(mturk_dict, 'interesting')

    print("\n#### OVERALL STATS ####")
    for i in range(len(grammar)):
        print(systems[i] + ": " + str(round(sum([grammar[i], means[i], simps[i]])/3, 2)))


if __name__ == '__main__':
    mturk_file = 'results/Batch_3539631_batch_results.csv'
    main(mturk_file)

'''
python analyze_results_v2.py \
results/Batch_3539631_batch_results.csv
'''
