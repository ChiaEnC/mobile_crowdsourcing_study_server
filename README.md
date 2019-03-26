# mobile_crowdsourcing_study
This project explores users' motivation and contexual factors for performing mobile crowdsourcing tasks, 
which is supervised under [Yung Ju Chang](https://www.armuro.info/) at MUILAB NCTU.

This tool is the revised version of [Minuku](https://github.com/minuku), which can collect contextual data, including phone log data and ESM questionnaires.

For more info, please visit the above links. 

# mobile_crowdsourcing_study_server
* server.py 
    * handles android dump data 
    * search routes : search_all_detail & search_all_count
    * for this project client side used : VolleySingleton to transfer data asynchronously 
* server.js 
  * handles android MIME type data (huge chunks of data)
  * hapi.js plug-in 
  * for this project client side used : Retrofit to transfer videos asynchronously 

