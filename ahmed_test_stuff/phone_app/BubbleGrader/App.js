import React from 'react';
import { Text, View, TouchableOpacity, Button, KeyboardAvoidingView, Image } from 'react-native';
import { Camera, Permissions } from 'expo';
import FileUploader from 'react-native-file-uploader'

export default class CameraExample extends React.Component {
  state = {
    hasCameraPermission: null,
    type: Camera.Constants.Type.back,
    scanning: true,
    imgURI: ""
  };

  async componentDidMount() {
    const { status } = await Permissions.askAsync(Permissions.CAMERA);
    this.setState({ hasCameraPermission: status === 'granted' });
  }

  render() {
    const { hasCameraPermission } = this.state;
    if (hasCameraPermission === null) {
      return <View />;
    } else if (hasCameraPermission === false) {
      return <Text>No access to camera</Text>;
    } else if (this.state.scanning === true) {
      return (
        <View style={{ flex: 1 }}>
          <Camera style={{ flex: 1 }} type={this.state.type}
          barCodeScannerSettings={{
            barCodeTypes: ["QRCode"]
          }}
          ref={ref => { this.camera = ref; }} 
          onBarCodeScanned={ async () => {
            if (this.camera) {
              const pictureSizes = await this.camera.getAvailablePictureSizesAsync('4:3');

              // alert(pictureSizes);
              // {pictureSize: pictureSizes[0], base64: true}
              let photo = await this.camera.takePictureAsync();
              alert(JSON.stringify(photo));
              this.setState({ scanning: false, imgURI: photo.uri });

              const data = new FormData();

              data.append("photo", {
                name: 'lol.jpg',
                type: 'image/jpeg',
                uri: photo.uri
              });

              fetch("http://142.1.4.130:3000/api/upload", {
                method: "POST",
                body: data
              });


              return;

              const obj = {
                uploadUrl: 'http://142.1.3.177:9081/ping',
                method: 'POST', // default 'POST',support 'POST' and 'PUT'
                headers: {
                  'Accept': 'application/json',
                },
                fields: {
                    'hello': 'world',
                },
                files: [
                  {
                    name: 'one', // optional, if none then `filename` is used instead
                    filename: 'one.w4a', // require, file name
                    filepath: photo.uri, // require, file absoluete path
                    filetype: 'image/jpeg', // options, if none, will get mimetype from `filepath` extension
                  },
                ]
              };

              FileUpload.upload(obj, function(err, result) {
                console.log('upload:', err, result);
              })

              return;

              let formData = new FormData();
              formData.append('photouri', {uri: photo.uri, name: 'image.jpg', type: 'image/jpeg'});
              
              fetch('http://142.1.3.177:9081/ping', {
                method: 'POST',
                headers: {
                  Accept: 'application/json',
                  'Content-Type': 'multipart/form-data',
                },
                body: formData
              }).then(response => {
                console.log("image uploaded");
              }).catch(err => {
                console.error(err);
              });
              
              return;

              let photoObj = {
                uri: photo.uri,
                type: 'image/jpeg',
                name: 'photo.jpg',
              };
              
              var body = new FormData();
              body.append('imgBase64', photoObj);
              body.append('name', 'A beautiful photo!');
              
              var xhr = new XMLHttpRequest();
              xhr.open('POST', 'http://142.1.3.177:9081/uploadImage');
              xhr.send(body);
            }
          }}>
            <View
              style={{
                flex: 1,
                backgroundColor: 'transparent',
                flexDirection: 'row',
              }}>
              <TouchableOpacity
                style={{
                  flex: 0.1,
                  alignSelf: 'flex-end',
                  alignItems: 'center',
                }}
                onPress={() => {
                  this.setState({
                    scanning: false
                  });
                }}>
                <Text
                  style={{ fontSize: 18, marginBottom: 10, color: 'white' }}>
                  {' '}Flip{' '}
                </Text>
              </TouchableOpacity>
            </View>
          </Camera>
        </View>
      );
    }else{
      return <View style={{
        flex: 1,
        alignItems: 'stretch'
      }}>
        <Image
          source={{
            uri: this.state.imgURI
          }}
          style={{
            flex: 1
          }}
        />
        <Button
          onPress={() => {this.setState({ scanning: true });}}
          title="Learn More"
          color="#841584"
        />
      </View>
    }
  }
}