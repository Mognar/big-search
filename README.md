# big-search [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/Mognar/big-search/master)
A jupyter notebook to help formulate searches on multiple thesaurus terms

Click the "Launch Binder" badge above to launch the Jupyter notebook. 

Parliamentary Search allows users to search on multiple subjects at a time. However, Search can only handle a text search on about 30-40 subject terms (depending on the length of the search term). In comparison, Search can handle over 100 term IDs (the unique identifier applied to each term). 

Our material is indexed using our Thesaurus terms, and these terms are organised in a hierarchy. Housing is a term, but underneath Housing there are more specific terms: Housing standards, Housing supply, Mortgages etc... And within those child terms may be even mroe specific terms: Mortgages has the child term Negative equity. 

Our indexers apply the most specific terms to material, to make the indexing as informative as possible. However, a search for Housing will not return results for its child terms. This specificity of searches is often useful, but occasionally a user may wish to find all material on the subject of Housing, including more granular subjects under Housing, like Temporary accommodation. 

This Jupyter notebook allows you to type in a broad term, such as Housing, and create a search query that includes all child terms that sit under that term. 

Please note - the term you type in has to be a part of the Thesaurus. If the term you type in is not a term in our Thesaurus (e.g. "Klingons"), you will get no results. 



