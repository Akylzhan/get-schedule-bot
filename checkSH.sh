#!/bin/bash
data=$1

curl -sL --output - 'https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json' \
-X 'POST' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Accept: application/json, text/javascript, */*; q=0.01' \
-H 'Accept-Language: en-us' \
-H 'Accept-Encoding: gzip, deflate, br' \
-H 'Host: registrar.nu.edu.kz' \
-H 'Origin: https://registrar.nu.edu.kz' \
-H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0' \
-H 'Connection: keep-alive' \
-H 'Referer: https://registrar.nu.edu.kz/course-catalog' \
-H 'X-Requested-With: XMLHttpRequest' \
--data 'method=getSearchData&searchParams%5BformSimple%5D=false&searchParams%5Blimit%5D=700&searchParams%5Bpage%5D=1&searchParams%5Bstart%5D=0&searchParams%5BquickSearch%5D='$data'&searchParams%5BsortField%5D=-1&searchParams%5BsortDescending%5D=-1&searchParams%5Bsemester%5D=521&searchParams%5Bschools%5D=&searchParams%5Bdepartments%5D=&searchParams%5Blevels%5D=&searchParams%5Bsubjects%5D=&searchParams%5Binstructors%5D=&searchParams%5Bbreadths%5D=&searchParams%5BabbrNum%5D=&searchParams%5Bcredit%5D='\
 | gunzip -c