#!/bin/bash

# This script is used to execute the spiders, while storing their output to log files.

# First we store all spiders in an array variable.
spiders=(
	"br_rss"
	"digitallearninglab"
	"geogebra"
	"irights"
	"leifi"
	"mediothek_pixiothek"
	"memucho"
	"merlin"
	"oai_sodis"
	"planet_schule"
	"rlp"
	"serlo"
	"wirlernenonline"
	"wirlernenonline_gsheet"
	"zdf_rss"
	"zoerr"
	"zum"
)

# Print the spiders that wil be executed (for debugging purposes).
#echo ${spiders[@]}

# Make the directory "nohups" if it does not already exist.
mkdir -p nohups

echo 
'
                          (
                           )
                          (
                    /\  .-"""-.  /\
                   //\\/  ,,,  \//\\
                   |/\| ,;;;;;, |/\|
                   //\\\;-"""-;///\\
                  //  \/   .   \/  \\
                 (| ,-_| \ | / |_-, |)
                   //`__\.-.-./__`\\
                  // /.-(() ())-.\ \\
                 (\ |)   '---'   (| /)
                  ` (|           |) `
                    \)           (/
   ____  ________  __              _     __              
  / __ \/ ____/ / / /  _________  (_)___/ /__  __________
 / / / / __/ / /_/ /  / ___/ __ \/ / __  / _ \/ ___/ ___/
/ /_/ / /___/ __  /  (__  ) /_/ / / /_/ /  __/ /  (__  ) 
\____/_____/_/ /_/  /____/ .___/_/\__,_/\___/_/  /____/  
                        /_/                              		
'

# Execute the spiders.
for spider in ${spiders[@]}
do
	echo "Executing $spider spider."
	
	# Execute the spider and save its output to two files: "nohup_SPIDER.out" (individual log) and "nohup.out" (collective logs).
	nohup scrapy crawl ${spider}_spider | tee -a nohups/nohup_${spider}.out nohups/nohup.out >/dev/null & 2>&1	
	
	# Execute the spider in the background. 
	#scrapy crawl ${spider}_spider &
done
echo "Happy crawling! :-)"
