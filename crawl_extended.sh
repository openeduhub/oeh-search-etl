#!/bin/bash
# Please execute this script in the following way:
# bash crawl_extended.sh --arg1 val1 --arg2 "val2 val3"
# TIP: This is how you could include it in a cronjob as well.

##############################
# STEP 1: Declaring variables.

working_dir=$(pwd)

# Causes the execution to run in the background and, thus, multiple spiders will run.
parallel_execution=false

## Main variables
spiders=(
        "mediothek_pixiothek_spider"
        "merlin_spider"
        "oeh_spider"
        "sodix_spider"
)

# dev, prod | WARNING: It assumes the existence of .env.dev and .env.prod in the converter/ directory. Please refer to
# .env.example for reference environmental variables.
environment="dev"

############################
# STEP 2: Parsing arguments.
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -e|--environment) environment="$2"; shift ;;
        -s|--spiders) spiders_str=("$2"); spiders=($spiders_str); shift ;; # Convert a double quoted value to an array.
        -m|--mailx_recipients) mailx_recipients=("$2"); shift ;;
        -w|--working_dir) working_dir="$2"; shift;;

        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "working_dir=$working_dir";
echo "environment=$environment";
echo "spiders=${spiders[@]}";
echo "mailx_recipients=$mailx_recipients";

venv_bin_dir="${working_dir}/.venv/bin"

##############################
# STEP 3: Prepare environment.
cd $working_dir || exit
source "${working_dir}/.venv/bin/activate"; # does not seem to have any effect

if ! test -f "converter/.env.$environment"; then
  echo "converter/.env.$environment does not exist. Exiting..."
  exit 2
else
  echo "Copying converter/.env.$environment to converter/.env"
  cp "converter/.env.$environment" "converter/.env"
fi

# Make the directory "nohups" if it does not already exist.
mkdir -p nohups

##############################
timestamp=$(date +"%Y_%m_%d_%H_%M")
# STEP 4: Execute the spiders.
for spider in ${spiders[@]}
do
        echo "Started execution of $spider spider."

        # Execute the spider
        if [ "$parallel_execution" = false ] ; then
          # Save its output to "nohup_SPIDER.out".
#          scrapy crawl ${spider} -a resetVersion=true &> nohups/nohup_${spider}_${timestamp}.out
          ${venv_bin_dir}/scrapy crawl ${spider} -a resetVersion=true | tee -a nohups/nohup_${spider}_${timestamp}.out \
                nohups/nohup_${timestamp}.out 2>&1
        else
          # Save its output to "nohup_SPIDER.out" (individual log) and "nohup.out". (collective logs)
          nohup ${venv_bin_dir}/scrapy crawl ${spider} -a resetVersion=true | tee -a nohups/nohup_${spider}_${timestamp}.out \
                nohups/nohup_${timestamp}.out >/dev/null 2>&1 &
        fi

        echo "Finished execution of $spider spider"

        # If the env var $mailx_recipients is set, please send the report to it. (Could be multiple addresses separated
        # via a white spaces). e.g., export mailx_recipients="mail1@gmail.de mail2@gmail.de ... mailN@gmail.de"
        if [ ! -z ${mailx_recipients+x} ]; then
          echo "Gathering report for $spider spider"

          spider_output=$(tail -n 500 nohups/nohup_${spider}_${timestamp}.out)
          # Remove everything before and including the string 'INFO: Closing spider (finished)'
          spider_output_statistics="*** Report for ${spider} crawling in ${environment} environment ***"${spider_output#*"INFO: Closing spider (finished)"}
          echo "$spider_output_statistics" | mailx -s "${spider} has just finished crawling in ${environment}." ${mailx_recipients}

          echo "Report sent for $spider spider"
        fi
done

echo "Finished with all spiders! :-)"
