package dam.sih.damreporter;

import android.content.Context;
import android.content.ContextWrapper;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;

/**
 * Created by tushar on 18/03/18.
 */

public class FragmentProfile extends Fragment {
    View view;
    DatabaseHelper db;
    public FragmentProfile(){

    }

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.user_profile, container, false);
        Button signOut = (Button) view.findViewById(R.id.sign_out);
        db = new DatabaseHelper(view.getContext());
        TextView uname = view.findViewById(R.id.userName);
        uname.setText(db.getUserName());

        TextView aadhaar = view.findViewById(R.id.aadharNumber);
        aadhaar.setText("Aadhaar No.: " + String.valueOf(db.getAadhaarNumber()));

        TextView mobile = view.findViewById(R.id.phoneNumber);
        mobile.setText(String.valueOf(db.getMobileNumber()));

        TextView email = view.findViewById(R.id.emailId);
        email.setText(db.getEmailId());

        ImageView userProfile = view.findViewById(R.id.userImage);

        try {
            ContextWrapper cw = new ContextWrapper(view.getContext());
            File directory = cw.getDir("images", Context.MODE_PRIVATE);
            File mypath = new File(directory,"profile.jpg");
            Bitmap b = BitmapFactory.decodeStream(new FileInputStream(mypath));
            userProfile.setImageBitmap(b);
        }
        catch (FileNotFoundException e)
        {
            e.printStackTrace();
        }

        signOut.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new DatabaseHelper(v.getContext()).trucate("user_profile");
                Intent intent = new Intent(getActivity(), MainActivity.class);
                startActivity(intent);
            }
        });
        return view;
    }

}