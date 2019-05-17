def main():
    results_norm = ''
    with open('results.txt', 'r') as f:
        for line in f:
            one_keyword_result = line.strip().split(', ')

            keyword = one_keyword_result[0]

            # make dict out of list, alternating key and value
            i = iter(one_keyword_result[1:])
            res_dict = dict(zip(i, i))
            for keys in res_dict:
                res_dict[keys] = float(res_dict[keys])
            res_dict = normalize_dict_values(res_dict, target=100)

            results_norm += keyword
            for key, value in sorted(res_dict.items(), key=lambda item: item[1], reverse=False):
                results_norm += ', ' + str(key) + ', ' + str(value)

            results_norm += '\n'

    with open('results_norm.txt', 'w') as r:
        r.write(results_norm)


def normalize_dict_values(d, target=1.0):
    factor = target / sum(d.values())
    return {key: value*factor for key, value in d.items()}


if __name__ == '__main__':
    main()
