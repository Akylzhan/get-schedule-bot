#!/bin/bash

data=$1

curl -sL --output $data.gz 'https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json' \
-X 'POST' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Accept: application/json, text/javascript, */*; q=0.01' \
-H 'Accept-Language: en-us' \
-H 'Accept-Encoding: gzip, deflate, br' \
-H 'Host: registrar.nu.edu.kz' \
-H 'Origin: https://registrar.nu.edu.kz' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15' \
-H 'Connection: keep-alive' \
-H 'Referer: https://registrar.nu.edu.kz/course-catalog' \
-H 'Cookie: _ga=GA1.3.715067609.1593191964; _gid=GA1.3.1028721498.1596383249; has_js=1; AUTHSSL=1; SSESS4985c7dbe54e755248659c29e4b83d20=9Ax14hRcBz1rfLX-oVxRTLsfjvO5TPiOQd2ExrWTxpI; _fbp=fb.2.1596398202999.123217043; _ym_isad=1; _ym_d=1596398202; _ym_uid=1593583841192740854' \
-H 'X-Requested-With: XMLHttpRequest' \
--data 'method=getSearchData&searchParams%5BformSimple%5D=false&searchParams%5Blimit%5D=100&searchParams%5Bpage%5D=1&searchParams%5Bstart%5D=0&searchParams%5BquickSearch%5D='$data'&searchParams%5BsortField%5D=-1&searchParams%5BsortDescending%5D=-1&searchParams%5Bsemester%5D=521&searchParams%5Bschools%5D=&searchParams%5Bdepartments%5D=&searchParams%5Blevels%5D=&searchParams%5Bsubjects%5D=&searchParams%5Binstructors%5D=&searchParams%5Bbreadths%5D=&searchParams%5BabbrNum%5D=&searchParams%5Bcredit%5D='
gunzip -c $data.gz > $data.json
rm $data.gz
cat $data.json
rm $data.json