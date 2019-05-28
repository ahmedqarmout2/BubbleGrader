package com.utm.bubblescanner;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;

import com.adityaarora.liveedgedetection.activity.ScanActivity;
import com.adityaarora.liveedgedetection.constants.ScanConstants;
import com.adityaarora.liveedgedetection.util.ScanUtils;
import com.utm.bubblescanner.api.BubbleNetworkManager;
import com.utm.bubblescanner.util.Constants;

import butterknife.BindView;
import butterknife.ButterKnife;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    @BindView(R.id.fab) FloatingActionButton mScanFab;
    @BindView(R.id.toolbar) Toolbar mToolbar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);

        setSupportActionBar(mToolbar);
        mScanFab.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.fab:
                startActivityForResult(new Intent(this, ScanActivity.class),
                        Constants.SCAN_REQUEST_CODE);
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable final Intent data) {
        if (requestCode != Constants.SCAN_REQUEST_CODE || data == null) return;

        AsyncTask.execute(new Runnable() {
            @Override
            public void run() {
                String filePath = data.getExtras().getString(ScanConstants.SCANNED_RESULT);
                BubbleNetworkManager.getInstance().uploadImages(filePath, new BubbleNetworkManager.SuccessCallback() {
                    @Override
                    public void onSuccess() {}

                    @Override
                    public void onFailure(String error) {}
                });
            }
        });
    }
}
