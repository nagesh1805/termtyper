# termtyper

### `termtyper` is a terminal based typing practice command-line application written in Python3 using curses library. It can run on mac/linux/unix and also windows.

### Installation
> `pip install termtyper`

**Note:** 
1. Please install latest python3(version >= 3.7) from www.python.org (with pip), though python come with your system. There are some issues (like permission errors) with python that comes with system by default (as it is insatlled system level not user level). DO NOT UNININSTALL the python that came with your system by default. Just install one latest python at user level.
2. On windows termtyper works with windows-terminal but one issue is, it crashes when we resize the terminal. So try not to resize the terminal after application got started (windows-terminal can be installed from microsoft store).
3. If you are mac user and get the SSL: CERTIFICATE_VERIFY_FAILED error for the first time you open application, then goto applications folder, and find the python folder and double click the file Install Certificates.command. then you are good to go.



### Usage of command
Just type `termtyper` on terminal to start application

usage: termtyper [-h] [--version] [--upgrade]

### Features
- Onscreen keyboard to see typing effect and has option to toggle onscreen keyboard.
- Can be customized the typing test challenge with 1 minute, 2 minute, 3 minute, 5 minute,10 minute and 15 minute.
- Can be customized the text for the typing test with English(12 options) or Programming languages (12 languages)
- Timer starts when first key is pressed and has option to pause/resume the typing test.
- Maintains performance statistics and shows Histogram for typing speed.
- Very much like GUI application despite the fact that the application is terminal based.

[![termtyper](https://img.youtube.com/vi/nPjmML7n2ag/0.jpg)](https://www.youtube.com/watch?v=nPjmML7n2ag)

### Versions
#### 2.0.5
> Fixed Bug! (crashing termtytper when we press some unwanted keys(like Insert, DELETE))
#### 2.0.4
> Updated setup.py (chnaged minimum python version requirement from 3.6  to 3.7)
#### 2.0.3
> Fixed Bug in staticstics(date key Error)
#### 2.0.2
> Fixed Bug in correct word count and wrong word count calculation
#### 2.0.1
> Fixed mistakes in the text of movie scripts in the English Language Category
#### 2.0.0
> **Added features:** 
>>1. Maintains performance statistics (All-time, Month, Week, Day) with total time (in minutes), top speed (wpm), and average speed (wpm) and also display the Histogram for typing speed.
>>2. Added 9 language options (famous movie scripts) in the English language category while removing 3 languages options (Top 50 words, Top 100 Words, and Top 300 words).
>>3. Shows new updates to upgrade (when available).
#### 1.1.x
> **Added features and bug fixes:** 
>> 1. Bug fix: install_requires keyword in setup.py(now windows-curses package will be autometically installed as required package for windows system)
>> 2. Added command line argument feature to upgrade (if latest version available) and for getting version information
>> 3. Pause/resume the typing test feature has been added in this version.
##### 1.0.0
> First version

### Languages

The following languages are available

#### English
>1. Top 200 words
>2. Too 500 words
>3. Top 1000 words
>4. Toy Story(1-4)
>5. Srek (1-4)
>6. Happy Feet(1-2)
>7. Kungfu Panda (1-3)
>8. Frozen (1-2)
>9. Moana
>10. Harry Potter (1-3)
>11. Lord of The Rings (1-3)
>12. Titanic


#### Programming 
>1. C/CPP
>2. C#
>3. Java
>4. Python
>5. Swift
>6. HTML
>7. Java Script
>8. GO
>9. PHP
>10. Ruby
>11. Kotlin
>12. Rust

### Challanges
The following practice challenges available
>- 1 minute test
>- 2 minute test
>- 3 minute test
>- 5 minute test
>- 10 minute test
>- 15 minute test
