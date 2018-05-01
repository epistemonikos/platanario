# Relevants phrases

Identify relevants phrases from a group of documents. A document can be anything containing text. A group is a set of documents that share something in common.

## Requirements
 * Python3 (maybe could work with Python2, not been tested)

## Installing
```
pip install -r requirements.txt
mkdir data
```

## Example data
We will as example data, health related cientifics articles in particular a type of document called systematic review.

The format of that data, needs to be formatted as tsv (tab separated values)

The example folder looks like this:
```
ls -1 data/examples/health_articles
```

 * common_cold.tsv
 * personality_disorder.tsv
 * testicular_cancer.tsv

Each one of those documents look like this: 

```
head -n2 data/examples/health_articles/common_cold.tsv
```

```
b366e2842d29e3f5c7e05afa0cef1fef25d404ca	10.1002/14651858.CD004782.pub2	17253524	Chinese medicinal herbs for the common cold	BACKGROUND: Chinese medicinal herbs are frequently used to treat the common cold in China. Until now, their efficacy has not been systematically reviewed. OBJECTIVES: To assess the effectiveness and safety of Chinese medicinal herbs for the common cold. SEARCH STRATEGY: We searched the Cochrane Central Register of Controlled Trials (CENTRAL) (The Cochrane Library 2008, issue 2), which contains the Cochrane Acute Respiratory Infections Group's Specialised Register; MEDLINE (1966 to May 2008); EMBASE (1980 to May 2008); AMED (1985 to May 2008); the Chinese Biomedical Database (CBMdisc) (1978 to May 2008); and China National Knowledge Infrastructure (CNKI) (1994 to May 2008). SELECTION CRITERIA: Randomised controlled trials (RCTs) studying the efficacy of Chinese medicinal herb(s) for the treatment of the common cold. DATA COLLECTION AND ANALYSIS: Four review authors telephoned the original trial authors of the RCTs identified by our searches to verify the randomisation procedure. Two review authors extracted and analysed data from trials which met the inclusion criteria. MAIN RESULTS: We found17 studies involving 3212 patients. The methods of 15 studies were at high risk of bias. In only two studies was the risk of bias low. Trials used "positive drugs", of which the efficacy was not known, as controls. Different Chinese herbal preparations were tested in nearly all trials. In only one trial was a Chinese herbal preparation tested twice. In seven trials, six herbal preparations were found to be more effective at enhancing recovery than the control preparations. In the other 10 studies, seven herbal preparations were not shown to be significantly different from the control. One study did not describe the difference between the intervention and control groups. AUTHORS' CONCLUSIONS: Chinese herbal medicines may shorten the symptomatic phase in patients with the common cold. However, the lack of trials of low enough risk of bias, or using a placebo or a drug clearly identified as a control, means that we are uncertain enough to be unable to recommend any kind of Chinese medicinal herbs for the common cold.
5bbcf96743bca418bf4c995245d0d6f18121ebce	10.1016/j.rmed.2004.11.004	15733498	Antibiotics for upper respiratory tract infections: an overview of Cochrane reviews.	OBJECTIVES: The aim of this paper is to review the four Cochrane reviews of antibiotics for upper respiratory tract infections. METHODS: Each Cochrane review was read and summarized, and results presented as odds ratios (as in the Internet version) and, where relevant, numbers needed to treat. RESULTS: The reviews of antibiotics for acute otitis media have concluded that benefit is not great with a number needed to treat for a benefit (NNTB) of 15. Recent US guidelines are recommending a delay in prescriptions in children over the age of 6 months. For streptococcal tonsillitis, the Cochrane reviewers suggest that antibiotic use seems to be discretionary rather than prohibited or mandatory. This is because the benefit in terms of symptoms is only about 16h (NNTB from 2 to 7 at day 3 for pain) compared with placebo, and that serious complications, such as rheumatic fever and glomerulonephritis, are now rare in developed countries. The reviewers do, however, suggest that antibiotics are considered in populations in whom these complications are more common. This is an area of debate, as the Infectious Disease Society of America (2002) recommends routine treatment. [Clin. Infect. Dis. 35 (2002) 113] There is good evidence and consensus that there is no indication for antibiotics for the common cold. The situation with acute purulent rhinitis is less clear, as new evidence suggests that antibiotics may be effective for acute purulent rhinitis (NNTB from 6 to 8). However, as most people with acute purulent rhinitis improve without antibiotics, giving antibiotics is not justified as an initial treatment. For acute maxillary sinusitis, the evidence suggests that antibiotics are effective for people with radiologically confirmed sinusitis. The reviewers suggest that clinicians should weigh up the modest benefits (NNTB from 3 to 6) against the potential for adverse effects. CONCLUSION: The use of antibiotics for acute otitis media, sore throat and streptococcal tonsillitis, common cold and acute purulent rhinitis, and acute maxillary sinusitis seems to be discretionary rather than prohibited or mandatory, at least for non-severe cases.
```


## Getting Stopwords

Is important to identify the stopwords. Stopwords are word that are common and can be present as relevant phrases for one specific group, but will be present as relevant in several groups. The way we are going to calculate the stopwords, is to get the data for 3 different groups, in the same area, in this example we will use 3 group of documents, all of those are health releated cientific articles, for different diseases. A minimum of 3 groups is recommended to get good results.

```
export TARGET_FOLDER="examples/health_articles"
python main.py stopwords data/${TARGET_FOLDER}/ 5 > data/${TARGET_FOLDER}_possible_stopwords.txt
```
The parameter 5, means we are going to use the fith column of the file (remember the file is separated by tabs), in my case the fith column was the abstract of the reference.

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

Each file have the following columns: id, doi, pmid, title, abstract

And they look like this:

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
python main.py stopwords data/references/sr_groups/ 5 > data/relevants_abstract.tsv
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


