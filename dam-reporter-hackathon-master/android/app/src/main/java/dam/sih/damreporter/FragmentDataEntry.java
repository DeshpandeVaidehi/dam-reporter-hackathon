package dam.sih.damreporter;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.location.LocationManager;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Handler;
import android.provider.MediaStore;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.widget.CardView;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.ImageView;
import android.location.Location;
import android.location.LocationListener;
import android.widget.LinearLayout;
import android.widget.Spinner;

import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.util.ArrayList;

/**
 * Created by tushar on 18/03/18.
 */

public class FragmentDataEntry extends Fragment implements LocationListener {
    private int image_count = 0;
    View view;
    FloatingActionButton btn;
    FloatingActionButton vbtn;
    ImageView img;
    Location location;
    ArrayList<Bitmap> imag_array;
    String send_string_image [] = new String[5];
    LinearLayout imageLayout;
    CardView cv;
    private static double lat = 0.0;
    private static double lon = 0.0;
    private static double alt = 0.0;
    private static double speed = 0.0;

    String toInt(String s){
//        <string-array name="two_choices">
//        <item>NO</item>
//        <item>YES</item>
//    </string-array>
//
//    <string-array name="three_choices">
//        <item>Best</item>
//        <item>Average</item>
//        <item>Worst</item>
//    </string-array>
        if (s.equals("NO")){
            return "0";
        }
        else if(s.equals("YES")){
            return "1";
        }
        else if(s.equals("BEST")){
            return "0";
        }
        else if(s.equals("Average")){
            return "1";
        }
        else if(s.equals("Worst")){
            return "2";
        }
        else{
            return "0";
        }
    }
    private static class Download extends AsyncTask<String, Void, String> {
        @Override
        protected void onPostExecute(String result) {
        }

        @Override
        protected String doInBackground(String... params) {

            HttpURLConnection con = null;
            try {
                URL url = new URL("http://192.168.1.102:5000/save_data");
                con = (HttpURLConnection)url.openConnection();
                con.setRequestMethod("POST");
                con.setRequestProperty("USER-AGENT", "Mozilla/5.0");
                con.setRequestProperty("ACCEPT-LANGUAGE", "en-US,en;0.5");
                con.setRequestProperty("Content-type", "application/json");
                con.setDoOutput(true);
                DataOutputStream dStream = new DataOutputStream(con.getOutputStream());
                dStream.writeBytes(params[0]);

                Log.d("query", params[0]);
                int responseCode = con.getResponseCode();
                Log.d("hey: ", String.valueOf(responseCode));
            } catch (Exception e) {
                e.printStackTrace();
            }
            return "Executed!";
        }
    }
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.data_entry, container, false);

        imageLayout = (LinearLayout) view.findViewById(R.id.imageview_layout);
        imag_array = new ArrayList<Bitmap>();
        img = (ImageView) view.findViewById(R.id.load_image);
//        result_video = (VideoView)view.findViewById(R.id.videoView);
        btn = (FloatingActionButton) view.findViewById(R.id.open_camera);
        vbtn = (FloatingActionButton) view.findViewById(R.id.open_video);
        cv = view.findViewById(R.id.send_data_to_server);
        final DatabaseHelper db = new DatabaseHelper(view.getContext());

        final Spinner dam_spinner = view.findViewById(R.id.dam_spinner);
        final Spinner seepage_spinner = view.findViewById(R.id.seepage_spinner);
        final Spinner crack_spinner = view.findViewById(R.id.cracks_spinner);
        final Spinner errosion_spinner = view.findViewById(R.id.errosion_spinner);
        final Spinner gate_spinner = view.findViewById(R.id.gate_spinner);
        final Spinner sluice_gate_spinner = view.findViewById(R.id.sluice_gate_spinner);
        final Spinner energy_dissipator_spinner = view.findViewById(R.id.energy_dissipator_spinner);
        final Spinner instrument_spinner = view.findViewById(R.id.instrument_spinner);
        final EditText max_flood_handled = view.findViewById(R.id.max_flood);
        final EditText comment = view.findViewById(R.id.comment);



        cv.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                //192.168.1.102
                //send data to aws server
                final String data = "{\"aadhaar_no\": \""+ db.getAadhaarNumber()
                        +"\", \"dam_name\": \""+ dam_spinner.getSelectedItem()
                        +"\", \"descrip\": \""+ comment.getText()
                        +"\", \"seepage\": \""+ toInt(seepage_spinner.getSelectedItem().toString())
                        +"\", \"cracks\":\""+ toInt(crack_spinner.getSelectedItem().toString())
                        +"\", \"erosion\":\""+ toInt(errosion_spinner.getSelectedItem().toString())
                        +"\", \"gates_condition\":\""+ toInt(gate_spinner.getSelectedItem().toString())
                        +"\", \"sluice_gates_condition\":\""+ toInt(sluice_gate_spinner.getSelectedItem().toString())
                        +"\", \"max_flood_handled\":\""+ max_flood_handled.getText().toString()
                        +"\", \"energy_dissipator_condition\":\""+ toInt(energy_dissipator_spinner.getSelectedItem().toString())
                        +"\", \"instrument_condition\":\""+ toInt(instrument_spinner.getSelectedItem().toString())
                        +"\", \"latitude\": \""+ String.valueOf(lat)
                        +"\", \"longitude\": \""+ String.valueOf(lon)
                        +"}\n" +
                        "\n"; //data to post
//                Log.d("data: " , data);
                new Download().execute(new String[]  {data});
            }

        });



        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                try {
                    LocationManager locationManager;
                    String context = Context.LOCATION_SERVICE;
                    locationManager = (LocationManager) getActivity().getSystemService(context);
                    String provider = LocationManager.GPS_PROVIDER;
                    if (ActivityCompat.checkSelfPermission(view.getContext(), Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(view.getContext(), Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                        // TODO: Consider calling
                        //    ActivityCompat#requestPermissions
                        // here to request the missing permissions, and then overriding
                        //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                        //                                          int[] grantResults)
                        // to handle the case where the user grants the permission. See the documentation
                        // for ActivityCompat#requestPermissions for more details.
                        return;
                    }
                    location = locationManager.getLastKnownLocation(provider);
                    lon = location.getLongitude();
                    lat = location.getLatitude();
                    System.out.println("lon : " + lon + " " +lat);
                }
                catch (Exception e) {
                    System.out.println("loaction exception : " + e);
                }
                Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                startActivityForResult(intent,0);
            }
        });

        vbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent takeVideoIntent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
                if (takeVideoIntent.resolveActivity(getActivity().getPackageManager()) != null) {
                    startActivityForResult(takeVideoIntent, 1);
                }
            }
        });
        return view;
    }

    public String getStringImage(Bitmap bm) {
        ByteArrayOutputStream ba = new ByteArrayOutputStream();
        bm.compress(Bitmap.CompressFormat.PNG, 90, ba);
        byte[] by = ba.toByteArray();
        String encod = Base64.encodeToString(by, Base64.DEFAULT);
        return encod;
    }



    public  FragmentDataEntry(){}

    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == 0 && resultCode == Activity.RESULT_OK) {
            Bitmap photo = (Bitmap) data.getExtras().get("data");

            ImageView image = new ImageView(view.getContext());
            image.setLayoutParams(new android.view.ViewGroup.LayoutParams(180,160));
            image.setMaxHeight(40);
            image.setMaxWidth(40);
            imageLayout.addView(image);
            image.setImageBitmap(photo);
            imag_array.add(photo);
            img.setImageBitmap(photo);


            send_string_image[image_count]=getStringImage( ( (BitmapDrawable) img.getDrawable( ) ).getBitmap( ) );
            System.out.println("Send this string " + send_string_image[image_count]);
            image_count++;
        }
        if (requestCode == 1 && resultCode == Activity.RESULT_OK) {
            //System.out.println("in videooooo");
            Uri videoUri = data.getData();
            //upload video
        }
    }

    @Override
    public void onLocationChanged(Location location) {
        lat = location.getLatitude();
        lon = location.getLongitude();
        alt = location.getAltitude();
        speed = location.getSpeed();
    }

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {

    }

    @Override
    public void onProviderEnabled(String provider) {

    }

    @Override
    public void onProviderDisabled(String provider) {

    }
}
