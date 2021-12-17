#!/bin/bash
# test.sh [file - $tests_available] [regex merge]
tests_available="basic positive negative "

function do_test() {
  if [ -f "test/$1_test.bats" ] ; then
    echo -e "$1 TESTING\n"
    bats test/$1_test.bats $filter
    my_exitcode=$?
    if [ $my_exitcode -ne 0 ] ; then
      exit $my_exitcode
    fi
  else
    echo "file test/$1_test.bats not found"
  fi
}


if [ "$1" == "all" ] || [ "$1" == "" ] ; then
  select="all"
elif [[ $tests_available =~ "$1 " ]] ; then
  select=$1
else
  echo "$1 is not a proper selection !!!"
  echo "please try: [$tests_available] or all"
  exit 1
fi

if [ ! -z "$2" ] ; then
  filter="-f $2"
else
  filter=""
fi



if [ "$select" == "all" ] ; then
  for i in $tests_available ; do
    echo "> $i"
    do_test $i
  done
else
  do_test $1
fi

exit 1
