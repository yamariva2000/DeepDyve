import argparse

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str,help="choose model i.e. LsiModel")
parser.add_argument('--num_docs', type=int,help="choose number of docs")
parser.add_argument('--num_topics', type=int,help="choose number of topics")
parser.add_argument('--field', type=str,help="choose doc field")
parser.add_argument('--lemmatize', type=bool,help="true for lemmatizing")

args = parser.parse_args()
