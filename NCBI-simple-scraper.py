import sys

from Bio import Entrez

import config  # requires config.py file with Entrez credentials.

Entrez.email = config.email
Entrez.api_key = config.api_key


def get_search(query):
    with Entrez.esearch(
        db="protein", term=query, idtype="acc", usehistory="y"
    ) as handle:
        search_results = Entrez.read(handle)
    return search_results


def get_sequences(search_results, out_file, batch_size=200, start_batch=0):
    webenv = search_results["WebEnv"]
    query_key = search_results["QueryKey"]
    count = int(search_results["Count"])

    if start_batch >= count or start_batch == -1:
        return

    with open(out_file, "a") as out:
        for start in range(start_batch, count, batch_size):
            sucess = False
            while not sucess:
                try:
                    fetch_handle = Entrez.efetch(
                        db="protein",
                        rettype="fasta",
                        retmode="text",
                        retstart=start,
                        retmax=batch_size,
                        webenv=webenv,
                        query_key=query_key,
                        idtype="acc",
                    )
                    sucess = True
                except:
                    continue

            data = fetch_handle.read()
            fetch_handle.close()
            out.write(data)


def main():
    query = ""
    search_results = get_search(query)
    get_sequences(
        search_results,
        out_file="phage-ref-seq.fasta",
    )


if __name__ == "__main__":
    sys.exit(main())
