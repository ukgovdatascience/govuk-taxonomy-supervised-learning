import json
import sys


def write_json(stream, generator):
    stream.write("[ ")
    stream.write(json.dumps(next(generator)))
    index = 0
    for index, taxon in enumerate(generator):
        stream.write(",\n")
        stream.write(json.dumps(taxon))
        if index % 1000 is 0:
            print("Documents exported: %s" % index, file=sys.stderr)
    stream.write("]\n")
    print("Documents exported: %s" % index, file=sys.stderr)
