# knowledge-graph-extraction-from-llms

## Introduction

Knowledge graphs can be a great tool to leverage information, more specifically healthcare data, that can lead to improved clinical decision-making, enhanced
research capabilities, and optimized healthcare delivery, this can be achieved by integrating patient-specific data with medical knowledge.
However, most knowledge graphs are manually created, might not fit all tasks and are mostly in English. Thus, most graphs can be rather costly to construct and they are not applicable to German data. Recently, language models like BERT have been shown to encode a large amount of knowledge implicitly in their parameters. Hao et al. 2022 harvested symbolic Knowledge Graphs from the LMs and proposed a framework for automatic KG construction. However, this approach has thus far only been tested on non-medical
English data. Therefore, this thesis project aims to evaluate the potential of language models as a source for harvesting medical knowledge in German.

### Researh Questions 

Q1. Can German clinical knowledge be extracted from pre-trained language models? <br>
Q2. What is the level of accuracy achieved by the resulting Knowledge Graph, and which data and models exhibit the highest performance? <br>
Q3. What is the best evaluation strategy? <br>


## Data 

The following table contains some statistics about the 

| Name           | Number of Tokens | Number of Documents | Domain      |
|-----------------|-----------------|-----------------|-----------------|
| GGPONC         | 1,877,100        | 30              | Oncology        |
| BRONCO150      | 70,572           | 150             | Oncology        | 
| DKG            | ToDO             | 128             | Cardiology      | 
| CARDIO.de      | 993,143          | 500             | Cardiology      |
| MieDEEP        | 977,504          | 500             | Cardiology      | 


## Methods

BERTNet: Harvesting Knowledge from the LMs (Hao et al. 2022)
This paper proposes an automated framework to extract a Knowledge Graph from pre-trained LMs such as BERT or RoBERTa. The framework derives knowledge of new relation types and entities, independent of existing knowledge bases or corpora. The study investigates the knowledge capacity of different models, revealing that larger models encode more knowledge. Improved pre-training strategies enhance the quality of learned and stored knowledge.

### Prompt Engineering



## Experiments

### Models 

- gBERT-base 
- gBERT-large
- medBERT.de
- xml-roBERTa 


### Experimental setup
Four sets of extractions: 
- models taken from hugging face, 
- further pre-trained models 
- further pre-trained models + contextualized prompts
- further pre-trained models + few-shot learning prompts

## Results 


## Evaluation 
- ground truth relations extracted from cardio.de 
- SNOMED CT ontologies 
- giving known correct pairs as input and evaluting the output probability 

## References

Hao et al. 2022
Socrates 2022
Bressem et al. 2023 
Devlin et al. 2019
