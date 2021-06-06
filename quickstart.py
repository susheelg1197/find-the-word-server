import json
import random
abcd={'range': 'sentences!A1:AF1000', 'majorDimension': 'ROWS', 'values': [['title', 'category', 'kind', 'difficulty', 'Option1', 'Option2', 'Option3', 'Option4', 'Option5', 'Option6', 'Option7', 'Option8', 'Option9', 'Answer1', 'Answer2', 'Answer3', 'explanation'], ['abc *dash* xyz ', 'GRE', 'single ', '3', 'a', 'b', 'c', 'd', 'g', 'f', '', '', '', '0', '1'], ['qwe *dash* xyz ', 'GRE', 'multiple', '2', 'a', 'b', 'c', 'd', 'e', '', '', '', '', '0'], ['try *dash* xyz ', 'GRE', 'multiple', '1', 'a', 'b', 'c', 'd', 'e', 'f', '', '', '', '0', '1'], ['ghj *dash* xyz ', 'GRE', 'multiple', '3', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', '0', '1', '2']]}



list1=[]
for i in range(1,len(abcd['values'])):
    dictionary={}
    answers=[]
    resolution=[]
    
    for j in range(0,len(abcd['values'][i])):
        if j>3 and j<13:
            answers.append({'content':abcd['values'][i][j]})
            dictionary['answers']=answers
        elif j>12 and j<16:
            resolution.append(int(abcd['values'][i][j]))
            dictionary['resolution']=resolution
        else:
            dictionary[abcd['values'][0][j]]=abcd['values'][i][j]
    list1.append(dictionary)

random.shuffle(list1) # to shuffle the list in a random order
answer=json.dumps(list1)
print(answer)