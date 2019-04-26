import datetime
import json
from collections import defaultdict

dict1, dict2, dict3, dict4, dict5 = defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(
    int), defaultdict(int)
map_list = [{}, dict1, dict2, dict3, dict4, dict5]

import glob

mylist = [f for f in glob.glob('*.json')]
print(mylist)

for inputfile in mylist:

    visited = set()
    with open(inputfile) as f:
        for line in f:
            data = (json.loads(line))
            posix_time = data['unixReviewTime']
            rating = int(data['overall'])
            date = datetime.datetime.utcfromtimestamp(posix_time).strftime('%Y-%m-%d')

            visited.add(date)
            map_list[rating][date] += 1

    final_dict = defaultdict()

    for dt in visited:
        list = [map_list[rating][dt] for rating in range(1, 6)]
        final_dict[dt] = list

    from collections import OrderedDict

    ordered = OrderedDict(sorted(final_dict.items(), key=lambda t: t[0]))
    # print(ordered)

    with open('timeline_' + inputfile, 'w') as fp:
        json.dump(ordered, fp)
