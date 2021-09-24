# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/grafeas/#history

### [1.1.3](https://www.github.com/googleapis/python-grafeas/compare/v1.1.2...v1.1.3) (2021-09-24)


### Bug Fixes

* add 'dict' annotation type to 'request' ([594f8d1](https://www.github.com/googleapis/python-grafeas/commit/594f8d19b3515c1cadab9fdacbba4317d4b43b29))

### [1.1.2](https://www.github.com/googleapis/python-grafeas/compare/v1.1.1...v1.1.2) (2021-07-28)


### Bug Fixes

* enable self signed jwt for grpc ([#88](https://www.github.com/googleapis/python-grafeas/issues/88)) ([81a0635](https://www.github.com/googleapis/python-grafeas/commit/81a06350840a854631ea9997d1c851aa62883d4b))


### Documentation

* add Samples section to CONTRIBUTING.rst ([#84](https://www.github.com/googleapis/python-grafeas/issues/84)) ([2849415](https://www.github.com/googleapis/python-grafeas/commit/28494150a4f0f4fbf1d70161e494ad3faf511412))


### Miscellaneous Chores

* release as 1.1.2 ([#89](https://www.github.com/googleapis/python-grafeas/issues/89)) ([508aa4d](https://www.github.com/googleapis/python-grafeas/commit/508aa4dc1c61dfc4cb12ed16c062977ed3f324ba))

### [1.1.1](https://www.github.com/googleapis/python-grafeas/compare/v1.1.0...v1.1.1) (2021-07-20)


### Bug Fixes

* **deps:** pin 'google-{api,cloud}-core', 'google-auth' to allow 2.x versions ([#83](https://www.github.com/googleapis/python-grafeas/issues/83)) ([1ada5bc](https://www.github.com/googleapis/python-grafeas/commit/1ada5bceefcbe750d40613614fccf5ad3a94fec5))

## [1.1.0](https://www.github.com/googleapis/python-grafeas/compare/v1.0.1...v1.1.0) (2021-05-20)


### Features

* bump release level to production/stable ([#71](https://www.github.com/googleapis/python-grafeas/issues/71)) ([53bd8a5](https://www.github.com/googleapis/python-grafeas/commit/53bd8a50ab731cf43d0c789198d221c7fbff6fb6))

### [1.0.1](https://www.github.com/googleapis/python-grafeas/compare/v1.0.0...v1.0.1) (2020-08-12)


### Bug Fixes

* remove gapic surface ([#42](https://www.github.com/googleapis/python-grafeas/issues/42)) ([aed68fe](https://www.github.com/googleapis/python-grafeas/commit/aed68fe9a83f041097d8a34f95eb89a1042b7b14))

## [1.0.0](https://www.github.com/googleapis/python-grafeas/compare/v0.4.1...v1.0.0) (2020-08-11)


### ⚠ BREAKING CHANGES

* generate with microgenerator (#36)

### Features

* generate with microgenerator ([#36](https://www.github.com/googleapis/python-grafeas/issues/36)) ([2785cc2](https://www.github.com/googleapis/python-grafeas/commit/2785cc23c3c59457d9f42a9ef1321c2ad0fade47))

### [0.4.1](https://www.github.com/googleapis/python-grafeas/compare/v0.4.0...v0.4.1) (2020-06-25)


### Bug Fixes

* update retry config ([#24](https://www.github.com/googleapis/python-grafeas/issues/24)) ([122ec6a](https://www.github.com/googleapis/python-grafeas/commit/122ec6a2fdf93ad745b6c275defa0bb809f1d005))

## [0.4.0](https://www.github.com/googleapis/python-grafeas/compare/v0.3.0...v0.4.0) (2020-02-07)


### Features

* **grafeas:** add support for upgrade notes; add `cpe` and `last_scan_time` to `DiscoveryOccurrence`; add `source_update_time` to `VulnerabilityNote` (via synth) ([#10084](https://www.github.com/googleapis/python-grafeas/issues/10084)) ([2ee967b](https://www.github.com/googleapis/python-grafeas/commit/2ee967b916e663bacbda8c391528cdca3a1117fd))


### Bug Fixes

* **grafeas:** deprecate resource name helper methods (via synth) ([#9835](https://www.github.com/googleapis/python-grafeas/issues/9835)) ([a2c26d9](https://www.github.com/googleapis/python-grafeas/commit/a2c26d9b60194d305f8cb2b8ec4a4a33d7bf3686))

## 0.3.0

10-10-2019 11:28 PDT


### Implementation Changes
- Remove send / receive message size limit (via synth). ([#8981](https://github.com/googleapis/google-cloud-python/pull/8981))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))

## 0.2.0

07-12-2019 17:04 PDT


### Implementation Changes
- replace `min_affected_version` w/ `affected_version_{start,end}` (via synth).  ([#8465](https://github.com/googleapis/google-cloud-python/pull/8465))
- Allow kwargs to be passed to create_channel, update templates (via synth). ([#8391](https://github.com/googleapis/google-cloud-python/pull/8391))

### New Features
- Update list method docstrings (via synth). ([#8510](https://github.com/googleapis/google-cloud-python/pull/8510))

### Documentation
- Update READMEs. ([#8456](https://github.com/googleapis/google-cloud-python/pull/8456))

### Internal / Testing Changes
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))

## 0.1.0

06-17-2019 10:44 PDT

### New Features
- Initial release of the Grafeas client library. ([#8186](https://github.com/googleapis/google-cloud-python/pull/8186))
