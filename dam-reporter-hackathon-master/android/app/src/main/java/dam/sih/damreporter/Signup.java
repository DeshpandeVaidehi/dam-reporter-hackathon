package dam.sih.damreporter;

import android.Manifest;
import android.content.Context;
import android.content.ContextWrapper;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Build;
import android.provider.MediaStore;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.util.Patterns;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

public class Signup extends AppCompatActivity {
    private String uname, pass, aadhar, mobile, email;
    private EditText et_username, et_pass, et_aadhar, et_mobile, et_email;
    private ImageView et_profile_pic;
    DatabaseHelper db;
    private static int RESULT_LOAD_IMAGE = 1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        db = new DatabaseHelper(this);
        et_profile_pic = (ImageView) findViewById(R.id.userImage);
        et_username = (EditText) findViewById(R.id.user_name);
        et_pass = (EditText) findViewById(R.id.password);
        et_aadhar = (EditText) findViewById(R.id.aadhaar_no);
        et_mobile = (EditText) findViewById(R.id.mobile_no);
        et_email = (EditText) findViewById(R.id.email_id);
        Button s = (Button)findViewById(R.id.signup) ;

        //Get Android permissions
        int PERMISSION_ALL = 1;
        String[] PERMISSIONS = {Manifest.permission.INTERNET, Manifest.permission.ACCESS_COARSE_LOCATION, Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.CAMERA, Manifest.permission.ACCESS_NETWORK_STATE};

        if(!hasPermissions(this, PERMISSIONS)){
            ActivityCompat.requestPermissions(this, PERMISSIONS, PERMISSION_ALL);
        }

        //back to login button
        TextView t = (TextView) findViewById(R.id.back_to_login);
        t.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(Signup.this, MainActivity.class);
                startActivity(i);
            }
        });

        //browse profile picture
        et_profile_pic.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                Intent i = new Intent(
                        Intent.ACTION_PICK,
                        android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);

                startActivityForResult(i, RESULT_LOAD_IMAGE);
            }
        });

        //signup
        s.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                register();
            }
        });
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == RESULT_LOAD_IMAGE && resultCode == RESULT_OK && null != data) {
            Uri selectedImage = data.getData();
            String[] filePathColumn = { MediaStore.Images.Media.DATA };

            Cursor cursor = getContentResolver().query(selectedImage,
                    filePathColumn, null, null, null);
            cursor.moveToFirst();

            int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
            String picturePath = cursor.getString(columnIndex);
            cursor.close();

            Bitmap bitmap = BitmapFactory.decodeFile(picturePath);
            FileOutputStream outStream = null;

            ContextWrapper cw = new ContextWrapper(getApplicationContext());
            File directory = cw.getDir("images", Context.MODE_PRIVATE);
            File mypath=new File(directory,"profile.jpg");

            try {
                outStream = new FileOutputStream(mypath);
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, outStream);
                outStream.flush();
                outStream.close();
            }
            catch(Exception ex){
                Log.e("Exception: ", ex.getMessage());
            }
            ImageView imageView = (ImageView) findViewById(R.id.userImage);
            imageView.setImageBitmap(BitmapFactory.decodeFile(picturePath));
        }
    }
    public void register() {
        uname = et_username.getText().toString().trim();
        pass = et_pass.getText().toString().trim();
        aadhar = et_aadhar.getText().toString().trim();
        mobile = et_mobile.getText().toString().trim();
        email = et_email.getText().toString().trim();
        if(!validate()) {
            Toast.makeText(this, "Failed", Toast.LENGTH_SHORT).show();
        }
        else {
            //send REST API query to server and register this user.
            db.insert("INSERT INTO user_profile(id, aadhaar_no, user_name, password, user_mobile, user_email) VALUES (1, '"+ aadhar +"','"+ uname +"','"+ pass +"','"+ mobile +"','"+ email +"')");
            Intent i = new Intent(Signup.this, MainActivity.class);
            startActivity(i);
        }
    }

    public boolean validate() {
        boolean valid = true;
        if(uname.isEmpty()) {
            et_username.setError("Enter name");
            valid = false;
        }
        if(pass.isEmpty()) {
            et_pass.setError("Enter pass");
            valid = false;
        }
        if(aadhar.isEmpty()) {
            et_aadhar.setError("Enter aadhaar");
            valid = false;
        }
        if(email.isEmpty() || !Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            et_email.setError("Enter valid email");
            valid = false;
        }
        if(mobile.isEmpty() || !mobile.matches("[1-9]{1}[0-9]{9}")) {
            et_mobile.setError("Enter valid mobile no");
            valid = false;
        }
        return valid;
    }
    public  boolean isStoragePermissionGranted() {
        if (Build.VERSION.SDK_INT >= 23) {
            if (checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE)
                    == PackageManager.PERMISSION_GRANTED) {
                Log.v("permission: ","Permission is granted");
                return true;
            }
            else {
                Log.v("permission: ","Permission is revoked");
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
                return false;
            }
        }
        else { //permission is automatically granted on sdk<23 upon installation
            Log.v("permission","Permission is granted");
            return true;
        }
    }
    @Override
    public void onBackPressed() {
        super.onBackPressed();
        return;
    }
    public static boolean hasPermissions(Context context, String... permissions) {
        if (context != null && permissions != null) {
            for (String permission : permissions) {
                if (ActivityCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED) {
                    return false;
                }
            }
        }
        return true;
    }
}