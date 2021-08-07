# dynamic-dns-checker
Wiz research team announced a new class of vulnerabilities on BlackHat & Defcon (for more information go to our [blog](https://duckduckgo.com)). Check if your organization is leaking Dynamic DNS updates to DNS providers or malicious actors. To use the checker, input your top level domain or a sample FQDN of your endpoints

For any question please contact us at [dynamic-dns-leak@wiz.io](mailto:dynamic-dns-leak@wiz.io) or join our [slack group](https://join.slack.com/t/dynamicdnsleak/shared_invite/zt-u7w6mw5d-dYn7KqY1c_z2kyfMrsSpPw), we are happy to help.


## Usage
The code is intended to work as a Lambda function in AWS.  
Do pip - 
```
pip3 install -r requirements.txt -t .
```
Then pack the code in a zip file and your are done;

## Online version
#### We upload an online version for easy use:
#### https://dynamic-dns-checker.tools.wiz.io/