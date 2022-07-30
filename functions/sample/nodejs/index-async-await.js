/**
 * Get all dealerships
 */
const fs = require('fs');
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
      
      try {
        if (params.state){
          console.log("params.state is included")
          let dealers = await cloudant.postFind({
            db: 'dealerships',
            selector: { "state": params.state},
          });
        } else{
          console.log("params.state is NOT included")
          let dealers = await cloudant.postAllDocs({
            db: 'dealerships',
            includeDocs: true,
          });
        }
        
        if(dealers.result.total_rows == 0){
          return {error : "404: The state does not exist"}
        }

        console.log(dealers.result)
        return dealers.result;

      } catch (error) {
          return { error : "500: Something went wrong on the server" };
      }
}

let rawdata = fs.readFileSync('../../.creds-sample.json');
let params = JSON.parse(rawdata);

console.log(main(params))

