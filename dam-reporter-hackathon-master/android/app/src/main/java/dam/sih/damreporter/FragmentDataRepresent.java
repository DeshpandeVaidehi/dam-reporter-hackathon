package dam.sih.damreporter;

import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

/**
 * Created by tushar on 18/03/18.
 */

public class FragmentDataRepresent extends Fragment{
    View view;
    public FragmentDataRepresent() {
    }

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.data_representation, container, false);
        return view;
    }
}