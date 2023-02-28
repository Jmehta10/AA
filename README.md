# html_Inj_wayback_automation
- Put all targets(domain names) in target.txt without http/https. for ex.(blindf.com)</br>
- Create an empty urls.txt file in the same folder</br>
# Usage:
- Run the script</br>
  python3 run.py </br>
# How script works:
- The script will take 1 target at a time from the target.txt and save all wayback urls in the urls.txt file. Then this script
  will call html_injection_check.py file and perform attack.
- This process will be continued until reaches End of line of the target.txt</br>
