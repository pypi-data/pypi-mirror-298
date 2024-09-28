# CHANGELOG

## v0.6.0 (2024-09-27)

### Feature

* feat: override user in job container ([`63ffceb`](https://gitlab.com/phooijenga/trycicle/-/commit/63ffcebba67f994d6373c59157713592a1056a1d))

## v0.5.0 (2024-09-27)

### Chore

* chore(release): version 0.5.0 ([`9a6a5c3`](https://gitlab.com/phooijenga/trycicle/-/commit/9a6a5c3a25a42c8b56782f4c079cd3d580b27d65))

### Feature

* feat: implement parallel and parallel:matrix ([`18aac39`](https://gitlab.com/phooijenga/trycicle/-/commit/18aac393a2fe2fb5cad92e77afd75a8052b2fffa))

### Refactor

* refactor: split run_job ([`9b1ef75`](https://gitlab.com/phooijenga/trycicle/-/commit/9b1ef7534dfae2beb1f4fa4c5250096b7b492353))

### Test

* test: add timeout to interactive sessions ([`0817fe4`](https://gitlab.com/phooijenga/trycicle/-/commit/0817fe46b8738370cb38ef4baee7bc5060d6c484))

## v0.4.1 (2024-07-13)

### Chore

* chore(release): version 0.4.1 ([`8ed62b4`](https://gitlab.com/phooijenga/trycicle/-/commit/8ed62b4ad421d6ff67e458600ef017099f6c13af))

### Fix

* fix: cache component versions separately ([`a0216b9`](https://gitlab.com/phooijenga/trycicle/-/commit/a0216b9ec4531a2adbf885d891ac400f78ae31fc))

### Refactor

* refactor: consistently use pathlib for paths ([`462db6b`](https://gitlab.com/phooijenga/trycicle/-/commit/462db6b22958bb832a236f4a577d9504efa3f0cf))

## v0.4.0 (2024-07-13)

### Chore

* chore(release): version 0.4.0 ([`f0794b0`](https://gitlab.com/phooijenga/trycicle/-/commit/f0794b07d5cf409f92adf8ca4c46394990ceb631))

### Documentation

* docs: add include example to readme ([`4c4f254`](https://gitlab.com/phooijenga/trycicle/-/commit/4c4f25406f70f1724b05b3aa104971b923309649))

### Feature

* feat: authenticate CI catalog queries ([`10cad64`](https://gitlab.com/phooijenga/trycicle/-/commit/10cad6403ca6765aecfbe3972426653dfb5cf604))

* feat: implement include:component ([`0297b56`](https://gitlab.com/phooijenga/trycicle/-/commit/0297b56e9e5159e6e96028f03a911878450b3947))

* feat: implement include:template ([`bfef881`](https://gitlab.com/phooijenga/trycicle/-/commit/bfef8812c71db0939f9d291d4a7ddf03fb4d72b4))

* feat: make variables available to includes ([`15c3897`](https://gitlab.com/phooijenga/trycicle/-/commit/15c3897c09783e14482f3d2425d8f814ed649116))

* feat: implement include:remote ([`6f53002`](https://gitlab.com/phooijenga/trycicle/-/commit/6f530026fd57eeb5a60e4ac78e28439746af1580))

* feat: implement include:inputs ([`cb3364d`](https://gitlab.com/phooijenga/trycicle/-/commit/cb3364de5566379c233c7106c21294391592bd73))

### Fix

* fix: use cache directory when tab-completing ([`4b8e9cc`](https://gitlab.com/phooijenga/trycicle/-/commit/4b8e9cc52cd8dfa980d683b4bb4305b91dec3d46))

* fix: treat glob pattern without metacharacters as literal path ([`06a5e08`](https://gitlab.com/phooijenga/trycicle/-/commit/06a5e080dfbffa8fe891b1983d892ad5a54b55ac))

* fix: add variables used by components ([`601aaf0`](https://gitlab.com/phooijenga/trycicle/-/commit/601aaf0a5684d1646fa5b8acc569ea3684fe44b3))

* fix: write job list to stdout ([`66fa9cc`](https://gitlab.com/phooijenga/trycicle/-/commit/66fa9cc033a7739f6da3626c42cb5c7a03d8a299))

* fix: recursively expand variables ([`71c1566`](https://gitlab.com/phooijenga/trycicle/-/commit/71c1566693d08fd16241a09819f6eda864528e8a))

## v0.3.1 (2024-04-24)

### Chore

* chore(release): version 0.3.1 ([`80d3f27`](https://gitlab.com/phooijenga/trycicle/-/commit/80d3f2749a76a3565247cf82a71c2e777880c61d))

### Fix

* fix: stop script on first failure ([`47be6b2`](https://gitlab.com/phooijenga/trycicle/-/commit/47be6b2702b02dcfb3d62b463749c0b8718ae9af))

## v0.3.0 (2024-04-16)

### Chore

* chore(release): version 0.3.0 ([`50426f7`](https://gitlab.com/phooijenga/trycicle/-/commit/50426f73430ef63a783c72552dd106ac8437ae61))

### Documentation

* docs: add cache example to readme ([`dfc5336`](https://gitlab.com/phooijenga/trycicle/-/commit/dfc5336bed36ac37c10d65a1979f8f22af6bbef8))

### Feature

* feat: refactor how extends are applied

Previously the parser would construct a set of partial job objects.
When a job was requested from the config, it would resolve each field
independenly, following the extends keyword to parent jobs if necessary.

This meant that to merge fields like `variables`, special handling was
necessary, which was not available to other fields (like `cache`).

The parser now merges values from `extends`, `default` and globals in
the same way (and only when the job is requested from the config). ([`b2cb7ea`](https://gitlab.com/phooijenga/trycicle/-/commit/b2cb7ea332b0989e3ea12cc6e283f72994092110))

* feat: implement caches ([`d2dce55`](https://gitlab.com/phooijenga/trycicle/-/commit/d2dce554de404deb17adc0ba719fa2ddee793882))

### Fix

* fix: add source directory name to cache key ([`3a2eb24`](https://gitlab.com/phooijenga/trycicle/-/commit/3a2eb242e6fd8d498b5f2cb7402bf917134ea04e))

* fix: ensure directories exist when copying cache ([`f813d6f`](https://gitlab.com/phooijenga/trycicle/-/commit/f813d6f44b81473abe475a909dccfa69a62c7639))

* fix: use user cache directory ([`5356312`](https://gitlab.com/phooijenga/trycicle/-/commit/535631254c76b2999a6218f08fc0787690a752cd))

* fix: allow cache without key ([`0d83b73`](https://gitlab.com/phooijenga/trycicle/-/commit/0d83b7347197010b6d6317091d3e555c3b2176d2))

### Test

* test: add cache test ([`a4d9c4c`](https://gitlab.com/phooijenga/trycicle/-/commit/a4d9c4ce229a967671c90d640900ca90e432888b))

## v0.2.2 (2024-03-31)

### Chore

* chore(release): version 0.2.2 ([`8e574c6`](https://gitlab.com/phooijenga/trycicle/-/commit/8e574c69e96d0334ef167994e681eba825abfa43))

### Fix

* fix(ci): skip version job only ([`4d01c5e`](https://gitlab.com/phooijenga/trycicle/-/commit/4d01c5ea12619264ad098c27bd7280190f0c21de))

## v0.2.1 (2024-03-31)

### Chore

* chore(release): version 0.2.1 [skip ci] ([`c3ac08e`](https://gitlab.com/phooijenga/trycicle/-/commit/c3ac08e69dfed126cc6963e1d737b9c8d55d75f4))

### Fix

* fix(ci): skip pipeline on version commit ([`8bf80a8`](https://gitlab.com/phooijenga/trycicle/-/commit/8bf80a827428caa1aaed0ef8d76306c04ae2e8f0))

## v0.2.0 (2024-03-31)

### Chore

* chore(release): 0.2.0 ([`84fc81b`](https://gitlab.com/phooijenga/trycicle/-/commit/84fc81b1fd371c768ecfe9cfe480490c12d72776))

### Feature

* feat: automate releases ([`6d1ba46`](https://gitlab.com/phooijenga/trycicle/-/commit/6d1ba467136808d1477ed1197848e4984c1b632a))

### Fix

* fix(ci): job token can not push to repository ([`79d8348`](https://gitlab.com/phooijenga/trycicle/-/commit/79d8348bf64fcd56f9644b043fefcf2a166af35e))
