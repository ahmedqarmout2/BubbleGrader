package com.utm.bubblescanner.liveedgedetection.interfaces;

import android.graphics.Bitmap;

import com.utm.bubblescanner.liveedgedetection.enums.ScanHint;

/**
 * Interface between activity and surface view
 */

public interface IScanner {
    void displayHint(ScanHint scanHint);
    void onPictureClicked(Bitmap bitmap);
}
