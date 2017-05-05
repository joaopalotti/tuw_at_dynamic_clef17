# TUW at Dynamic CLEF17

This repository contains the data used by TUW team at the pilot task of Dynamic Search workshop at CLEF 17.

Our system leverages the structure of Wikipedia pages to build a search agent.
We consider that the human editors would carefully choose meaningful section names covering the various aspects of an information need for the topic covered by a page.

Let's take as an example the first query used in this challenge:

```html
<topics>
<topic num='4'>
<cat>health</cat>
<query>quit smoking</query>
<desc>Your friend would like to quit smoking. You would like to provide him with relevant information about different ways to quit smoking, programs available to help quit smoking, benefits of quitting smoking, second effects of quitting smoking, using hypnosis to quit smoking, using the cold turkey method to quit smoking</desc>
</topic>
```
The very first hit for __quit smoking__ on the English Wikipedia is [Smoking Cessation](https://en.wikipedia.org/wiki/Smoking_cessation), which contains the following sections (as it was on the May 5th 2017): [Methods](https://en.wikipedia.org/wiki/Smoking_cessation#Methods), [Special Populations](https://en.wikipedia.org/wiki/Smoking_cessation#Special_populations), [Comparison of success rates](https://en.wikipedia.org/wiki/Smoking_cessation#Comparison_of_success_rates), [Factors Affection Success](https://en.wikipedia.org/wiki/Smoking_cessation#Factors_affecting_success), [Side Effects](https://en.wikipedia.org/wiki/Smoking_cessation#Side_effects), [Health Benefits](https://en.wikipedia.org/wiki/Smoking_cessation#Health_benefits), [Cost-Effectiveness](https://en.wikipedia.org/wiki/Smoking_cessation#Cost-effectiveness), [Statistical trends](https://en.wikipedia.org/wiki/Smoking_cessation#Statistical_trends). Our intuition is that each section is a section because humans considered it to be an important aspect of this page, and we explore this explicit judgment in our system.

Our system is a collection os scripts each one responsible for a simple task:
(1) query_wikipedia.py: Extracts candidate pages from several Wikipedia pages (in the submitted version, we used the top 3 Wikipedia pages for each query/topic).
(2) rank_candidates.py: Ranks the candidate sections. Alternatives explored are:
  __run1:__ _human_: a human inspected each subsection and used the top 5 most useful ones.
  __run2:__ _mean_: it is based on a pretrained word2vec model (trained on a GoogleNews corpus). We used the mean of all cosine similarities of each word in the description of a topic compared to each word in the content of a section.
  __run3:__ _fifo_: we simply used the first 5 sections found in the top 3 Wikipedia pages (they might come all from the top one Wikipedia page for example if it has 5 or more sections).
(3) obtain_training.py: TODO
(4) predictor.py: TODO
(5) search.py: TODO




