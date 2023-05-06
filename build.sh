#!/bin/sh

function process {
  cc -E - < "$1"
}

rm -rf ./build
mkdir ./build

for html_file in $(find -name "*.html"); do
  sed "/^#/d" <(process $html_file) > ./build/${html_file#./}
done
