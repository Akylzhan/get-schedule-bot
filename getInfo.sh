#!/bin/bash
curl -L --output data/courseList.gz 'https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json' \
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
-H 'X-Requested-With: XMLHttpRequest' \
--data 'method=getSearchData&searchParams%5BformSimple%5D=false&searchParams%5Blimit%5D=1000&searchParams%5Bpage%5D=1&searchParams%5Bstart%5D=0&searchParams%5BquickSearch%5D=&searchParams%5BsortField%5D=-1&searchParams%5BsortDescending%5D=-1&searchParams%5Bsemester%5D=541&searchParams%5Bschools%5D=&searchParams%5Bdepartments%5D=&searchParams%5Blevels%5D=&searchParams%5Bsubjects%5D=&searchParams%5Binstructors%5D=&searchParams%5Bbreadths%5D=&searchParams%5BabbrNum%5D=&searchParams%5Bcredit%5D='

gunzip -c data/courseList.gz > data/courseList.json
rm data/courseList.gz


curl -L --output data/instructors.gz 'https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json' \
-X 'POST' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Accept: application/json, text/javascript, */*; q=0.01' \
-H 'Accept-Language: en-us' \
-H 'Accept-Encoding: gzip, deflate, br' \
-H 'Host: registrar.nu.edu.kz' \
-H 'Origin: https://registrar.nu.edu.kz' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15' \
-H 'Connection: keep-alive' \
-H 'Referer: https://registrar.nu.edu.kz/course-catalog/json' \
-H 'Content-Length: 21' \
-H 'X-Requested-With: XMLHttpRequest' \
--data 'method=getInstructors'

gunzip -c data/instructors.gz > data/instructors.json
rm data/instructors.gz


curl -L --output data/semesters.gz 'https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json' \
-X 'POST' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Accept: application/json, text/javascript, */*; q=0.01' \
-H 'Accept-Language: en-us' \
-H 'Accept-Encoding: gzip, deflate, br' \
-H 'Host: registrar.nu.edu.kz' \
-H 'Origin: https://registrar.nu.edu.kz' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15' \
-H 'Connection: keep-alive' \
-H 'Referer: https://registrar.nu.edu.kz/course-catalog/json' \
-H 'Content-Length: 19' \
-H 'X-Requested-With: XMLHttpRequest' \
--data 'method=getSemesters'

gunzip -c data/semesters.gz > data/semesters.json
rm data/semesters.gz


curl -L --output data/schools.gz 'https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json' \
-X 'POST' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Accept: application/json, text/javascript, */*; q=0.01' \
-H 'Accept-Language: en-us' \
-H 'Accept-Encoding: gzip, deflate, br' \
-H 'Host: registrar.nu.edu.kz' \
-H 'Origin: https://registrar.nu.edu.kz' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15' \
-H 'Connection: keep-alive' \
-H 'Referer: https://registrar.nu.edu.kz/course-catalog/json' \
-H 'Content-Length: 17' \
-H 'X-Requested-With: XMLHttpRequest' \
--data 'method=getSchools'

gunzip -c data/schools.gz > data/schools.json
rm data/schools.gz


curl -L --output data/departments.gz 'https://registrar.nu.edu.kz/my-registrar/public-course-catalog/json' \
-X 'POST' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Accept: application/json, text/javascript, */*; q=0.01' \
-H 'Accept-Language: en-us' \
-H 'Accept-Encoding: gzip, deflate, br' \
-H 'Host: registrar.nu.edu.kz' \
-H 'Origin: https://registrar.nu.edu.kz' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15' \
-H 'Connection: keep-alive' \
-H 'Referer: https://registrar.nu.edu.kz/course-catalog/json' \
-H 'Content-Length: 21' \
-H 'X-Requested-With: XMLHttpRequest' \
--data 'method=getDepartments'

gunzip -c data/departments.gz > data/departments.json
rm data/departments.gz

