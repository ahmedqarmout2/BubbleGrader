package com.utm.bubblescanner.api;

import android.support.annotation.NonNull;
import android.util.Log;

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

    public static void uploadImages(@NonNull String uriString) {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://142.1.4.224:3000")
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
            }

            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                Log.e("Upload error:", t.getMessage());
            }
        });
    }
}
