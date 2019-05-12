package com.utm.bubblescanner.api;

import android.support.annotation.NonNull;
import android.text.TextUtils;
import android.util.Log;
import android.util.Patterns;

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

    public void uploadImages(@NonNull String uriString, final SuccessCallback callback) {
        if (!Patterns.WEB_URL.matcher(mBaseUrl).matches()) callback.onFailure("Invalid url");

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(mBaseUrl)
                .build();

        BubbleService service = retrofit.create(BubbleService.class);
        File file = new File(uriString);

        // create RequestBody instance from file
        RequestBody requestFile = RequestBody.create(MediaType.parse("image/*"), file);

        // MultipartBody.Part is used to send also the actual file name
        MultipartBody.Part body =
                MultipartBody.Part.createFormData("photo", file.getName(), requestFile);

        Call<ResponseBody> call = service.uploadPhotos(body);
        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call,
                                   Response<ResponseBody> response) {
                Log.v("Upload", "success");
                callback.onSuccess();
            }

            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                Log.e("Upload error:", t.getMessage());
                callback.onFailure(t.getMessage());
            }
        });
    }

    public interface SuccessCallback {
        void onSuccess();
        void onFailure(String error);
    }
}
