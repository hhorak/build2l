get_url_smart() {
  if [ $# -eq 0 ] ; then
    echo "Usage: `basename $0` http://something.com/.*.rpm"
    exit 1
  fi

  while [ $# -gt 0 ] ; do
    url=$1
    shift
    dirurl=$(dirname $url)
    file_pattern=$(basename $url)

    # get srpm path
    curl -Ls ${dirurl} | grep -Po '(?<=href=")[^"]*' | grep -e "${file_pattern}$" | while read srpmpath ; do
      [[ $srpmpath =~ ^http(s)?:// ]] || srpmpath="$dirurl/$srpmpath"
      echo "$srpmpath"
    done
  done
}

download_file_smart() {
  get_url_smart "$@" | while read srpmpath ; do
    echo -n "Downloading $srpmpath ..."
    wget -q "$srpmpath"
    echo " DONE"
  done
}
