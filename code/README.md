## Getting Started

create an enviroment with `python 3.8`

```
git clone https://github.com/tanyuqian/knowledge-harvest-from-lms.git 

```

Then install the required packages:

```
pip install -r requirements.txt

```
in case of an error durinng the installation change the package number of fire to 0.5.0 


make a change to the data_utils.py by changing the language of the stop words to german. Before running the scripts run this code in your enviroment:

```python
>>> import nltk
>>> nltk.download('stopwords')
```

extend the german stopwords in `data_utils.py` with the following keywords to improve the results: <br>
```python
stopwords = stopwords.words('german')
stopwords.extend(['zwischen','seit jahren', 'hierfür', 'heute', 'dafür', 'jedoch', 'ebenfalls', 'schließlich', 'bisher', 'hauptsächlich', 'selber', 'bereits', 'primär', 'allerdings', 'allein', 'dabei'])
```

also in the gpt3.py change the prompt to "paraphrase in German". <br>
after specifying the initial prompts and five seed samples, the script would generate the paraphrased prompts. Those can be found in the relation_info folder. Further changes can be made to the json files, for instance, adding the few shots in the prompts. <br>

### Further pre-training

in the same enviroment as above the sctipt train.py. In the script the paths to the train and val set should be specified, as well as the paths to save the model and the tokenizer. Moreover, a WandB project can be added to track the progress of training.

### Web scraping

The German cardiology guidelines were downloaded from the internet. They were only in the pdf format available. Converting a pdf file to a txt file introducing many issues with the spacing better individual characters or words. Since manual correction would have be very time consuming, GPT-3.5 API was used to go through the text and fix the issues in the text files. The script can be found in `dgk_conversion.ipynb` notebook. 

### GPT-4 post-processing filtering step

The BERTnet output a large number of entity pairs per relation. This number sometimes goes up to 500 pairs. Unfortunately not all of the pairs are correct and manually picking out the pairs is too time consuming. An option could be to set a threshold that only takes the top number of pairs, however, because these relations require very precise entities, the threshold has to be set very high and thus resulting in only 4-10 entity pairs per relation. To increase the number of correct enitity pairs that are extracted a post-processing step has been introduced that utilized GPT-4 API and filtered the full output list and removed the wrong pairs based on its knowledge.
