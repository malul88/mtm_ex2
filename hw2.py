

def countCompetitors(competitors, competition):
    counter = 0
    for i in range(len(competitors)):
        if competitors[i]["competition name"] == competition:
            counter += 1
    return counter


def winnersSortTimed(competitors, competition, start, end):
    winning_countries = [str(competition), "undef_country", "undef_country", "undef_country"]
    counter = 1
    for i in range(start, end):
        if counter > 3:
            break
        winning_countries[counter] = competitors[i]["competitor country"]
        counter += 1
    return winning_countries


def winnersSortUntimed(competitors, competition, start, end):
    winning_countries = [str(competition), "undef_country", "undef_country", "undef_country"]
    counter = 1
    for i in range(end - 1, start - 1, -1):
        if counter > 3:
            break
        winning_countries[counter] = competitors[i]["competitor country"]
        counter += 1
    return winning_countries


def printCompetitor(competitor):
    """
    Given the data of a competitor, the function prints it in a specific format.
    Arguments:
        competitor: {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country,
                        'result': result}
    """
    competition_name = competitor['competition name']
    competition_type = competitor['competition type']
    competitor_id = competitor['competitor id']
    competitor_country = competitor['competitor country']
    result = competitor['result']

    assert (isinstance(result, int))  # Updated. Safety check for the type of result

    print(
        f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


def printCompetitionResults(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country, winning_silver_country, winning_bronze_country] if
                 country != undef_country]
    print(f'The winning competitors in {competition_name} are from: {countries}')


def key_sort_competitor(competitor):
    """
    A helper function that creates a special key for sorting competitors.
    Arguments:
        competitor: a dictionary contains the data of a competitor in the following format:
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country,
                        'result': result}
    """
    competition_name = competitor['competition name']
    result = competitor['result']
    return (competition_name, result)


def checkForCheaters(competitors_in_competitions, competition_names):
    sorted_list = sorted(competitors_in_competitions, key=key_sort_competitor)
    sum_of_competitors = 0
    for competition in competition_names.keys():
        competitors_id = []
        num_of_competitors = countCompetitors(sorted_list, competition)
        deleted = 0
        for i in range(sum_of_competitors, sum_of_competitors + num_of_competitors):
            competitors_id.append(sorted_list[i]["competitor id"])
            competitors_id.sort()
        if len(competitors_id) >= 2:
            for j in range(len(competitors_id) - 1):
                if competitors_id[j] == competitors_id[j + 1]:
                    k = sum_of_competitors
                    counter = 0
                    while counter < num_of_competitors:
                        if k >= len(sorted_list):
                            break
                        if sorted_list[k]["competitor id"] == competitors_id[j]:
                            sorted_list.remove(sorted_list[k])
                            deleted += 1
                            counter += 1
                            continue
                        counter += 1
                        k += 1
        sum_of_competitors += num_of_competitors - deleted
    return sorted_list

def readParseData(file_name):
    """
    Given a file name, the function returns a list of competitors.
    Arguments:
        file_name: the input file name. Assume that the input file is in the directory of this script.
    Return value:
        A list of competitors, such that every record is a dictionary, in the following format:
            {'competition name': competition_name, 'competition type': competition_type,
                'competitor id': competitor_id, 'competitor country': competitor_country,
                'result': result}
    """
    competitors = []
    competitors_in_competitions = []

    f = open(file_name, 'r')
    for line in f:
        split_line = line.split()
        if split_line[0] == "competitor":
            competitors.append(split_line[1])
            competitors.append(split_line[2])
        else:
            dict_competitions = {
                "competition name": split_line[1],
                "competitor id": split_line[2],
                "competition type": split_line[3],
                "result": int(split_line[4])
            }
            competitors_in_competitions.append(dict_competitions)
    for temp_dict in competitors_in_competitions:
        competitor_id = temp_dict["competitor id"]
        temp_dict["competitor country"] = competitors[competitors.index(competitor_id) + 1]


    return competitors_in_competitions


def calcCompetitionsResults(competitors_in_competitions):
    """
    Given the data of the competitors, the function returns the champs countries for each competition.
    Arguments:
        competitors_in_competitions: A list that contains the data of the competitors
                                    (see readParseData return value for more info)
    Retuen value:
        A list of competitions and their champs (list of lists).
        Every record in the list contains the competition name and the champs, in the following format:
        [competition_name, winning_gold_country, winning_silver_country, winning_bronze_country]
    """
    competitions_champs = []
    #  creating a dictionary of competition names and their type
    competition_names = {}
    for temp_dict in sorted(competitors_in_competitions, key=key_sort_competitor):
        if temp_dict["competition name"] in competition_names:
            continue
        competition_names[temp_dict["competition name"]] = [temp_dict["competition type"]]
    #  check if there's a cheater and delete him
    sorted_list = checkForCheaters(competitors_in_competitions, competition_names)
    #  rank the winners countries
    sum_of_competitors = 0
    for comp_name, comp_type in competition_names.items():
        num_of_competitors = countCompetitors(sorted_list, comp_name)
        if comp_type == ['timed'] or comp_type == ['knockout']:
            competitions_champs.append(winnersSortTimed(sorted_list, comp_name, sum_of_competitors,
                                                        sum_of_competitors + num_of_competitors))
        else:
            competitions_champs.append(winnersSortUntimed(sorted_list, comp_name, sum_of_competitors,
                                                          sum_of_competitors + num_of_competitors))

        sum_of_competitors += num_of_competitors
    return competitions_champs


def partA(file_name='input.txt', allow_prints=True):
    # read and parse the input file
    competitors_in_competitions = readParseData(file_name)
    if allow_prints:
        # competitors_in_competitions are sorted by competition_name (string) and then by result (int)
        for competitor in sorted(competitors_in_competitions, key=key_sort_competitor):
            printCompetitor(competitor)

    # calculate competition results
    competitions_results = calcCompetitionsResults(competitors_in_competitions)
    if allow_prints:
        for competition_result_single in sorted(competitions_results):
            printCompetitionResults(*competition_result_single)

    return competitions_results


def partB(file_name='input.txt'):
    competitions_results = partA(file_name, allow_prints=False)
    import Olympics
    olympic = Olympics.OlympicsCreate()
    for lists in competitions_results:
        Olympics.OlympicsUpdateCompetitionResults(olympic, str(lists[1]), str(lists[2]), str(lists[3]))
    Olympics.OlympicsWinningCountry(olympic)
    Olympics.OlympicsDestroy(olympic)


if __name__ == "__main__":
    """
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.

    To run only a single part, comment the line below which corresponds to the part you don't want to run.
    """
    file_name = 'input.txt'

    partA(file_name)
    partB(file_name)
