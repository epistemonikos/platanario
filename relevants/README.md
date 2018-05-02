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
 * intervention_to_improve_vaccination.tsv
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

Stopwords are words, that are frequent in a group of documents, but they are not really relevant. Normally words as: a, be, is, are common English stopwords.

We will try to identify, stopwords for this groups of documents, an we will exclude this words from the relevants ones.

The way we are going to calculate the stopwords, is to get the data for 3 different groups. In this case, all of those groups are health releated cientific articles, for different diseases. A minimum of 3 groups is recommended to get good results.

```
python main.py stopwords data/examples/health_articles/ 5 > data/examples/health_articles_stopwords.txt
```
The parameter 5, means we are going to use the fith column of the file (remember the file is separated by tabs), in my case the fith column was the abstract of the reference.

When we are running the command: python main.py stopwords data/references/sr_groups/ 5

That gives you a list of phrases that could be stopwords.

Example of the first 25 phrases:

|-------------------|
| studies           |
| review            |
| results           |
| data              |
| methods           |
| trials            |
| evidence          |
| patients          |
| risk              |
| medline           |
| included          |
| literature        |
| treatment         |
| controlled        |
| conclusions       |
| criteria          |
| background        |
| identified        |
| quality           |
| systematic review |
| have              |
| search            |
| effects           |
| is                |
| associated        |

In this example, we reviewed the first 1,000 phrases and from there we identified 939 as stopwords and 61 were not stopwords.

## Calculate relevant phrases


```
python main.py relevants data/examples/health_articles 4,5 > data/examples/health_articles_relevants.tsv
```

In this case we are going to use both, title (4) and abtract (5), to calculate the relevants words.

We will obtain a tab separated file, looking like this:


| group_id    | phrase                                      | count | rank           |
|-------------|---------------------------------------------|-------|----------------|
| common_cold | common cold                                 | 146   | 0.0124         |
| common_cold | antibiotics                                 | 22    | 0.0035         |
| common_cold | vitamin c                                   | 19    | 0.0034         |
| common_cold | placebo group                               | 10    | 0.0043         |
| common_cold | antibiotic use                              | 5     | 0.0076         |
| common_cold | common cold incidence                       | 8     | 0.0031         |
| common_cold | acute purulent rhinitis                     | 11    | 0.002          |
| common_cold | zinc lozenges                               | 17    | 0.0013         |
| common_cold | zinc gluconate lozenges                     | 8     | 0.0024         |
| common_cold | zinc gluconate                              | 5     | 0.0038         |
| common_cold | common cold patients                        | 3     | 0.0062         |
| common_cold | acute cough                                 | 7     | 0.0022         |
| common_cold | nasal                                       | 12    | 0.0013         |
| common_cold | upper respiratory tract infection           | 4     | 0.0038         |
| common_cold | acute urtis                                 | 12    | 0.0012         |
| common_cold | acute rhinosinusitis                        | 7     | 0.002          |
| common_cold | routine treatment                           | 2     | 0.0068         |
| common_cold | probiotics                                  | 8     | 0.0017         |
| common_cold | cochrane acute respiratory infections group | 2     | 0.0059         |
| common_cold | acute                                       | 4     | 0.003          |
| common_cold | acute otitis media                          | 4     | 0.003          |
| common_cold | common                                      | 2     | 0.0059         |
| common_cold | common signs                                | 2     | 0.0059         |
| common_cold | cold symptoms                               | 8     | 0.0014         |
| common_cold | review authors                              | 3     | 0.0036         |

...

The count is the counter for that specific phrase in the group
The rank is a metric calculated using pytextrank, based in the context.
You can filter by the count. For example only phrases that has more than 1 in count.


