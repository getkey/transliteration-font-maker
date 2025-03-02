#!/bin/sh

cp ./decompose/traditional_greek_romanization_base.tsv ./transcriptions/traditional_greek_romanization.tsv
./decompose/decompose.py >> ./transcriptions/traditional_greek_romanization.tsv
