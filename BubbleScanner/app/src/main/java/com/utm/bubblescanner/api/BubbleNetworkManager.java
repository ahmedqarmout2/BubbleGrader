package com.utm.bubblescanner.api;

import android.graphics.Bitmap;
import android.support.annotation.NonNull;
import android.util.Log;
import android.util.Patterns;

import com.utm.bubblescanner.liveedgedetection.constants.ScanConstants;

import java.io.ByteArrayOutputStream;
import java.io.File;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;

public class BubbleNetworkManager {

    private volatile static BubbleNetworkManager mInstance;
    private String mBaseUrl;

    public static BubbleNetworkManager getInstance() {
        if (mInstance == null) {
            synchronized (BubbleNetworkManager.class) {
                if (mInstance == null) mInstance = new BubbleNetworkManager();
            }
        }
        return mInstance;
    }

    public void setBaseUrl(String url) {
        mBaseUrl = url;
    }

    public void uploadImages(@NonNull Bitmap bitmap, final SuccessCallback callback) {
        if (!Patterns.WEB_URL.matcher(mBaseUrl).matches()) callback.onFailure("Invalid url");

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(mBaseUrl)
                .build();

        BubbleService service = retrofit.create(BubbleService.class);

        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, bos);
        byte[] bitmapData = bos.toByteArray();

        RequestBody requestFile = RequestBody.create(MediaType.parse("image/png"), bitmapData);
        MultipartBody.Part body =
                MultipartBody.Part.createFormData("photo",
                        ScanConstants.IMAGE_PREFIX + bitmap.hashCode(), requestFile);

        Call<ResponseBody> call = service.uploadPhotos(body);
        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call,
                                   Response<ResponseBody> response) {
                Log.v("Upload", "Success");
                callback.onSuccess();
            }

            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                Log.e("Upload", "Error: " + t.getMessage());
                callback.onFailure(t.getMessage());
            }
        });
    }

    public interface SuccessCallback {
        void onSuccess();
        void onFailure(String error);
    }
}
