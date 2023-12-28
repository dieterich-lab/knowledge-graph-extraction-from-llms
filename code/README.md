## Getting Started

create an enviroment with `python 3.8`

```
git clone https://github.com/tanyuqian/knowledge-harvest-from-lms.git 

```

Then install the required packages:

```
pip install -r requirements.txt

```
in case of an error durinng the installation change the package number. or use the requirements txt from this repo that has been used for this project. 


make a change to the data_utils.py by changing the language of the stop words to german. Before running the scripts run this code in the enviroment:

```python
>>> import nltk
>>> nltk.download('stopwords')
```


also in the gpt3.py change the prompt to "paraphrase in German". <br>
after specifying the initial prompts and five seed samples, the script would generate the paraphrased prompts. Those can be found in the relation_info folder. Further changes can be made to the json files, for instance, adding the demonstartions in the prompts. <br>

### Further pre-training

in the same enviroment as above the sctipt train.py. In the script the paths to the train and val set should be specified, as well as the paths to save the model and the tokenizer. Moreover, a WandB project can be added to track the progress of training.

