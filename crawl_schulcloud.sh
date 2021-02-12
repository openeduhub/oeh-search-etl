#!/bin/bash
# Please execute this script in the following way:
# env mailx_recipients="e-mail1 e-mail2 ... e-mailN" bash crawl_schulcloud.sh
# TIP: This is how you could include it in a cronjob as well.

working_dir=/root/oeh-search-etl-branches/master_cron/oeh-search-etl
cd $working_dir
source .venv/bin/activate

spiders=(
        "mediothek_pixiothek_spider"
        "merlin_spider"
        "oeh_spider"
)

print_logo=false
show_spider_output=false

# dev, prod | WARNING: It assumes the existence of .env.dev and .env.prod in the converter/ directory. Please refer to
# .env.example for reference environmental variables.
environment="dev"
if [[ $# -eq 0 ]] ; then
  echo 'No environment specified as an argument, defaulting to dev.'
else
  environment=$1
  echo "The environment ${environment} was specified."
fi
if ! test -f "converter/.env.$environment"; then
  echo "converter/.env.$environment does not exist. Exiting..."
  exit 2
else
  echo "Copying converter/.env.$environment to converter/.env"
  cp "converter/.env.$environment" "converter/.env"
fi

# Set to true only when $show_spider_output = false. Please prefer to keep to false, at least for crawlings against the
# production machine. (It causes the execution to run in the background and, thus, multiple spiders will run.)
use_nohup=false

# Make the directory "nohups" if it does not already exist.
mkdir -p nohups

###################################
if [ "$print_logo" = true ] ; then
    echo '
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
                        /_/'
fi


# Execute the spiders.
for spider in ${spiders[@]}
do
        echo "Executing $spider spider."

        # Execute the spider
        if [ "$show_spider_output" = true ] ; then
          # ... , save its output to "nohup_SPIDER.out", AND print stdout and stderr.
          scrapy crawl ${spider} -a resetVersion=true | tee -a nohups/nohup_${spider}.out
        elif [ "$show_spider_output" = false ] && [ "$use_nohup" = true ]; then
          # Execute the spider and save its output to two files: "nohup_SPIDER.out" (individual log) and "nohup.out"
          # (collective logs).
          nohup scrapy crawl ${spider} -a resetVersion=true | tee -a nohups/nohup_${spider}.out \
                nohups/nohup.out >/dev/null 2>&1 &
        else # elif [ "$show_spider_output" = false ] && [ "use_nohup" = false ]; then
          # ... and save its output to "nohup_SPIDER.out".
          scrapy crawl ${spider} -a resetVersion=true &> nohups/nohup_${spider}.out
        fi

        echo "Finished execution of $spider spider"

        # If the env var $mailx_recipients is set, please send the report to it. (Could be multiple addresses separated
        # via a white spaces). e.g., export mailx_recipients="mail1@hpi.de mail2@hpi.de ... mailN@hpi.de"
        if [ ! -z ${mailx_recipients+x} ]; then
          echo "Gathering report for $spider spider"

          spider_output=$(tail -n 40 nohups/nohup_${spider}.out)
          # Remove everything before and including the string 'INFO: Closing spider (finished)'
          spider_output_statistics="*** Report for ${spider} crawling ***"${spider_output#*"INFO: Closing spider (finished)"}
          echo "$spider_output_statistics" | mailx -s "${spider} has just finished crawling." ${mailx_recipients}

          echo "Report sent for $spider spider"
        fi
done

echo "Finished with all spiders! :-)"