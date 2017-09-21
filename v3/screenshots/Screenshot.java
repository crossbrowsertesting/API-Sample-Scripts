import java.util.List;

import org.apache.commons.codec.binary.Base64;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class Screenshot {
	private String username;
	private String authkey;
	
	public Screenshot(String username, String authkey) {
		this.username = username;
		this.authkey = authkey;
	}
	
	public void startScreenshot(String url, String browserList) {
		String apiUrl = "https://crossbrowsertesting.com/api/v3/screenshots/";
		String payload = "{\"url\": \"" + url + "\", \"browser_list_name\": \"" + browserList + "\"}";
		String resp = makeRequest("POST",apiUrl,payload);
		System.out.println(resp);
	}
	
	private String makeRequest(String requestMethod, String apiUrl, String payload) {
		URL url;
		String auth = "";
		String resp = "";

        if (this.username != null && this.authkey != null) {
            auth = "Basic " + Base64.encodeBase64String((this.username+":" + this.authkey).getBytes());
        }
        try {
            url = new URL(apiUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod(requestMethod);
            conn.setDoOutput(true);
            conn.setRequestProperty("Authorization", auth);
            conn.setRequestProperty("Content-Type", "application/json");
            OutputStreamWriter osw = new OutputStreamWriter(conn.getOutputStream());
            osw.write(payload);
            osw.flush();
            osw.close();
            conn.getResponseMessage();
            BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            String output = "";
            while((output = br.readLine()) != null) {
            	resp += output;
            }
            return resp;
        } catch (Exception e) {
        	System.out.println(e.getMessage());
        }
        return resp;
	}
	
	public static void main(String[] args) {
		String username = "chase@crossbrowsertesting.com";
		String authkey = "<notmyauthkey>";
		Screenshot st = new Screenshot(username, authkey);
		st.startScreenshot("https://www.crossbrowsertesting.com", "Popular Browsers");
		
	}
}
