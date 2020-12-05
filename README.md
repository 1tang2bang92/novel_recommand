# Novel Recommand System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Logo](https://miro.medium.com/max/640/1*55ujLQhjMm6Quc_pzeqYjw.jpeg)

<center>나에게 알맞는 웹 소설을 추천받아 보자.</center>

## Description
---
[네이버 시리즈](https://series.naver.com/novel), [조아라](https://joara.com/main.html), [문피아](https://novel.munpia.com)를 크롤링해 사용자에게 맞는 소설을 추천하는 프로그램입니다.

## 환경
---
server : centos 8 + podman + k8s
db : maria db
backend : python + Django
frontend : flutter
build server : github action -> local server

## 설계 구조
---

## 사용 방법 (Usage)
---

## 추가 예정
---
1. 카카오페이지
2. 리디북스
3. 네이버 소설
4. app
## [robots.txt](https://namu.wiki/w/robots.txt)
---
2020/12/06 기준 각 사이트에서 크롤링 가능한 페이지인지 확인함.
* [naver series](https://series.naver.com/robots.txt)
>User-agent: *
>Disallow: /
>Allow: /$
>Allow: /ebook/home.nhn
>Allow: /comic/home.nhn
>Allow: /novel/home.nhn
>Allow: /movie/home.nhn
>Allow: /broadcasting/home.nhn
>Allow: /ebook/detail.nhn
>Allow: /comic/detail.nhn
>Allow: /novel/detail.nhn
>Allow: /series
* [joara](http://www.joara.com/robots.txt)
>User-agent: *
>Disallow: /config/
>Disallow: /cron_data/
>Disallow: /itemshop/
>Disallow: /itemshop_sum/
>Disallow: /member/
>Disallow: /mypage/
>Disallow: /payment/
>Disallow: /search/
>Disallow: /user/
>Disallow: /literature/webtoon/
>Disallow: /adkey/
>Disallow: /app/
>Disallow: /cash/
>Disallow: /cron/
>Disallow: /inc/
>Disallow: /js/
>Disallow: /renew/
>Disallow: /modules/
* [munpia](https://novel.munpia.com/robots.txt)
>User-agent: Twitterbot
>Allow: /files/attach/
>
>User-agent: *
>Disallow: /addon/
>Disallow: /ch/
>Disallow: /files/
>Disallow: /tpl/
>Disallow: /widget/
>Disallow: /page/goods_event

## Lisence
---
The MIT License (MIT)
Copyright © <2020> <copyright 1tang2bang92>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
