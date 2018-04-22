# Relevants phrases
The idea is to identify relevants phrases from a group of documents.

A group is a file in tsv, where each line is a reference or text been part of the group.
You can have several files (one for each group)

## Requirements
 * Python3 (maybe could work with Python2, not been tested)

## Installing
```
pip install -r requirements.txt
mkdir data
```

## Getting Stopwords
Is important to identify the stopwords. We calculate stopwords taking into account the phrases from several groups, so it's important that you add more than 3 groups, and ideally very differents from each other.

The parameter 5, means we are going to use the fith column of the file (remember the file is separated by tabs), in my case the fith column was the abstract of the reference.
```
python main.py stopwords data/references/sr_groups/ 5 > data/possible_stopwords.txt
```

Where my folder data/references/sr_groups/ looks like this:

```
bronchopulmonary_dysplasia.tsv
colorectal_cancer.tsv
common_cold.tsv
congenital_cardiac_diseases.tsv
infertility.tsv
intervention_to_improve_vaccination.tsv
medical_cannabinoids.tsv
meningococcal_disease.tsv
neural_tube_defects.tsv
palliative_care.tsv
personality_disorder.tsv
refractive_errors.tsv
respiratory_distress_of_newborn.tsv
subarachnoid_hemorrhage.tsv
testicular_cancer.tsv
```

And each file looks like this:

```
f66bdc15ae683153d787560778573d904fa7ebca	10.1016/S0140-6736(10)60278-4	20552718	Elective high-frequency oscillatory versus conventional ventilation in preterm infants: a systematic review and meta-analysis of individual patients' data.	BACKGROUND: Population and study design heterogeneity has confounded previous meta-analyses, leading to uncertainty about effectiveness and safety of elective high-frequency oscillatory ventilation (HFOV) in preterm infants. We assessed effectiveness of elective HFOV versus conventional ventilation in this group. METHODS: We did a systematic review and meta-analysis of individual patients' data from 3229 participants in ten randomised controlled trials, with the primary outcomes of death or bronchopulmonary dysplasia at 36 weeks' postmenstrual age, death or severe adverse neurological event, or any of these outcomes. FINDINGS: For infants ventilated with HFOV, the relative risk of death or bronchopulmonary dysplasia at 36 weeks' postmenstrual age was 0.95 (95% CI 0.88-1.03), of death or severe adverse neurological event 1.00 (0.88-1.13), or any of these outcomes 0.98 (0.91-1.05). No subgroup of infants (eg, gestational age, birthweight for gestation, initial lung disease severity, or exposure to antenatal corticosteroids) benefited more or less from HFOV. Ventilator type or ventilation strategy did not change the overall treatment effect. INTERPRETATION: HFOV seems equally effective to conventional ventilation in preterm infants. Our results do not support selection of preterm infants for HFOV on the basis of gestational age, birthweight for gestation, initial lung disease severity, or exposure to antenatal corticosteroids. FUNDING: Nestlé Belgium, Belgian Red Cross, and Dräger International.
318f54b154978e294c3d351baf2cfdba52e0427d	10.1136/adc.2010.210187	21697236	Chorioamnionitis as a risk factor for bronchopulmonary dysplasia: a systematic review and meta-analysis.	OBJECTIVE: o conduct a systematic review of the association between chorioamnionitis (CA) and bronchopulmonary dysplasia (BPD) in preterm infants. METHODS: he authors searched Medline, Embase, CINAHL, Science Citation Index and PubMed, reviewed reference lists and contacted the primary authors of relevant studies. Studies were included if they had a comparison group, examined preterm or low birthweight infants, and provided primary data. Two reviewers independently screened the search results, applied inclusion criteria and assessed methodological quality. One reviewer extracted data and a second reviewer checked data extraction. Studies were combined with an OR using a random effects model. Meta-regression was used to explore potential confounders. Results 3587 studies were identified; 59 studies (15 295 patients) were included. The pooled unadjusted OR showed that CA was significantly associated with BPD (OR 1.89, 95% CI 1.56 to 2.3). Heterogeneity was substantial (I(2)=66.2%) and may be partially explained by the type of CA. Infants exposed to CA were significantly younger and lighter at birth. The pooled adjusted OR was 1.58 (95% CI 1.11 to 2.24); heterogeneity was substantial (I(2)=65.1%) which may be due to different variables being controlled in each study. There was strong evidence of publication bias which suggests potential overestimation of the measure of association between CA and BPD. CONCLUSIONS: nadjusted and adjusted analyses showed that CA was significantly associated with BPD; however, the adjusted results were more conservative in the magnitude of association. The authors found strong evidence of publication bias. Despite a large body of evidence, CA cannot be definitively considered a risk factor for BPD.
...
````

When we are running the command: python main.py stopwords data/references/sr_groups/ 5

That gives you a list of words that could be stopwords, in my case the first 500 were all stopwords, then manual review was needed.

## Calculate relevant phrases


```
python main.py relevants data/references/sr_groups/ 4 > data/relevants_title.tsv
```

```
python main.py stopwords data/references/sr_groups/ 4 > data/relevants_abstract.tsv
```

We will obtain a tab separated file, looking like this in my case:


| group_id        | phrase                             | count | rank        | 
|-----------------|------------------------------------|-------|-------------| 
| palliative_care | palliative care                    | 31    | 0.047364846 | 
| palliative_care | systematic                         | 31    | 0.021011936 | 
| palliative_care | cancer                             | 24    | 0.006006845 | 
| palliative_care | end-of-life                        | 20    | 0.003588642 | 
| palliative_care | palliative                         | 4     | 0.017030767 | 
| palliative_care | ill patients                       | 5     | 0.004758822 | 
| palliative_care | pediatric palliative care programs | 1     | 0.023682423 | 
| palliative_care | adult                              | 11    | 0.001995739 | 
| palliative_care | care interventions                 | 3     | 0.006766407 | 
| palliative_care | surgical patients                  | 1     | 0.01903529  | 
| palliative_care | palliative care patients           | 2     | 0.009517645 | 
| palliative_care | advanced cancer                    | 6     | 0.003003423 | 
| palliative_care | diseases                           | 7     | 0.002422722 | 
| palliative_care | therapy                            | 10    | 0.00164028  | 

...

The count is the counter for that specific phrase in the group
The rank is a metric calculated using pytextrank, based in the context.
You can filter by the count. For example only phrases that has more than 1 in count.


