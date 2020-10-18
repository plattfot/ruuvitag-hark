;; Copyright (C) 2020  Fredrik Salomonsson

;; This file is part of ruuvitag-hark.

;; Ruuvitag-hark is free software: you can redistribute it and/or
;; modify it under the terms of the GNU General Public License as
;; published by the Free Software Foundation, either version 3 of the
;; License, or (at your option) any later version.

;; Ruuvitag-hark is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
;; General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with ruuvitag-hark. If not, see
;; <https://www.gnu.org/licenses/>.

(use-modules (guix packages)
             (guix download)
             (guix git-download)
             (guix build-system python)
             ((guix licenses) #:prefix license:)
             (gnu packages)
             (gnu packages python)
             (gnu packages python-web)
             (gnu packages python-xyz)
             (gnu packages check))

;; (define-public python-rx
;;   (package
;;     (name "python-rx")
;;     (version "3.1.1")
;;     (source
;;      (origin
;;        (method url-fetch)
;;        (uri (pypi-uri "Rx" version))
;;        (sha256
;;         (base32
;;          "1pl2298hk9zn6k75vsxgvd242s1941lbvka3hhhmmz97vg7m2a2n"))))
;;     (build-system python-build-system)
;;     ;; (native-inputs
;;     ;;  `(("python-pytest-runner" ,python-pytest-runner)
;;     ;;    ("python-pytest" ,python-pytest)
;;     ;;    ("python-coverage" ,python-coverage)
;;     ;;    ("python-pytest-asyncio" ,python-pytest-asyncio)))
;;     (arguments
;;      `(#:tests? #f)) ;; No tests directory in release
;;     (home-page "http://reactivex.io")
;;     (synopsis "Reactive Extensions (Rx) for Python")
;;     (description
;;      "Reactive Extensions (Rx) for Python")
;;     (license license:expat)))

(define-public python-rx
  (package
    (name "python-rx")
    (version "1.6.1")
    (source
     (origin
       (method url-fetch)
       (uri (pypi-uri "Rx" version))
       (sha256
        (base32
         "08wcfkcz1zxq1176iz0gyhfgxbafc4g4g5f77lbmqqjjwbcxi88k"))))
    (build-system python-build-system)
    (arguments
     `(#:tests? #f)) ;; No tests directory in release
    (home-page "http://reactivex.io")
    (synopsis "Reactive Extensions (Rx) for Python")
    (description
     "Reactive Extensions (Rx) for Python")
    (license license:expat)))

(define-public python-ruuvitag-sensor
  (package
    (name "python-ruuvitag-sensor")
    (version "1.1.0")
    (source
     (origin
       (method git-fetch)
       (uri (git-reference
             (url "https://github.com/ttu/ruuvitag-sensor")
             (commit version)))
       (file-name (git-file-name name version))
       (sha256
        (base32
         "1i9aj218rlkhwb1i7kb56bmcfvrlzb0mawvgnj8ccwzlw2jgpz99"))))
    (build-system python-build-system)
    (native-inputs
     `(("python-mock" ,python-mock)
       ("python-nose" ,python-nose)
       ("python-ptyprocess" ,python-ptyprocess)))
    (propagated-inputs `(("python-rx" ,python-rx)))
    (home-page
     "https://github.com/ttu/ruuvitag-sensor")
    (synopsis
     "Find RuuviTag sensor beacons, get and encode data from selected sensors")
    (description
     "Find RuuviTag sensor beacons, get and encode data from selected sensors")
    (license license:expat)))

(define-public python-bleson
  (package
   (name "python-bleson")
   (version "0.1.6")
   (source
    (origin
     (method url-fetch)
     (uri (pypi-uri "bleson" version))
     (sha256
      (base32
       "1pgp3w4g9yc4isxfllymnay85jclr8hi2k0s6p43ry63lqvz51vk"))))
   (build-system python-build-system)
   (arguments
    `(#:tests? #f)) ;; guix's python3 not built with bluetooth support
   (home-page
    "https://github.com/TheCellule/python-bleson")
   (synopsis "Bluetooth LE Library")
   (description "Bluetooth LE Library")
   (license license:expat)))

(packages->manifest
 (list
  python
  python-ruuvitag-sensor
  python-bleson
  python-ptyprocess
  python-aiohttp
  python-toml
  python-pep517
  python-pytest
  python-tox
  ))

