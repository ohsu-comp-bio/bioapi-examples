"""
    hello_ga4gh_client.py
    Provides examples of using GA4GH compliant API using
    a supplied client library.
"""

# In this example we will use the ga4gh client to make
# working with the API a little easier. We won't need
# the requests module because the ga4gh client handles
# the HTTP layer.

import ga4gh.client as client

# Documentation for the functions made avaialable by this
# client can be found here:
# http://ga4gh-reference-implementation.readthedocs.org/en/latest/api.html#client-api

BASE_URL = "http://ga4gh-a1.westus.cloudapp.azure.com/ga4gh-count1-data/"

def main():
    # First, instantiate an HTTP client using the BASE_URL.

    c = client.HttpClient(BASE_URL)

    # If you are using an IDE with autocompletion (like PyCharm)
    # you should be able to access the named functions by
    # placing a `.` after the c in your editor.

    # We'll start by finding the datasets as we did in the
    # previous example.

    response = c.searchDatasets()

    # Notice that the client returns a generator so we have
    # to iterate through the response to get our datasets.

    print(response)
    datasets = []

    for dataset in response:
        datasets.append(dataset)
        print(dataset)

    # We can repeat the process of collecting all variant
    # sets as was done in `hello_ga4gh` without fussing
    # with json.

    variant_sets = []

    for dataset in datasets:
        # The client provides results as classed objects,
        # so we can access their attributes using dot-notation.

        datasetId = dataset.id
        response = c.searchVariantSets(datasetId)
        for variant_set in response:
            variant_sets.append(variant_set)

    # We'll now pick out a single variant set to do some
    # analysis on.

    variant_set = variant_sets[0]
    variantSetId = variant_set.id
    variants = c.searchVariants(variantSetId, 100000, 900000, "1")

    # The client manages paging for us, so there may be
    # a large number of results generated by a search.
    variant_list = []

    for variant in variants:
        variant_list.append(variant)

    print(str(len(variant_list)) + " variants.")

    # Here we will generate the same count of reference base
    # length as in the previous examples.

    reference_base_counts = {}

    for variant in variant_list:
        reference_base_length = len(variant.referenceBases)
        if reference_base_length not in reference_base_counts:
            reference_base_counts[reference_base_length] = 1
        else:
            reference_base_counts[reference_base_length] += 1

    # Did we get the same results as in `hello_ga4gh.py`?

    print(reference_base_counts)

if __name__ == "__main__":
    main()