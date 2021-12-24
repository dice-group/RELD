# RELD: A Knowledge Graph of Relation Extraction Datasets
RDFizing relation extraction datasets and benchmarking relations and sentences.

## Documentation


### Conversion to RDF

The script can be used to generate the RDF of a single dataset individually or at once for all datasets (The process will take a few hours to complete for all the datasets at once)
### Prerequisites
The required packages for running the script will be installed by running the following command:
```
 pip install -r requirements.txt
```

#### Single dataset conversion
To convert a single dataset, you can run the individual script as follow:

```
  # For SemEval 2010 Task 8 Dataset
  python semEval.py
  
  # For Google Relation Extraction Dataset
  python google.py
  
  # For Wikipedia-Wikidata Dataset
  python wikiRE.py
  
  # For WEBNLG Dataset
  python webNlg.py
  
  # For FewRel Dataset
  python few_rel.py
  
  # For NYT-FB Dataset
  python nyt.py
  
```
The .ttl output will be saved in the respective folders inside the output folder

<b>Note:</b> The datasets files must be in the respective folders inside the data folder, otherwise, you need to set the path variable inside each script. 

#### Conversion at once for all six datasets
To convert all the datasets at once, you need to run the following command:

```
 python main.py 
```
<hr>

### Datasets used

| *Dataset*   | *Download*  |
|-------------|-----------|
|Wikipedia_Wikidata|[Download](https://www.informatik.tu-darmstadt.de/ukp/research_6/data/lexical_resources/wikipedia_wikidata_relations/)|
|SemEval 2010 Task 8|[Download](http://www.kozareva.com/downloads.html)|
|WEBNLG|[Download](https://webnlg-challenge.loria.fr/)|
|Google RE|[Download](https://github.com/google-research-datasets/relation-extraction-corpus)|
|FewRel|[Download](https://www.zhuhao.me/fewrel/)|
|NYT-FB|[Download](http://iesl.cs.umass.edu/riedel/ecml/)|

<hr>

## Sustainability

### Static dumps

The generated dumps in .ttl format are available online [here](https://hobbitdata.informatik.uni-leipzig.de/RELD/ttl_dumps/)

The dumps are also available in JSON-LD format for non-semantic web community [here](https://hobbitdata.informatik.uni-leipzig.de/RELD/json_dumps/)

<hr>

### SPARQL Endpoint

The endpoint for RELD is live [here](http://reld.cs.upb.de:8890/sparql)

<hr>

### Local Virtuoso Endpoint

A linux based local Virtuoso endpoint is avaliable [here](https://hobbitdata.informatik.uni-leipzig.de/RELD/endpoint/) that is easily configurable.

#### Setup local endpoint

Download the local Virtuoso from from the above mentioned link and unzip it; then run the following commands to setup a local instance:

```
cd bin
sh start_virtuoso.sh

```
After running the above commands the local instance will be availble on http://localhost:8890/sparql


<hr>

### Coming soon updates

Integrating DocRed dataset to RELD. 


### Overview of RELD Framework
![RELD Model Overview](images/Model.svg)

<hr>

## RELD Example SPARQL Queries

Following are two example SPARQL queries on RELD dataset:

#### Q1: 

Selecting 40 relations based on some filter criteria

```
PREFIX reldv : <https://reld.dice-research.org/schema/>
SELECT ? rId
WHERE
{
? rId reldv : hasSentence ? sent .
? sent reldv : numOfTokens ? nT .
? sent reldv : numBetToken ? tB .
FILTER (? nT < 25 && ? tB > 5 )
}
LIMIT 40
  
```

#### Q2: 

Selecting distinct relations based on number of sentences grouping 

```
PREFIX reldv : <https://reld.dice-research.org/schema/>
SELECT
DISTINCT ? rId
( AVG (? nToken ) as ? avgToken ) ( count (? ne ) as ? avgNE )
{
? rId reldv : hasSentence ? sentence .
? sentence reldv : numOfTokens ? nToken .
? sentence reldv : hasN amedEn tity ? ne .
}
Group by ? rId having ( count (? sentence ) = 700)
  
```

#### Q3: 

To get distinct relations from an individual graph here is an example query for Wikipedia-Wikidata dataset 

```
SELECT  distinct ?relations 
from <http://reld.dice-research.org/Wiki-RE> 
where {
  ?relations <https://reld.dice-research.org/schema/hasSentence> ?sent.
  }
  
```

### Authors
  * [Manzoor Ali](https://dice-research.org/ManzoorAli) (DICE, Paderborn University) 
  * [Muhammad Saleem](https://sites.google.com/site/saleemsweb/) (AKSW, University of Leipzig) 
  * [Axel-Cyrille Ngonga Ngomo](https://dice-research.org/AxelCyrilleNgongaNgomo) (DICE, Paderborn University)

## License
The source code of this repo is published under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

