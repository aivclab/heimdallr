#!/usr/bin/env bash

PARENT="$( dirname -- "$0"; )";
cd "${PARENT}" || exit
#./"${PARENT}"/clean.sh
./clean.sh
for f in Makefile; do
  make -f "$f" html || exit
  #make -f "$f" epub || exit
done
