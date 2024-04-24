import pip._vendor.requests as requests;
from collections import Counter;

resp = requests.post('http://[::]:9000/?properties={"annotators":"ner,coref","outputFormat":"json"}', data = {'data':'2024 ElectionRFK Jr. candidacy hurts Trump more than Biden, NBC News poll findsThe finding contrasts with a number of other national polls, and it comes amid concerted Democratic efforts to prevent Kennedy from harming Biden’s campaign.Independent presidential candidate Robert F. Kennedy Jr. speaks to supporters on April 13 in West Des Moines, Iowa. Charlie Neibergall / APPrintSaveCreate your free profile or log in to save this articleApril 21, 2024, 1:00 PM UTCBy Mark MurrayThe latest national NBC News poll shows the third-party vote — and especially independent presidential candidate Robert F. Kennedy Jr. — cutting deeper into former President Donald Trump’s support than President Joe Biden’s, though the movement the other candidates create is within the poll’s margin of error.Trump leads Biden by 2 percentage points in a head-to-head matchup, 46% to 44%, in the new NBC News pollYet when the ballot is expanded to five named candidates, Biden is the one with a 2-point advantage: Biden 39%, Trump 37%, Kennedy 13%, Jill Stein 3% and Cornel West 2%.The big reason why is that the poll finds a greater share of Trump voters in the head-to-head matchup backing Kennedy in the expanded ballot. Fifteen percent of respondents who picked Trump the first time pick Kennedy in the five-way ballot, compared with 7% of those who initially picked Biden.Also, Republican voters view Kennedy much more favorably (40% positive, 15% negative) than Democratic voters do (16% positive, 53% negative).“At this stage, [Kennedy’s] appeal looks to be more with Trump than Biden voters,” said Democratic pollster Jeff Horwitt, who conducted the NBC News poll with Republican pollster Bill McInturff.This finding, however, contrasts with the conventional political wisdom — as well as the results of other national polls — suggesting that a bigger third-party vote hurts Biden more.The NBC News poll results on Kennedy’s impact are “different than other surveys,” said McInturff, the GOP pollster. “So there’s always two possibilities: One, it’s an outlier. … Or two, we’re going to be seeing more of this, and our survey is a harbinger of what’s to come.”The Biden campaign has actively tried to peel support away from Kennedy. Most recently, Biden held an event Thursday with members of the Kennedy family who are endorsing the president over their relative.Overall, the party is paying much closer attention to Kennedy than it has to past third-party candidates, mobilizing new super PACs and an arm of the Democratic National Committee focused on reducing the pull of his candidacy.The NBC News poll was conducted April 12-16 of 1,000 registered voters nationwide — 891 contacted via cell phone — and the poll has an overall margin of error of plus-minus 3.1 percentage points.Mark MurrayMark Murray is a senior political editor at NBC News.'}).json();
corefsDict = resp['corefs']
sentencesDict = resp['sentences']

def assess_persons() :
    subject_array = []
    used_indexes = []
    for sent in sentencesDict :

        for i in range(0, len(sent['tokens'])) :
            if i not in used_indexes:
                if (sent['tokens'][i]['ner'] == 'PERSON') and (sent['tokens'][i+1]['ner'] == 'PERSON') and (sent['tokens'][i+2]['ner'] == 'PERSON') and (sent['tokens'][i+3]['ner'] == 'PERSON'):
                    append_target = sent['tokens'][i]['word'] + " " + sent['tokens'][i+1]['word'] + " " + sent['tokens'][i+2]['word'] + " " + sent['tokens'][i+3]['word']
                    subject_array.append(append_target)
                    used_indexes.append(i)
                    used_indexes.append(i+1)
                    used_indexes.append(i+2)
                    used_indexes.append(i+3)
                elif (sent['tokens'][i]['ner'] == 'PERSON') and (sent['tokens'][i+1]['ner'] == 'PERSON') and (sent['tokens'][i+2]['ner'] == 'PERSON'):
                    append_target = sent['tokens'][i]['word'] + " " + sent['tokens'][i+1]['word'] + " " + sent['tokens'][i+2]['word']
                    subject_array.append(append_target)
                    used_indexes.append(i)
                    used_indexes.append(i+1)
                    used_indexes.append(i+2)
                elif (sent['tokens'][i]['ner'] == 'PERSON') and (sent['tokens'][i+1]['ner'] == 'PERSON'):
                    append_target = sent['tokens'][i]['word'] + " " + sent['tokens'][i+1]['word']
                    subject_array.append(append_target)
                    used_indexes.append(i)
                    used_indexes.append(i+1)
                elif (sent['tokens'][i]['ner'] == 'PERSON'):
                    append_target = sent['tokens'][i]['word']
                    subject_array.append(append_target)
                    used_indexes.append(i)
    
    return subject_array

def assess_orgs() :
    subject_array = []
    for sent in sentencesDict :

        for i in range(0, len(sent['tokens'])) :
            if (sent['tokens'][i]['ner'] == 'ORGANIZATION') :
                append_target = sent['tokens'][i]['word']
                if sent['tokens'][i]['ner'] == sent['tokens'][i+1]['ner'] :
                    append_target = sent['tokens'][i]['word'] + " " + sent['tokens'][i+1]['word']
                    if sent['tokens'][i+1]['ner'] == sent['tokens'][i+2]['ner'] :
                        append_target = sent['tokens'][i]['word'] + " " + sent['tokens'][i+1]['word'] + " " + sent['tokens'][i+2]['word']
                subject_array.append(append_target)

    return subject_array

def assess_ideo() :
    subject_array = []
    for sent in sentencesDict :

        for i in range(0, len(sent['tokens'])) :
            if (sent['tokens'][i]['ner'] == 'IDEOLOGY') :
                append_target = sent['tokens'][i]['word']
                if sent['tokens'][i]['ner'] == sent['tokens'][i+1]['ner'] :
                    append_target = sent['tokens'][i]['word'] + " " + sent['tokens'][i+1]['word']
                    if sent['tokens'][i+1]['ner'] == sent['tokens'][i+2]['ner'] :
                        append_target = sent['tokens'][i]['word'] + " " + sent['tokens'][i+1]['word'] + " " + sent['tokens'][i+2]['word']
                subject_array.append(append_target)

    return subject_array

c = Counter(assess_persons())
o = Counter(assess_orgs())
id = Counter(assess_ideo())

c_amended = {}
o_amended = {}
i_amended = {}

for i in c:
    if c[i] > 1:
        c_amended[i] = c[i]

for i in o:
    if o[i] > 1:
        o_amended[i] = o[i]

for i in id:
    if id[i] > 1:
        i_amended[i] = id[i]

c_copy = c_amended.copy()

for i in c_amended:
    i_sorted = set(sorted(i.split()))
    for j in c_amended:
        j_sorted = set(sorted(j.split()))
        if i_sorted & j_sorted and i_sorted != j_sorted:
            c_amended[i] = c_copy[i] + c_copy[j]
print(c_amended)

c_count = Counter(c_amended)
o_count = Counter(o_amended)
i_count = Counter(i_amended)

print("PRIMARY SUBJECT: ", c_count.most_common(1)[0][0])
del c_count[c_count.most_common(1)[0][0]]
for i in c_count:
        print("SECONDARY SUBJECT: ", i)



