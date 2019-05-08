package com.utm.bubblescanner;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.support.design.button.MaterialButton;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextUtils;
import android.text.TextWatcher;
import android.util.AttributeSet;
import android.util.Patterns;
import android.view.View;
import android.widget.EditText;

import com.utm.bubblescanner.api.BubbleNetworkManager;

import butterknife.BindView;
import butterknife.ButterKnife;

public class SetupActivity extends AppCompatActivity {

    @BindView(R.id.server_address_input)
    EditText mServerAddressInput;
    @BindView(R.id.enter_button)
    MaterialButton mEnterButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup);
        ButterKnife.bind(this);

        mEnterButton.setEnabled(false);
        mServerAddressInput.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {}

            @Override
            public void afterTextChanged(Editable s) {
                String url = s.toString();
                mEnterButton.setEnabled(Patterns.WEB_URL.matcher(url).matches());
            }
        });

        mEnterButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                BubbleNetworkManager.getInstance()
                        .setBaseUrl(mServerAddressInput.getText().toString());
                startActivity(new Intent(SetupActivity.this, MainActivity.class));
                finish();
            }
        });
    }
}
