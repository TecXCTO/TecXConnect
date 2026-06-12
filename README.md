# TecXConnect
TecX Connect

```
Automating Renewals: Let's Encrypt certificates expire every 90 days. You can automate renewals by adding a Linux Cron Job (crontab -e) that runs this script quietly in the background on the 1st of every month:0 2 1 * * /path/to/setup-certificates.sh > /dev/null 2>&1
```
