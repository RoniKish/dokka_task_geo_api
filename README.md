# dokka_task_geo_api

1. Open a mongoDb service locally: <br/>
  a. download mongodb from https://www.mongodb.com/ and install <br/>
  b. go to C:\Program Files\MongoDB\Server\<version installed>\bin <br/>
  c. open cmd and run "mongod" <br/>

2. Run the python flask api: <br/>
  a. Pip install the following: pymongo, pandas, flask <br/>
  b. Run the app.py script <br/>
 
3. Run the POST/GET request via Curl:
  a. Make sure you have Curl and node.js <br/>
  b. for Post request run: curl -F csv_file=@<location_of_csv_file> http://127.0.0.1:5000/api/getAddresses <br/>
    for example: curl -F csv_file=@C:\dokkaAssignment\myCsvFile.csv http://127.0.0.1:5000/api/getAddresses <br/>
  c. for the get request take the result_id you got in the post and run: <br/>
    curl http://127.0.0.1:5000/api/getResult?result_id=<your_result_id> <br/>
    for example: curl http://127.0.0.1:5000/api/getResult?result_id=5f8b18248e0217ef089f0a64 <br/>


 * Note which ports the servers runs on although the default for flask is 5000 and mongodb is 27017, it might be different and you will need to change
 the app.py or Curl command accordingly 
