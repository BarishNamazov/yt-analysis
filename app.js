const API_KEY = "AIzaSyBKb7k3oddL9kEiYZO0zIwUPrV5tdJKVho"; // please don't abuse our key :(
const CLIENT_ID = "671626616241-ntpkkcdovesel98iqli5dp7uipfe2ani.apps.googleusercontent.com";
const SCOPE = "https://www.googleapis.com/auth/youtube.readonly";
const YT_API = "https://youtube.googleapis.com/youtube/v3/";

let client;
let access_token;

function initClient() {
  client = google.accounts.oauth2.initTokenClient({
    client_id: CLIENT_ID,
    scope: SCOPE,
    callback: (tokenResponse) => {
      access_token = tokenResponse.access_token;
      console.log("access_token=", access_token);
    },
  });
}

function getToken() {
  client.requestAccessToken();
}
function revokeToken() {
  google.accounts.oauth2.revoke(access_token, () => {console.log('access token revoked')});
}

function get(resource, queries) {
    queries["key"] = API_KEY;
    const query_list = [];
    for (const [query, value] of Object.entries(queries)) {
        query_list.push(`${query}=${value}`);
    }
    const url = YT_API + resource + "?" + query_list.join("&");
    return fetch(url, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${access_token}`
        }
    });
}

function getChannels() {
    let queries = {
        "part": "snippet,contentDetails,statistics",
        "mine": "true"
    };
    get('channels', queries).then(res => res.json()).then(res => console.log(res));
}