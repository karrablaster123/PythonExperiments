import sys
import re
from urllib.parse import urlencode, quote_plus
import requests
from time import sleep

argc = len(sys.argv)

if argc < 4:
    print("usage: web_blast.py program database query [query]...")
    print("where program = megablast, blastn, blastp, rpsblast, blastx, tblastn, tblastx\n")
    print("example: web_blast.py blastp nr protein.fasta")
    print("example: web_blast.py rpsblast cdd protein.fasta")
    print("example: web_blast.py megablast nt dna1.fasta dna2.fasta")
    sys.exit(1)

program = sys.argv[1]
database = sys.argv[2]

if program == "megablast":
    program = "blastn&MEGABLAST=on"

if program == "rpsblast":
    program = "blastp&SERVICE=rpsblast"

# read and encode the queries
encoded_queries = []
for query in sys.argv[3:]:
    with open(query) as f:
        encoded_query = quote_plus(f.read().strip())
        encoded_queries.append(encoded_query)

# build the request
args = {"CMD": "Put", "PROGRAM": program, "DATABASE": database, "QUERY": "\n".join(encoded_queries)}
url = "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(url, data=urlencode(args), headers=headers)

# parse out the request id
rid = re.search(r"^    RID = (.*$)", response.text, re.MULTILINE).group(1)

# parse out the estimated time to completion
print(re.search(r"^    RTOE = (.*$)", response.text, re.MULTILINE).group(1))
rtoe = int(re.search(r"^    RTOE = (.*$)", response.text, re.MULTILINE).group(1))

# wait for search to complete
sleep(rtoe)

# poll for results
while True:
    sleep(5)

    url = f"https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID={rid}"
    response = requests.get(url)

    if re.search(r"\s+Status=WAITING", response.text):
        # print("Searching...")
        continue

    if re.search(r"\s+Status=FAILED", response.text):
        print("Search", rid, "failed; please report to blast-help@ncbi.nlm.nih.gov.")
        sys.exit(4)

    if re.search(r"\s+Status=UNKNOWN", response.text):
        print("Search", rid, "expired.")
        sys.exit(3)

    if re.search(r"\s+Status=READY", response.text):
        if re.search(r"\s+ThereAreHits=yes", response.text):
            # print("Search complete, retrieving results...")
            break
        else:
            print("No hits found.")
            sys.exit(2)

    # if we get here, something unexpected happened.
    sys.exit(5)

# retrieve and display results
url = f"https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&FORMAT_TYPE=Text&RID={rid}"
response = requests.get(url)
f = open("myfile.txt", "w")
f.write(response.text)
print(response.text)
sys.exit(0)