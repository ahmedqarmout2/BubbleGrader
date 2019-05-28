package com.utm.bubblescanner;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.button.MaterialButton;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextUtils;
import android.text.TextWatcher;
import android.util.Patterns;
import android.view.View;
import android.widget.EditText;

import com.utm.bubblescanner.api.BubbleNetworkManager;

import butterknife.BindView;
import butterknife.ButterKnife;

public class SetupActivity extends AppCompatActivity implements TextWatcher {

    @BindView(R.id.server_address_input)
    EditText mServerAddressInput;
    @BindView(R.id.port_number_input)
    EditText mPortNumberInput;
    @BindView(R.id.enter_button)
    MaterialButton mEnterButton;

    private String mServerAddress;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup);
        ButterKnife.bind(this);

        mEnterButton.setEnabled(false);
        mServerAddressInput.addTextChangedListener(this);
        mPortNumberInput.addTextChangedListener(this);

        mEnterButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                BubbleNetworkManager.getInstance()
                        .setBaseUrl(mServerAddress);
                startActivity(new Intent(SetupActivity.this, MainActivity.class));
                finish();
            }
        });
    }

    private void validateUrl() {
        String serverAddress = mServerAddressInput.getText().toString();
        String portNo = mPortNumberInput.getText().toString();
        if (!TextUtils.isEmpty(portNo)) {
            serverAddress = serverAddress + ":" + portNo;
        }

        if (Patterns.WEB_URL.matcher(serverAddress).matches()) {
            mEnterButton.setEnabled(true);
            mServerAddress = serverAddress;
        }
    }

    @Override
    public void beforeTextChanged(CharSequence s, int start, int count, int after) {

    }

    @Override
    public void onTextChanged(CharSequence s, int start, int before, int count) {

    }

    @Override
    public void afterTextChanged(Editable s) {
        validateUrl();
    }
}
