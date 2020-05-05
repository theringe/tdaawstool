-------------------------------------
Token Prerequirement:

1. Registrate a develop account from TDA via https://developer.tdameritrade.com/apis

2. Create a new app from your develop account (specify your callback URL to http://localhost:8080) and get the Consumer Key (a.k.a. client id)

3. Open this URL in your browser (please change X to your client id you've gained before) with your login credential and get a callback URL (It is normal which the URL could not be loaded, all we need is the URL itself)
https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8080&client_id=X%40AMER.OAUTHAP

4. Decode your callback URL (e.g., https://localhost:8080/?code=XXX) using urldecode function and get XXX for example
-------------------------------------
System Prerequirement:

1. Install Anaconda3 / redis-cli on your system.

2. Install redis / websocket-client / websocket-server / boto3 via pip.

3. Launch redis-cli and set refresh_token "XXX" you've gained in the previous step

4. For steps 2-4 from Token Prerequirement and steps 3 from System Prerequirement, you have to do it every 2 months due to token expiration
-------------------------------------
Installation:

1. Download this repository

2. symbol.json: change permission to 666

3. tda_access_token_tool.py: follow the comments, change client_id

4. tda_str.sh: change permission to 755, follow the comments, change the paths

5. tda_streaming.py: follow the comments, change KINESIS_STREAM_NAME / REGION_NAME

6. Set the crontab as a non-root user
0,20,40 * * * * cd /path/to/your/tdaawstool ; /path/to/your/anaconda3/bin/python ./tda_access_token_tool.py > /dev/null
0 1 * * *       cd /path/to/your/tdaawstool ; /path/to/your/anaconda3/bin/python ./nasdaq_symbol.py         > /dev/null
0 2 * * *       cd /path/to/your/tdaawstool ; ./tda_str.sh > /dev/null

7. Run the command (Just one time)
cd /path/to/your/tdaawstool ; /path/to/your/anaconda3/bin/python ./tda_access_token_tool.py
cd /path/to/your/tdaawstool ; /path/to/your/anaconda3/bin/python ./nasdaq_symbol.py
cd /path/to/your/tdaawstool ; ./tda_str.sh
-------------------------------------
