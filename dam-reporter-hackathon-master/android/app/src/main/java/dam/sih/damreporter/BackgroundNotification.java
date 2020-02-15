package dam.sih.damreporter;

/**
 * Created by tushar on 19/03/18.
 */
import android.app.Notification;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.*;
import android.support.annotation.Nullable;
import android.util.Log;
import android.widget.Toast;


public class BackgroundNotification extends Service{
    private boolean isNetworkAvailable() {
        ConnectivityManager connectivityManager
                = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetworkInfo = connectivityManager.getActiveNetworkInfo();
        return activeNetworkInfo != null && activeNetworkInfo.isConnected();
    }
    public Handler handler = null;
    public static Runnable runnable = null;
    int i = 0;
    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onCreate() {
        handler = new Handler();
        runnable = new Runnable() {
            public void run() {
                Log.e("Network On?:", isNetworkAvailable()?"Yes":"NO");
                if(isNetworkAvailable()) {
                    //call get_notification uri
                    //If the returning JSON contains notifications, then proceed. Else Skip
                    NotificationManager notif = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
                    Notification notify = new Notification.Builder
                            (getApplicationContext()).setContentTitle("Notification")
                            .setContentText("Hello")
                            .setContentTitle("New Notification")
                            .setSmallIcon(R.drawable.ic_pie_chart_black_24dp)
                            .setPriority(Notification.PRIORITY_MAX)
                            .build();
                    notify.flags = Notification.FLAG_AUTO_CANCEL;
                    notify.defaults |= Notification.DEFAULT_SOUND;
                    notif.notify(i, notify);
                    i += 1;
                    handler.postDelayed(runnable, 3600000);
                }
            }
        };
        handler.postDelayed(runnable, 3600000);
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
//        return super.onStartCommand(intent, flags, startId);
        Toast.makeText(this, "Welcome!", Toast.LENGTH_LONG).show();
        return START_STICKY ;
    }

    @Override
    public void onDestroy() {
//        handler.removeCallbacks(runnable); //to remove background process
        Toast.makeText(this, "Service stopped", Toast.LENGTH_LONG).show();
    }
}
