#!/bin/bash
# test.sh [file - $tests_available] [regex merge]
tests_available="basic positive negative docker autoresume "
parallel_tests=20



function do_test() {
  if [ -f "test/$1_test.bats" ] ; then
    echo -e "$1 TESTING\n"
    if [ ${parallel_tests} -gt 1 ] && [ ${1} != "docker" ]; then
      bats --jobs ${parallel_tests} test/$1_test.bats $filter
    else
      bats test/$1_test.bats $filter
    fi
    my_exitcode=$?
    if [ $my_exitcode -ne 0 ] ; then
      echo "Test \"$1\" failed - exiting"
      post_cleanup
      exit $my_exitcode
    fi
  else
    echo "file test/$1_test.bats not found"
  fi
}

function do_tag() {
  my_date=$(date +%Y%m%d-%H%M%S-%Z)
  git tag "BATS-TEST-SUCCESSFUL__$my_date"
}

function pre_cleanup() {
  # We saw some issues with stale (unkilled) processes
  killall timeout -9
}

function post_cleanup() {
  # We saw some issues with stale (unkilled) processes
  echo "cleaning up potential stale test processes"
  for proc in $(ps -ef | egrep -i "uls" | grep -v "grep" | cut -d " " -f 4) ; do
    if ! [ -z $proc ] ; then
      echo ">killing< $proc"
      kill -9 $proc
    fi
  done
}


# The code

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


pre_cleanup
if [ "$select" == "all" ] ; then
  for i in $tests_available ; do
    echo "> $i"
    do_test $i
    do_tag
  done
else
  do_test $1
fi

post_cleanup
exit 0
