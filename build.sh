#!/bin/sh

function process {
  cc -E - < "$1"
}

rm -rf ./build
mkdir ./build

for html_file in $(find -name "*.html"); do
  path=./build/${html_file#./}
  mkdir $(dirname $path) 2> /dev/null
  sed "/^#/d" <(process $html_file) > $path
done
