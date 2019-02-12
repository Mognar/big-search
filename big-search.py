
# coding: utf-8

# In[16]:


from flask import Flask, request, render_template
app = Flask(__name__)


#This bit imports the necessary code packages to run this program
import json
import requests
import itertools


# In[ ]:


@app.route("/")
def hello(): 
    return render_template('index.html')

@app.route('/resultpage', methods=['POST'])
def my_form_post():
    TermToSearch = request.form['Term']
    ExcludeTopicTerms = request.form['TPGAvoid']
#Replace "Housing" with whichever term you would like to search on. 
#Please make sure the term is in quotes
#If you would like Topic terms left out, leave ExcludeTopicTerms as 1, if you want to look for them, set this to 0.
#TermToSearch = "Members"
#ExcludeTopicTerms = 0
#Once you've changed the term in the box above, go to the top of the page and Click Cell > Run All. This will run the program and produce your search string at the end of the page.


    #This bit puts the term into a search on data.parliament.uk
    if ExcludeTopicTerms == 1:
        slug = "http://eldaddp.azurewebsites.net/terms.json?prefLabel={}&maxEx-attribute=TPG".format(TermToSearch)
    else:
        slug = "http://eldaddp.azurewebsites.net/terms.json?prefLabel={}".format(TermToSearch)
    print(slug)
    r=requests.get(slug)
    #If this works, the following line should output the full text of the 
    #data.parliament.uk page on your term of choice.
    print(r.text)




    #This part reads the json code of the term you searched for. 
    j=json.loads(r.text)
    if j['result']['totalResults'] == 0:
        print('No terms found, please try another term')
    else:
        if j['result']['items'][0]['isPreferred']['_value'] == "false":
            terminfo = j['result']['items'][0]['exactMatch']['_about']
        else:
            terminfo = j['result']['items'][0]['_about']
        termname = j['result']['items'][0]['prefLabel']['_value']

    #This is the part that does the heavy lifting. 
    #The code here finds the preferred name and ID number of each term under your
    #chosen term. 
    #It then looks to see if the child terms of your chosen term have any children. 
    #If it does, it pulls out the name and ID of that term too. 
    #The term names are all printed below.
    #This is the part that does the heavy lifting. 
    #The code here finds the preferred name and ID number of each term under your
    #chosen term. 
    #It then looks to see if the child terms of your chosen term have any children. 
    #If it does, it pulls out the name and ID of that term too. 
    #The term names are all printed below.
    ids = []
    terms = []
    terms.append(termname)
    bing = terminfo.split("/")[4]
    ids.append(bing)
    termjson = terminfo + '.json'
    tj = requests.get(termjson)
    j2 = json.loads(tj.text)
    try:
        j3 = j2['result']['primaryTopic']['narrower']
        print(j3)
        for i in j3:
            try:
                termbits = (i['prefLabel']['_value'])
                terms.append(termbits)
            except TypeError:
                termbits = (j3['prefLabel']['_value'])
                terms.append(termbits)
            try:
                jsnoos = i['_about']
            except TypeError:
                jsnoos = j3['_about']  
            jbing = jsnoos.split("/")[4]
            ids.append(jbing)
            try:
                j4 = i['_about']
            except TypeError:
                j4 = j3['_about']
            j5 = j4 + '.json'
            j6 = requests.get(j5)
            j7 = json.loads(j6.text)
            try:
                j8 = j7['result']['primaryTopic']['narrower']
                for i in j8:
                    try:
                        termbits1 = (i['prefLabel']['_value'])
                        terms.append(termbits1)
                    except TypeError:
                        termbits1 = (j8['prefLabel']['_value'])
                        terms.append(termbits1)
                    try:
                        ksnoos = i['_about']
                    except TypeError:
                        ksnoos = j8['_about']  
                    kbing = ksnoos.split("/")[4]
                    ids.append(kbing)
                    try:
                        k4 = i['_about']
                    except TypeError:
                        k4 = j8['_about']
                    k5 = k4 + '.json'
                    k6 = requests.get(k5)
                    k7 = json.loads(k6.text)
                    try:
                        k8 = k7['result']['primaryTopic']['narrower']
                        for i in k8:
                            try:
                                termbits2 = (i['prefLabel']['_value'])
                                terms.append(termbits2)
                            except TypeError:
                                termbits2 = (k8['prefLabel']['_value'])
                                terms.append(termbits2)
                            try:
                                lsnoos = i['_about']
                            except TypeError:
                                lsnoos = k8['_about']  
                            lbing = lsnoos.split("/")[4]
                            ids.append(lbing)
                            try:
                                l4 = i['_about']
                            except TypeError:
                                l4 = k8['_about']
                            l5 = l4 + '.json'
                            l6 = requests.get(l5)
                            l7 = json.loads(l6.text)
                            try:
                                l8 = l7['result']['primaryTopic']['narrower']
                                for i in l8:
                                    termbits3 = (l8['prefLabel']['_value'])
                                    terms.append(termbits3)
                            except: "KeyError"
                            pass
                    except: "KeyError"
                    pass
            except: "KeyError"
            pass
    except: "KeyError"
    pass

    #This part takes all of the IDs and puts them into a text string, with "OR" 
    #in between each ID. This will output a text string that can be copied into 
    #Parliamentary Search. 
    #
    #You can change the paramters of the search below, or change them in Search.

    def remove_duplicates(values):
        output = []
        seen = set()
        for value in values:
            # If value has not been encountered yet,
            # ... add it to both list and set.
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output

    # Remove duplicates from this list.
    result = remove_duplicates(ids)
    numofterms = len(result)
    termlist = remove_duplicates(terms)
    if numofterms > 200:
        halflist = int(len(result)/2 + 1)
        def chunks(l, n):
        # For item i in a range that is a length of l,
            for i in range(0, len(l), n):
            # Create an index range for l of n items:
                yield l[i:i+n]

        
        stringchunks = list(chunks(result, halflist))
        string = []
        for f in stringchunks:
            stringy = '+OR+'.join(f)
            if j['result']['items'][0]['class'] == "":
                if j['result']['items'][0]['attribute'] == "TPG":
                    strings = 'https://search.parliament.uk/search?q=topic_ses:('+stringy+")+session:17/19"
                    string.append(strings)
                else:
                    strings = 'https://search.parliament.uk/search?q=subject_ses:('+stringy+")+session:17/19"
                    string.append(strings)
            elif j['result']['items'][0]['class'] == "TPG":
                strings = 'https://search.parliament.uk/search?q=topic_ses:('+stringy+")+session:17/19"
                string.append(strings)
            else:
                strings = 'https://search.parliament.uk/search?q=subject_ses:('+stringy+")+session:17/19"
                string.append(strings)
    else:
        stringy = '+OR+'.join(result)
        if j['result']['items'][0]['class'] == "":
            if j['result']['items'][0]['attribute'] == "TPG":
                string = 'https://search.parliament.uk/search?q=topic_ses:('+stringy+")+session:17/19"
            else:
                string = 'https://search.parliament.uk/search?q=subject_ses:('+stringy+")+session:17/19"
        elif j['result']['items'][0]['class'] == "TPG":
            string = 'https://search.parliament.uk/search?q=topic_ses:('+stringy+")+session:17/19"
        else:
            string = 'https://search.parliament.uk/search?q=subject_ses:('+stringy+")+session:17/19"

    return render_template('resultpage.html', string = string, numofterms = numofterms, termtosearch = TermToSearch, termsandids = zip(result,termlist))
if __name__ == "__main__":
  app.debug = True
  app.run(port=5006, use_reloader=False)

