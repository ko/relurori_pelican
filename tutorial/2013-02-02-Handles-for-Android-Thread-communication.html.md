Title: Handles for Android Thread communication
Date: 2013/02/02 14:39
Author: Ken Ko
Tags: android, thread, handle

This is a brief overview of thread communication in an Android 
application. 

In the MainActivity class, my code is structured as seen below.
Note that this is effectively pseudo code, except for when it isn't.

<code>
    class MainActivity extends Activity {
        ...
        public Handler mHandler;
        ...
        onCreate() {
            ...
            setupBgThread();
            ...
        }

        private void setupBgThread() {
            mHandler = new Handler(Looper.getMainLooper()) {

                @Override
                public void handleMessage(Message m) {
                    Log.v(_tag, "main: " + m.what);
                    if (m.what == 3) {
                        Log.v(_tag, "m.what=" + m.what);
                    }
                }
            };

            UpdateThread mThread = new UdateThread(getBaseContext(), 
                                                   mHandler,
                                                   "UpdateThread");
            mThread.start();
            ...
            Message msg = new Message();
            msg.what = mThread.handler.START_EVENT;
            mThread.handler.sendMessage(msg);
        }
    }
</code>

So, what we have is a handler that listens for events from the associated
thread, UpdateThread. When UpdateThread sends a message where _msg.what_
is set to _3_, we log a message. 

From the UpdateThread side, we have:

<code>
    class UpdateThread extends Thread {
        UpdateThreadHandler handlerFromCaller;
        Handler handlerToCaller;
        ...
        public UpdateThread(Context context, Handler handler, String name) {
            super(name);
            handlerToCaller = handler;
            handlerFromCaller = new handlerFromCaller(...)
            ...
        }
        ...
        @Override
        public void run() {
            super.run();
            ... 
            Looper.prepare();
            Looper.loop();
            ...
        }
        ...
        sendToUI(Message msg) {
            handlerToCaller.sendMessage(msg);
        }
    }
</code>

Note that in the _run_ function, there is additional logic recommended
to handle _onPause()_ and _onResume()_ calls. That is, we need to 
gracefully manage this thread for when the application is put in the
background. Users sometimes want to switch applications. 

The UpdateThreadHandler looks something like this: 

<code>
    class UpdateThreadHandler extends Handler {
        ...
        @Override
        public void handleMessage(Message msg) {
            switch (msg.what) {
            ...
            }
        }
    }
</code>

Seems pretty simple, after the fact. There's also a chance at using
a _HandlerTHread_ which does the Looper work for you. This may be
more verbose, but also pretty straightforward to grok. 
