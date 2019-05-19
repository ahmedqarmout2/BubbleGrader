package com.utm.bubblescanner;

import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;

import com.utm.bubblescanner.api.BubbleNetworkManager;
import com.utm.bubblescanner.util.Constants;

import butterknife.BindView;
import butterknife.ButterKnife;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    @BindView(R.id.fab) FloatingActionButton mScanFab;
    @BindView(R.id.scanned_image) TouchImageView mScannedImage;
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
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        if (requestCode == Constants.SCAN_REQUEST_CODE && data != null) {
            if (data.getExtras() == null) return;

            String filePath = data.getExtras().getString(ScanConstants.SCANNED_RESULT);
            final Bitmap bitmap = ScanUtils.decodeBitmapFromFile(filePath, ScanConstants.IMAGE_NAME);
            String fileName = filePath+"/"+ScanConstants.IMAGE_NAME;
            BubbleNetworkManager.getInstance().uploadImages(fileName, new BubbleNetworkManager.SuccessCallback() {
                @Override
                public void onSuccess() {
                    showScannedImage(bitmap);
                }

                @Override
                public void onFailure(String error) {}
            });
        }
    }

    private void showScannedImage(Bitmap bitmap) {
        mScannedImage.setVisibility(View.VISIBLE);
        mScannedImage.setImageBitmap(bitmap);
    }
}
