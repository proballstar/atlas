# 🚀 Atlas
[![Build Status](https://travis-ci.com/firebolt-space/atlas.svg?branch=master)](https://travis-ci.com/firebolt-space/atlas)

```
       _______ _                _____ 
    /\|__   __| |        /\    / ____|
   /  \  | |  | |       /  \  | (___  
  / /\ \ | |  | |      / /\ \  \___ \ 
 / ____ \| |  | |____ / ____ \ ____) |
/_/    \_\_|  |______/_/    \_\_____/ 

🚀 This is Atlas. Fast. Fuel efficient. The official rocket of Firebolt Space Agency.
We chose to build Atlas not because it is easy, but because it is hard.

- Aaron Ma & Rohan Fernandes
```

![Atlas](./images/moon.jpg?raw=true)
![Rocket](https://github.com/firebolt-space/atlas/blob/master/svg/rocket/rocket.svg?raw=true)

**ALERT!**
We're delaying Atlas v0.0.1 to May 25, 2020. The reason we're making this change is due to the ever growing threat of the COVID-19 (Coronavirus Disease 2019), we want to make sure that the public is safe, as your safety is our top priority.

Atlas is an end-to-end open source platform for rockets. It contains a comprehensive, flexible ecosystem of tools, libraries, and community resources that lets researcher push state-of-the-art research in rocket science and developers to easily integrate Atlas into their existing rocket codebase.

Atlas was originally developed by two middle school students, Aaron Ma and Rohan Fernandes who realized that researchers needed a better way to develop software for rockets.

Atlas provides stable Python APIs, along with currently developing C++ binding API. Support for other languages are future plans. Our ideas for support with other languages are:

* Ruby
* Assembly
* R
* C
* JavaScript
* TypeScript
* PHP
* Java
* Objective-C
* Swift
* CSS(for styling)
* Scala
* Rust
* CoffeeScript
* Perl
* Kotlin
* Go
* Matlab
* Julia
* Fortran
* C#
* ActionScript
* Dart
* Other (suggest them here -> hi@aaronhma.com)

## Coding Versions
If you want a setup to run Atlas code just like us, here's our coding versions used while developing Atlas.

**Python**: 3.7.6 (released on December 30, 2019)

**C++**: C++ 14 (released in 2014)

## Versions

*Versions may change at any time, and released marked "🎖" may change at any time, without notice, per descretion at The Atlas Authors.*

**Atlas 0.0.1: Special Holiday Release**

Atlas 0.0.1, commonly referred to the Starter Kit will be released on April 1, 2020.

This release contains:

* Code name: Mars Martian
* Works: Honeycomb, Rocket basic functionality
* Actively working on: Python API, C++ API
* Acknowledgements: This release was couldn't be made without the 💖 & 😀 of Aaron Ma and Rohan Fernandes.
* APIs from mini projects 

Atlas 0.0.1's logo is stil TBA and under review.

**🎖 Atlas 0.0.2**

Atlas 0.0.2, codenamed Venus, is planned to be released on June 5, 2020.

**🎖 Atlas 0.0.3:**

Atlas 0.0.3, codenamed Lunar Unicorn, is planned to be released on December 21, 2020.

**🎖 Atlas 0.0.4:**

Atlas 0.0.4, codenamed Bionic Dingo, is planned to be released on February 28, 2021.

**🎖 Atlas 0.0.5:**

Atlas 0.0.5, codenamed Saturn Salamandar, is planned to be released on August 16, 2021.

**🎖 Atlas 0.0.6:**

Atlas 0.0.6, codenamed Mercury, is planned to be released on November 29, 2021.

**🎖 Atlas 0.0.7:**

Atlas 0.0.7, codenamed W, is planned to be released on April 6, 2022.

🎖 Future Dates Are TBA

## Alert! Please Read!
We, Aaron Ma and Rohan Fernandes are preparing a special holiday release for April Fool's Day 2020. Stay tuned for updates!

FOR ROHAN & AARON:

Please check your assignments and grades in ASSIGNMENTS.md

FOR ATLAS GROUND CREW:

In the Storage Room, we have provided disinfecting sprays and hand sanitizer. Use hand sanitizer often and use the disinfecting sprays to spray in the Atlas capsule in the morning and evening. Mahalo for your cooperation!

## Atomic Base Info
**Alert!** Atomic Base is still *unstable*. If Atomic Base crashes, please do not be alarmed. Note that Atomic Base is a side project to simplify Travis CI and building for Atlas and is *not to be used for anything else*.

## Getting Started Guide
Welcome to the wonderful world of Atlas! Atlas is full of easy-to-use features, but you must calibrate Atlas correctly before you take it out for a spin.

🎖 Stable Release:

1. Get into the directory where Atlas will be downloaded.

!! MAKE SURE YOU ARE IN THIS DIRECTORY WHEN CLONING ATLAS !!
** NOTICE: In the future, you won't need to clone Atlas in `/` of your computer. **

```bash
$ cd /
```

2. Get Atlas.
With git:
```bash
$ git clone https://github.com/firebolt-space/atlas.git
```
Or SSH:
```bash
$ git@github.com:firebolt-space/atlas.git
```

3. Install and build Atlas.
```bash
$ cd $PATH_TO_ATLAS
$ bash ./scripts/install.sh
$ bash /atlas/scripts/build.sh --path-to-honeycomb /atlas/src/onboard/components/honeycomb/
```

4. Start Atlas server.
```bash
$ bash /atlas/scripts/atlas.sh start
```

5. Get into the directory where Honeycomb is stored:
```bash
$ cd /atlas/src/onboard/components/honeycomb/
```

6. Start Honeycomb:
```bash
$ python3 server.py
```

7. Congratulations! You have successfully setup Atlas. You can now proceed to the Atlas Tutorials by clicking [here](https://github.com/firebolt-space/atlas/tree/master/docs).

## Examples
!! COMING SOON !!

## Atlas Status

!! FUTURE DEPRECATION WARNING: In the future, we will remove this: !!

| Component    | Status                                    | Submitted By    |  Remarks    |
| ------------ |   -------------                           | -----           | ----        |
| Stage 1  🎖  | ![Build Passing](./svg/build/passing.svg) | aaronhma        | Passed.     |
| Stage 2  🎖  | ![Build Passing](./svg/build/passing.svg) | aaronhma        | Passed.     |
| Stage 3  🎖  | ![Build Passing](./svg/build/passing.svg) | aaronhma        | Passed.     |
| Honeycomb    | ![Build Passing](./svg/build/passing.svg) | rohan           | Passed.     |
| SkyHawk      | ![Build Passing](./svg/build/passing.svg) | aaronhma, rohan | Passed.     |
| Skyforce     | ![Build Passing](./svg/build/passing.svg) | aaronhma, rohan | Passed.     |
| PTurtle      | ![Build Passing](./svg/build/passing.svg) | rohan           | Passed.     |
| Omega        | ![Build Passing](./svg/build/passing.svg) | aaronhma, rohan | Passed.     |
| NightSky     | ![Build Passing](./svg/build/passing.svg) | aaronhma, rohan | Passed.     |

[Information not correct? Contact maintainer to correct](mailto:hi@aaronhma.com)

Thanks for soarin' with Atlas!
-

![Aaron Ma](./svg/signature/aaron.svg)
![Rohan Fernandes](./svg/signature/rohan.svg)
