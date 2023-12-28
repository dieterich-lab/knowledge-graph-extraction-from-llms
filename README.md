# Harvesting German clinical knowledge from pre-trained language models

## Introduction

Knowledge graphs can be a great tool to leverage information, more specifically healthcare data, that can lead to improved clinical decision-making, enhanced
research capabilities, and optimized healthcare delivery, this can be achieved by integrating patient-specific data with medical knowledge.
However, most knowledge graphs are manually created, might not fit all tasks and are mostly in English. These KGs can be rather costly to construct and they are not applicable to German data. Recently, language models like BERT have been shown to encode a large amount of knowledge implicitly in their parameters. Hao et al. 2022 harvested symbolic Knowledge Graphs from the pretrained LMs and proposed a framework for automatic KG construction. However, this approach has thus far only been tested on non-medical English data. <br>
Therefore, this master thesis aims to evaluate the potential of pre-trained language models as a source for harvesting clinical knowledge in German.

### Researh Questions 

Q1. Can German clinical knowledge be extracted from pre-trained language models? <br>
Q2. What is the optimal combination of models, data and prompts to give the best results? <br>
Q3. What is the best evaluation strategy? <br>


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

## Data 

The following table contains some statistics about the 

| Name           | Number of Tokens | Number of Documents | Domain      |
|-----------------|-----------------|-----------------|-----------------|
| GGPONC         | 1,877,100        | 30              | Oncology        |
| BRONCO150      | 70,572           | 150             | Oncology        | 
| DKG            | ToDO             | 128             | Cardiology      | 
| CARDIO.de      | 993,143          | 500             | Cardiology      |
| MieDEEP        | 977,504          | 500             | Cardiology      | 


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


<p float="left">
  <img src="https://github.com/dieterich-lab/knowledge-graph-extraction-from-llms/blob/main/results/gbert-base.png" alt="gbert-base" width="300" height="500">
  <img src="https://github.com/dieterich-lab/knowledge-graph-extraction-from-llms/blob/main/results/gbert-large.png" alt="gbert-large" width="300" height="500">
  <img src="https://github.com/dieterich-lab/knowledge-graph-extraction-from-llms/blob/main/results/medbert_comparison.png" alt="medbert" width="300" height="500"> <br>
  Figure 1. Futher pre-trained gBERT-base  Figure 2. Further pre-trained gBERT-large      Figure 3. Further pretrained medBERT.de
</p>
<br>
<p float="left">
  <img src="https://github.com/dieterich-lab/knowledge-graph-extraction-from-llms/blob/main/results/no_context_prompt_illnessRecommendation.png" alt="no_context" width="400" height="500">
  <img src="https://github.com/dieterich-lab/knowledge-graph-extraction-from-llms/blob/main/results/prompt_with_context_illnessRecommendation.png" alt="with_context" width="400" height="500"> <br>
  Figure 4. Prompt with no cardiology context Figure 5. Prompt with cardiology context
</p>
<br>
The following results are from the medbert.de model.
<p float="left">
  <img src="https://github.com/dieterich-lab/knowledge-graph-extraction-from-llms/blob/main/results/hasMedication.png" alt="meds" width="300" height="500">
<br> 
  Figure 6. hasMedication <br> 
<p float="left">
  <img src="https://github.com/dieterich-lab/knowledge-graph-extraction-from-llms/blob/main/results/hasDrugForm.png" alt="no_context" width="400" height="500">
  <img src="https://github.com/dieterich-lab/knowledge-graph-extraction-from-llms/blob/main/results/hasRiskFactor.png" alt="with_context" width="400" height="500"> <br>
  Figure 7. hasDrugForm Figure 8. hasRiskFactors
</p>
<br>
<p float="left">
  <img src="https://github.com/dieterich-lab/knowledge-graph-extraction-from-llms/blob/main/results/hasSymptoms.png" alt="no_context" width="400" height="500">
  <img src="https://github.com/dieterich-lab/knowledge-graph-extraction-from-llms/blob/main/results/hasSideEffect.png" alt="with_context" width="400" height="500"> <br>
  Figure 9. hasSymptopms Figure 10. hasSideEffects
</p>
<br>
  
## Evaluation 
Manual evalution is the most effective approach. To reduce the effort of manually checking over 100 entries and extra filtering step has been added. The filtering steps involves passing the output of the BERTnet framework in batches of 20 to gpt4 with an instruction to filter out pairs that are wrong for the given relation. 
an example of an instuction: <br>
"For element in the nested list: element[0] is a disease and element[1] is a medication. Go through the list and if element[1] is a valid medication for element[0] or it is part of therapy for element[0] then keep it in the list, if not, then remove it from the list"<br>
These the filtered results: <br>
HasMedication: 156 generated pairs --> 50 correct pairs <br>
HasDrugForm: 116 generated pairs --> 15 correct pairs <br>
HasRiskFaktor: 68 generated pairs --> 45 correct pairs <br>
HasSideEffect: 100 generated pairs --> 18 correct pairs <br>
HasSymptom:  125 generated pairs --> 68 correct pairs <br>

## Conclusion
From the above results, it can be seen that it is possible to extract German clinical Knowledge from a pre-trained language model. The best results are extracted from a medBERT.de model that was further pre-trained on the cardio data(DGK, CARDIO.de and mieDEEP). The best evaluation strategy is to pass the results through a filtering step with GPT4 and then do a manual check on the remaining enities. 

## References

Hao et al. 2022 "BertNet: Harvesting Knowledge graphs from pretrained language models" <br>
Vimig Socrates. (2022). Extraction of Diagnostic Reasoning Relations for Clinical Knowledge Graphs.  <br>
Bressem et al. 2023 "medBERT.DE: A comprehensive German BERT model for the medical domain"  <br>
Devlin, Jacob et al. “BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.” North American Chapter of the Association for Computational Linguistics (2019).
