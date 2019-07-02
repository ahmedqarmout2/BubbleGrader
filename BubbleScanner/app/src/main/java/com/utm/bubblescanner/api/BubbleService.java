package com.utm.bubblescanner.api;

import okhttp3.MultipartBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface BubbleService {

    @Multipart
    @POST("api/upload/photo")
    Call<ResponseBody> uploadPhotos(@Part MultipartBody.Part file);
}
