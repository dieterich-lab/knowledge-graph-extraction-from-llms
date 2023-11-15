# knowledge-graph-extraction-from-llms

## Introduction

Knowledge graphs can be a great tool to leverage information, more specifically healthcare data, that can lead to improved clinical decision-making, enhanced
research capabilities, and optimized healthcare delivery, this can be achieved by integrating patient-specific data with medical knowledge.
However, most knowledge graphs are manually created, might not fit all tasks and are mostly in English. Thus, most graphs can be rather costly to construct and they are not applicable to German data. Recently, language models like BERT have been shown to encode a large amount of knowledge implicitly in their parameters. Hao et al. 2022 harvested symbolic Knowledge Graphs from the LMs and proposed a framework for automatic KG construction. However, this approach has thus far only been tested on non-medical
English data. <br>
Therefore, this master thesis aims to evaluate the potential of language models as a source for harvesting clinical knowledge in German.

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
This paper proposes an automated framework to extract a Knowledge Graph from pre-trained LMs such as BERT or RoBERTa. The framework derives knowledge of new relation types and entities, independent of existing knowledge bases or corpora. The study investigates the knowledge capacity of different models, revealing that larger models encode more knowledge. <br>
<br>
Core components of BERTnet: 
1. Automatic creation of diverse prompts with confidence weights

Given the input information of a relation: initial prompt and a few shots of seed entity pairs 
→ initial prompt is paraphrased to a large set of prompts that are linguistically diverse but semantically describe the same relation. Entity names are then removed. Each prompt is associated with a confidence weight. 
Based on the edit distance the prompts that are sufficiently different are kept. Compatibility score is created to avoid noisy prompts.

2. Efficient search to discover consistent entity pairs 

Entity pairs are harvested that satisfy all prompts. The minimum individual log-likelihoods and weighted averaged across different prompts are used to propose a large set of candidate entity pairs.

These pairs are then re-ranked based with the full consistency score and top-K instances are picked as the output knowledge
It is important to change the language of the stopwords that used to filter out the unnecessary candidates.  

### Prompt Engineering

Getting the right prompt is very important in order to extract accurate entity pairs. This sections contains samples of different types of prompts that have been used in the experiments. 

1. Das \<ENT1> wird bei der Krankheit \<ENT0> angewendet.

2. Das in der Kardiologie verwendete Medikament \<ENT1> dient der Behandlung von Krankheit \<ENT0> .

3. Medikament: Warfarin, Krankheit: Vorhofflimmern. Das Medikament \<ENT1> wird zur Behandlung der Krankheit \<ENT0> in der Kardiologie eingesetzt.

4. In der Kardiologie wird das Medikament Warfarin bei Vorhofflimmern eingesetzt. Auch das Medikament Amiodaron wird zur Behandlung der Arrhythmie verwendet. Das Medikament Aspirin wird bei Arteriosklerose angewendet. Das Medikament \<ENT1> wird zur Behandlung der Krankheit \<ENT0> in der Kardiologie eingesetzt.

## Experiments

### Models 

- gBERT-base 
- gBERT-large
- medBERT.de

### Experimental setup
Four sets of extractions: 
- models taken from hugging face, 
- further pre-trained models 
- further pre-trained models + contextualized prompts
- further pre-trained models + few-shot learning prompts

## Results 
This section will list out some of the best results that were produced.

## Evaluation 


HasMedication: 156 generated pairs --> 50 correct pairs <br>
HasDrugForm: 116 generated pairs --> 15 correct pairs <br>
HasRiskFaktor: 68 generated pairs --> 45 correct pairs <br>
HasSideEffect: 100 generated pairs --> 18 correct pairs <br>
HasSymptom:  125 generated pairs --> 68 correct pairs <br>


## References

Hao et al. 2022
Socrates 2022
Bressem et al. 2023 
Devlin et al. 2019
