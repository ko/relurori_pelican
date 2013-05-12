Title: Android leaked ServiceConnection
Date: 2012/12/16 23:19
Author: Ken Ko
Tags: android

Whenever I hit this particular code path, there are endless logcat errors.
For context, this is hit only during an *ListView.OnItemClickListener* or
a Button's *onClick* handler. 

The code
========
<pre>
@Override
    public String JSONGet(String... arg0) {
        String line = "";
        String ret = "";
        String url = arg0[0]; // Added this line
        
        HttpClient client = new DefaultHttpClient();
        HttpGet get = new HttpGet(url);
        
        try {
            HttpResponse response = client.execute(get);

            StatusLine statusLine = response.getStatusLine();
            int statusCode = statusLine.getStatusCode();

            if (statusCode == 200) { // Ok
                BufferedReader rd = new BufferedReader(
                                        new InputStreamReader(
                                            response.getEntity().getContent()
                                        ));

                while ((line = rd.readLine()) != null) {
                    ret += line;
                }
            }
            
            // Close the HTTP client
            get.abort();
            client.getConnectionManager().shutdown();
            
        } catch (ClientProtocolException e) {
            ret = "client protocol exception";
            e.printStackTrace();
        } catch (IOException e) {
            ret = "io exception";
            e.printStackTrace();
        }

        return ret;
    }
</pre>

The error
=========
<pre>
12-20 07:49:28.251: E/StrictMode(661): null
12-20 07:49:28.251: E/StrictMode(661): android.app.ServiceConnectionLeaked: Service com.android.exchange.ExchangeService has leaked ServiceConnection com.android.emailcommon.service.ServiceProxy$ProxyConnection@40cfaab0 that was originally bound here
12-20 07:49:28.251: E/StrictMode(661):  at android.app.LoadedApk$ServiceDispatcher.<init>(LoadedApk.java:969)
12-20 07:49:28.251: E/StrictMode(661):  at android.app.LoadedApk.getServiceDispatcher(LoadedApk.java:863)
12-20 07:49:28.251: E/StrictMode(661):  at android.app.ContextImpl.bindService(ContextImpl.java:1418)
12-20 07:49:28.251: E/StrictMode(661):  at android.app.ContextImpl.bindService(ContextImpl.java:1407)
12-20 07:49:28.251: E/StrictMode(661):  at android.content.ContextWrapper.bindService(ContextWrapper.java:473)
12-20 07:49:28.251: E/StrictMode(661):  at com.android.emailcommon.service.ServiceProxy.setTask(ServiceProxy.java:157)
12-20 07:49:28.251: E/StrictMode(661):  at com.android.emailcommon.service.ServiceProxy.setTask(ServiceProxy.java:145)
12-20 07:49:28.251: E/StrictMode(661):  at com.android.emailcommon.service.AccountServiceProxy.getDeviceId(AccountServiceProxy.java:116)
12-20 07:49:28.251: E/StrictMode(661):  at com.android.exchange.ExchangeService.getDeviceId(ExchangeService.java:1249)
12-20 07:49:28.251: E/StrictMode(661):  at com.android.exchange.ExchangeService$7.run(ExchangeService.java:1856)
12-20 07:49:28.251: E/StrictMode(661):  at com.android.emailcommon.utility.Utility$2.doInBackground(Utility.java:551)
12-20 07:49:28.251: E/StrictMode(661):  at com.android.emailcommon.utility.Utility$2.doInBackground(Utility.java:549)
12-20 07:49:28.251: E/StrictMode(661):  at android.os.AsyncTask$2.call(AsyncTask.java:287)
12-20 07:49:28.251: E/StrictMode(661):  at java.util.concurrent.FutureTask.run(FutureTask.java:234)
12-20 07:49:28.251: E/StrictMode(661):  at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1080)
12-20 07:49:28.251: E/StrictMode(661):  at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:573)
12-20 07:49:28.251: E/StrictMode(661):  at java.lang.Thread.run(Thread.java:856)
</pre>

Not sure what this is; will have to look into it in the future. Some
people, though, seem to suggest that this is harmless (not sure how).
