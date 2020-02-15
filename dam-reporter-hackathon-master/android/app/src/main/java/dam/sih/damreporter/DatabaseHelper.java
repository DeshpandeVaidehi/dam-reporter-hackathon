package dam.sih.damreporter;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.text.Editable;
import android.util.Log;

/**
 * Created by vaidehi on 18/3/18.
 */

public class DatabaseHelper extends SQLiteOpenHelper {
    private static final String database_name = "myDB";
    private static final String notify = "notifications";
    private static final String user = "user_profile";
    SQLiteDatabase db;
    DatabaseHelper(Context context) {
        super(context, database_name, null, 1);
        db = this.getWritableDatabase();
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE IF NOT EXISTS '" + notify + "' (id INTEGER PRIMARY KEY, notification TEXT)");
        db.execSQL("CREATE TABLE IF NOT EXISTS '" + user + "' (id INTEGER, aadhaar_no TEXT PRIMARY KEY, password TEXT, user_name TEXT, user_mobile TEXT, user_email TEXT )");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        onCreate(db);
    }

    boolean isRegistered() {
        //call aws and see if this user exists
        //and get user profile
        Cursor data = db.rawQuery("SELECT COUNT(*) as total FROM " + user, null);
        data.moveToFirst();
//        Log.d("Users: ", "Num Users: " + data.getInt(data.getColumnIndex("total")));
        int isReg = data.getInt(data.getColumnIndex("total"));
        data.close();
        return isReg == 1;
    }

    void insert(String s) {
        db.execSQL(s);
    }

    boolean validate(Editable userMob, Editable password) {
        Cursor data = db.rawQuery("SELECT COUNT(*) as total FROM '" + user + "' WHERE user_mobile = '"+ userMob +"' and password = '"+ password +"' ", null);
        data.moveToFirst();
//        Log.d("Users: ", "Num Users: " + data.getInt(data.getColumnIndex("total")));
        int isReg = data.getInt(data.getColumnIndex("total"));
        data.close();
        return isReg == 1;
    }

    void trucate(String tab) { //Truncates given table
        db.execSQL("DELETE FROM '"+ tab +"'");
    }

    String getUserName() {
        Cursor data = db.rawQuery("SELECT user_name From '" + user + "' WHERE id = 1", null);
        data.moveToFirst();
//        Log.d("Users: ", "Num Users: " + data.getInt(data.getColumnIndex("total")));
        String ret = data.getString(data.getColumnIndex("user_name"));
        data.close();
        return ret;
    }

    String getAadhaarNumber() {
        Cursor data = db.rawQuery("SELECT aadhaar_no From '" + user + "' WHERE id = 1", null);
        data.moveToFirst();
//        Log.d("Users: ", "Num Users: " + data.getInt(data.getColumnIndex("total")));
        String ret = data.getString(data.getColumnIndex("aadhaar_no"));
        data.close();
        return ret;
    }

    String getMobileNumber() {
        Cursor data = db.rawQuery("SELECT user_mobile From '" + user + "' WHERE id = 1", null);
        data.moveToFirst();
//        Log.d("Users: ", "Num Users: " + data.getInt(data.getColumnIndex("total")));
        String ret = data.getString(data.getColumnIndex("user_mobile"));
        data.close();
        return ret;
    }

    String getEmailId() {
        Cursor data = db.rawQuery("SELECT user_email From '" + user + "' WHERE id = 1", null);
        data.moveToFirst();
//        Log.d("Users: ", "Num Users: " + data.getInt(data.getColumnIndex("total")));
        String ret = data.getString(data.getColumnIndex("user_email"));
        data.close();
        return ret;
    }
}