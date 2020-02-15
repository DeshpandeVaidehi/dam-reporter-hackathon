package dam.sih.damreporter;

import android.os.AsyncTask;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.widget.SwipeRefreshLayout;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.util.ArrayList;

/**
 * Created by tushar on 18/03/18.
 */

public class FragmentNotify extends Fragment implements SwipeRefreshLayout.OnRefreshListener {
    View view;
    SwipeRefreshLayout swipeLayout;
    ListView listView;
    ArrayAdapter adapter;
    ArrayList< String> arrayList;
    String [] array = new String[]{"Red","Black","White","Purple"};
    public FragmentNotify() {
    }

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.notification_center, container, false);
        swipeLayout = (SwipeRefreshLayout) view.findViewById(R.id.swipeToRefresh);
        swipeLayout.setOnRefreshListener(this);
        // swipeLayout.setColorSchemeColors();
        listView = (ListView) view.findViewById(R.id.mlistView);
        adapter = new ArrayAdapter(getActivity(),android.R.layout.simple_list_item_1, appendData());
        listView.setAdapter(adapter);
        return view;
    }


    @Override
    public void onRefresh() {
        new Handler().postDelayed(new Runnable() {
            @Override public void run() {
                addMore();
                swipeLayout.setRefreshing(false);
            }
        }, 2000);

    }

    private ArrayList appendData(){
        if(arrayList==null)
            arrayList =  new ArrayList();

        for (String items : array) {
            arrayList.add(items);
        }
        return arrayList;
    }

    private void addMore() {
        if(arrayList==null)
            arrayList =  new ArrayList();

        for (String items : array) {
            arrayList.add(items);
        }
        adapter.notifyDataSetChanged();
    }
}