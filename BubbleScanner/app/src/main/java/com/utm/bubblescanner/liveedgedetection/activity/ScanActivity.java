package com.utm.bubblescanner.liveedgedetection.activity;

import android.Manifest;
import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.PointF;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.transition.TransitionManager;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.FrameLayout;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.utm.bubblescanner.R;
import com.utm.bubblescanner.api.BubbleNetworkManager;
import com.utm.bubblescanner.liveedgedetection.enums.ScanHint;
import com.utm.bubblescanner.liveedgedetection.interfaces.IScanner;
import com.utm.bubblescanner.liveedgedetection.util.ScanUtils;
import com.utm.bubblescanner.liveedgedetection.view.PolygonPoints;
import com.utm.bubblescanner.liveedgedetection.view.PolygonView;
import com.utm.bubblescanner.liveedgedetection.view.Quadrilateral;
import com.utm.bubblescanner.liveedgedetection.view.ScanSurfaceView;

import org.opencv.android.Utils;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.Point;
import org.opencv.imgproc.Imgproc;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

import static android.view.View.GONE;

/**
 * This class initiates camera and detects edges on live view
 */
public class ScanActivity extends AppCompatActivity implements IScanner, View.OnClickListener {
    private static final String TAG = ScanActivity.class.getSimpleName();

    private static final int MY_PERMISSIONS_REQUEST_CAMERA = 101;
    private static final String OPEN_CV_LIBRARY = "opencv_java3";

    private ViewGroup mContainerScan;
    private FrameLayout mCameraPreview;
    private ScanSurfaceView mImageSurfaceView;
    private boolean mPermissionNotGranted;
    private TextView mCaptureHintText;
    private LinearLayout mCaptureHintLayout;
    private FrameLayout mCropLayout;
    private PolygonView mPolygonView;
    private ImageView mCropImageView;
    private View mCropAccept;
    private View mCropReject;
    private ImageButton mManualCapture;

    public final static Stack<PolygonPoints> sDraggedPoints = new Stack<>();
    private Bitmap mCopyBitmap;
    private float scaledWidthFactor;
    private float scaledHeightFactor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        init();
    }

    private void init() {
        mContainerScan = findViewById(R.id.container_scan);
        mCameraPreview = findViewById(R.id.camera_preview);
        mCaptureHintLayout = findViewById(R.id.capture_hint_layout);
        mCaptureHintText = findViewById(R.id.capture_hint_text);
        mPolygonView = findViewById(R.id.polygon_view);
        mCropImageView = findViewById(R.id.crop_image_view);
        mCropAccept = findViewById(R.id.crop_accept_btn);
        mCropReject = findViewById(R.id.crop_reject_btn);
        mCropLayout = findViewById(R.id.crop_layout);
        mManualCapture = findViewById(R.id.manual_capture);

        mCropAccept.setOnClickListener(this);
        mCropReject.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                TransitionManager.beginDelayedTransition(mContainerScan);
                mCropLayout.setVisibility(View.GONE);
                showAcceptancePrompt(false);
                mImageSurfaceView.startPreview();
                mManualCapture.setVisibility(View.VISIBLE);
            }
        });
        checkCameraPermissions();

        mManualCapture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mImageSurfaceView.takePicture();
                mManualCapture.setVisibility(View.INVISIBLE);
            }
        });
    }

    private void showAcceptancePrompt(boolean visible) {
        mCropAccept.setVisibility(visible ? View.VISIBLE : View.INVISIBLE);
        mCropReject.setVisibility(visible ? View.VISIBLE : View.INVISIBLE);
    }

    private void checkCameraPermissions() {
        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            mPermissionNotGranted = true;
            if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                    Manifest.permission.CAMERA)) {
                Toast.makeText(this, "Enable camera permission from settings", Toast.LENGTH_SHORT).show();
            } else {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.CAMERA},
                        MY_PERMISSIONS_REQUEST_CAMERA);
            }
        } else {
            if (!mPermissionNotGranted) {
                mImageSurfaceView = new ScanSurfaceView(this, this);
                mCameraPreview.addView(mImageSurfaceView);
            } else {
                mPermissionNotGranted = false;
            }
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           @NonNull String permissions[],
                                           @NonNull int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSIONS_REQUEST_CAMERA:
                onRequestCamera(grantResults);
                break;
            default:
                break;
        }
    }

    private void onRequestCamera(int[] grantResults) {
        if (grantResults.length > 0
                && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            mImageSurfaceView = new ScanSurfaceView(ScanActivity.this, ScanActivity.this);
                            mCameraPreview.addView(mImageSurfaceView);
                        }
                    });
                }
            }, 500);

        } else {
            Toast.makeText(this, getString(R.string.camera_activity_permission_denied_toast), Toast.LENGTH_SHORT).show();
            this.finish();
        }
    }

    @Override
    public void displayHint(ScanHint scanHint) {
        mCaptureHintLayout.setVisibility(View.VISIBLE);
        switch (scanHint) {
            case MOVE_CLOSER:
                mCaptureHintText.setText(getResources().getString(R.string.move_closer_hint));
                mCaptureHintLayout.setBackground(getResources().getDrawable(R.drawable.hint_red));
                break;
            case MOVE_AWAY:
                mCaptureHintText.setText(getResources().getString(R.string.move_away_hint));
                mCaptureHintLayout.setBackground(getResources().getDrawable(R.drawable.hint_red));
                break;
            case ADJUST_ANGLE:
                mCaptureHintText.setText(getResources().getString(R.string.adjust_angle_hint));
                mCaptureHintLayout.setBackground(getResources().getDrawable(R.drawable.hint_red));
                break;
            case FIND_RECT:
                mCaptureHintText.setText(getResources().getString(R.string.darker_background_hint));
                mCaptureHintLayout.setBackground(getResources().getDrawable(R.drawable.hint_white));
                break;
            case CAPTURING_IMAGE:
                mCaptureHintText.setText(getResources().getString(R.string.hold_still_hint));
                mCaptureHintLayout.setBackground(getResources().getDrawable(R.drawable.hint_green));
                break;
            case NO_MESSAGE:
                mCaptureHintLayout.setVisibility(GONE);
                break;
            default:
                break;
        }
    }

    @Override
    public void onPictureClicked(final Bitmap bitmap) {
        try {
            mCopyBitmap = bitmap.copy(Bitmap.Config.ARGB_8888, true);

            int height = getWindow().findViewById(Window.ID_ANDROID_CONTENT).getHeight();
            int width = getWindow().findViewById(Window.ID_ANDROID_CONTENT).getWidth();

            int scaledWidth = mCopyBitmap.getWidth();
            int scaledHeight = mCopyBitmap.getHeight();

            scaledWidthFactor = ((float) width) / scaledWidth;
            scaledHeightFactor = ((float) height) / scaledHeight;

            Mat originalMat = new Mat(mCopyBitmap.getHeight(), mCopyBitmap.getWidth(), CvType.CV_8UC1);
            Utils.bitmapToMat(mCopyBitmap, originalMat);
            ArrayList<PointF> points;
            Map<Integer, PointF> pointFs = new HashMap<>();
            try {
                Quadrilateral quad = ScanUtils.detectLargestQuadrilateral(originalMat);
                if (null != quad) {
                    double resultArea = Math.abs(Imgproc.contourArea(quad.contour));
                    double previewArea = originalMat.rows() * originalMat.cols();
                    if (resultArea > previewArea * 0.08) {
                        points = new ArrayList<>();
                        points.add(new PointF((float) quad.points[0].x, (float) quad.points[0].y));
                        points.add(new PointF((float) quad.points[1].x, (float) quad.points[1].y));
                        points.add(new PointF((float) quad.points[3].x, (float) quad.points[3].y));
                        points.add(new PointF((float) quad.points[2].x, (float) quad.points[2].y));
                    } else {
                        points = ScanUtils.getPolygonDefaultPoints(mCopyBitmap);
                    }

                } else {
                    points = ScanUtils.getPolygonDefaultPoints(mCopyBitmap);
                }

                int index = -1;
                for (PointF pointF : points) {
                    pointF.x = pointF.x * scaledWidthFactor;
                    pointF.y = pointF.y * scaledHeightFactor;
                    pointFs.put(++index, pointF);
                }

                mPolygonView.setPoints(pointFs);
                int padding = (int) getResources().getDimension(R.dimen.scan_padding);
                FrameLayout.LayoutParams layoutParams = new FrameLayout.LayoutParams((int) (mCopyBitmap.getWidth() * scaledWidthFactor) + 2 * padding,
                        (int) (mCopyBitmap.getHeight() * scaledHeightFactor) + 2 * padding);
                layoutParams.gravity = Gravity.CENTER;
                mPolygonView.setLayoutParams(layoutParams);
                TransitionManager.beginDelayedTransition(mContainerScan);
                mCropLayout.setVisibility(View.VISIBLE);
                showAcceptancePrompt(true);

                mCropImageView.setImageBitmap(mCopyBitmap);
                mCropImageView.setScaleType(ImageView.ScaleType.FIT_XY);
            } catch (Exception e) {
                Log.e(TAG, e.getMessage(), e);
            }
        } catch (Exception e) {
            Log.e(TAG, e.getMessage(), e);
        }
    }

    static {
        System.loadLibrary(OPEN_CV_LIBRARY);
    }

    @Override
    public void onClick(View view) {
        Map<Integer, PointF> points = mPolygonView.getPoints();

        final Bitmap croppedBitmap;

        if (ScanUtils.isScanPointsValid(points)) {
            Point point1 = new Point(points.get(0).x / scaledWidthFactor, points.get(0).y / scaledHeightFactor);
            Point point2 = new Point(points.get(1).x / scaledWidthFactor, points.get(1).y / scaledHeightFactor);
            Point point3 = new Point(points.get(2).x / scaledWidthFactor, points.get(2).y / scaledHeightFactor);
            Point point4 = new Point(points.get(3).x / scaledWidthFactor, points.get(3).y / scaledHeightFactor);
            croppedBitmap = ScanUtils.enhanceReceipt(mCopyBitmap, point1, point2, point3, point4);
        } else {
            croppedBitmap = mCopyBitmap;
        }


        AsyncTask.execute(new Runnable() {
            @Override
            public void run() {
            BubbleNetworkManager.getInstance().uploadImages(croppedBitmap, new BubbleNetworkManager.SuccessCallback() {
                @Override
                public void onSuccess() {
                    Toast.makeText(ScanActivity.this, R.string.image_upload_success, Toast.LENGTH_SHORT)
                            .show();
                }

                @Override
                public void onFailure(String error) {
                    Toast.makeText(ScanActivity.this, R.string.image_upload_error, Toast.LENGTH_SHORT)
                            .show();
                }
            });
            }
        });

        setResult(Activity.RESULT_OK);
        System.gc();
        finish();
    }
}
