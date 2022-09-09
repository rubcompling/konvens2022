# Assessing the Linguistic Complexity of German Abitur Texts from 1963–2013

This dataset accompanies the following research paper:

Noemi Kapusta, Marco Müller, Matilda Schauf, Isabell Siem and Stefanie Dipper (2022). Assessing the Linguistic Complexity of German Abitur Texts from 1963–2013. Proceedings of KONVENS 2022.


## Data (in `data/`)

### Sample data:

* Sample texts from the GraphVar corpus (two each from 1963, 1993, 2018), with kind permission of Kristian Berg (Bonn)
* Sample fragments from the EXPRESS and ZEIT corpus

### Formats

* GraphVar:
  * `*.xml`: original [EXMARaLDA](https://github.com/Exmaralda-Org/exmaralda) XML format
  * `*.conllup`: CoNLL-U Plus Format, documented [here](https://github.com/rubcompling/C6C/blob/master/README_Importers.md#graphvarexbimporter)
  
  The conversion script that maps XML to CoNLL-U PlUS uses the [C6C scripts](https://github.com/rubcompling/C6C): `python3 C6C.py convert -i "graphvar" -e "conlluplus" -cols "src/graphvar.conf" <INDIR> <OUTDIR>`

* EXPRESS and ZEIT:
  * `*.wpl`: 1 word per line
  * `*.spl`: 1 sentence per line
  * `*_all.wpl` / `*_all.spl`: all fragments concatenated; empty line indicates the fragment boundaries
  * `*.parsed`: output of the [Berkeley Parser](https://www.cs.mcgill.ca/~jcheung/topoparsing/topoparsing.html), using the model "tuebadz_topf_no_edge.gr"
  * `*.conllup`: CoNLL-U Plus Format with just POS and syntactic information in BIO format, as documented [here](https://github.com/rubcompling/C6C/blob/master/README_Importers.md#graphvarexbimporter)

  The conversion script that maps syntax brackets to the BIO format first removes extra whitespace (`line = line.replace(" (", "(").replace(" )", ")")`) and then uses the [C6C scripts](https://github.com/rubcompling/C6C): `python3 C6C.py convert -i "tuebatrees" -p "['treetobio']" -e "conlluplus" <INDIR> <OUTDIR>`


### Temporary files

are stored in `data_tmp/`


## Scripts (in root and `src/`)

The scripts for calculating complexity are stored in individual notebooks, which use modules and data splits provided in `src/`.

* Lexical diversity: `1_lexical_diversity.ipynb`
* Perplexity: `2_perplexity.ipynb`
* Syntactic complexity: `3_syntactic_complexity.ipynb`
* For calculating significance for the syntactic features, first collect all results in one file: `python3 src/collect_syn_results.py`. Next find trend lines applying regression analyses: `Rscript src/calc_syn_significance.R`.


## Results (in `results/`)

The directory results contains:

1. The results from the complete original corpora (which we cannot provide here due to legal issues): `results/1_lex/`, `results/2_perplex/`, `results/3_syntax/`. Each subdirectory contains the results for the GraphVar development data (20%) and the final test data (80%). In addition, `results/1_lex/` and `results/3_syntax/` contain the results for the reference corpora EXPRESS and ZEIT. `results/3_syntax/significance/` contains the results for the syntax significance tests.

2. The results for the demo data provided in: `results/1_lex_demo/`, `results/2_perplex_demo/`, `results/3_syntax_demo/`.


## Authors

This study is the result of a collaborative work which was developed in the course "Symbolic and Statistical Methods in Computational Linguistics" in the winter semester 2021/22 at Ruhr-University Bochum. Participating students were Noemi Kapusta, Marco Müller, Matilda Schauf and Isabell Siem under the supervision of Stefanie Dipper.

## License

All data and software is provided under CC BY 4.0.

For questions or problems, feel free to file a GitHub issue, or contact me direc
tly:

    Stefanie Dipper (stefanie.dipper@rub.de)
