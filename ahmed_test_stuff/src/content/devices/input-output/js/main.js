/*
 *  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree.
 */

'use strict';

const videoElement = document.querySelector('video');
const audioInputSelect = document.querySelector('select#audioSource');
const audioOutputSelect = document.querySelector('select#audioOutput');
const videoSelect = document.querySelector('select#videoSource');
const selectors = [audioInputSelect, audioOutputSelect, videoSelect];

audioOutputSelect.disabled = !('sinkId' in HTMLMediaElement.prototype);

function gotDevices(deviceInfos) {
  // Handles being called several times to update labels. Preserve values.
  const values = selectors.map(select => select.value);
  selectors.forEach(select => {
    while (select.firstChild) {
      select.removeChild(select.firstChild);
    }
  });
  for (let i = 0; i !== deviceInfos.length; ++i) {
    const deviceInfo = deviceInfos[i];
    const option = document.createElement('option');
    option.value = deviceInfo.deviceId;
    if (deviceInfo.kind === 'audioinput') {
      option.text = deviceInfo.label || `microphone ${audioInputSelect.length + 1}`;
      audioInputSelect.appendChild(option);
    } else if (deviceInfo.kind === 'audiooutput') {
      option.text = deviceInfo.label || `speaker ${audioOutputSelect.length + 1}`;
      audioOutputSelect.appendChild(option);
    } else if (deviceInfo.kind === 'videoinput') {
      option.text = deviceInfo.label || `camera ${videoSelect.length + 1}`;
      videoSelect.appendChild(option);
    } else {
      console.log('Some other kind of source/device: ', deviceInfo);
    }
  }
  selectors.forEach((select, selectorIndex) => {
    if (Array.prototype.slice.call(select.childNodes).some(n => n.value === values[selectorIndex])) {
      select.value = values[selectorIndex];
    }
  });
}

navigator.mediaDevices.enumerateDevices().then(gotDevices).catch(handleError);

// Attach audio output device to video element using device/sink ID.
function attachSinkId(element, sinkId) {
  if (typeof element.sinkId !== 'undefined') {
    element.setSinkId(sinkId)
      .then(() => {
        console.log(`Success, audio output device attached: ${sinkId}`);
      })
      .catch(error => {
        let errorMessage = error;
        if (error.name === 'SecurityError') {
          errorMessage = `You need to use HTTPS for selecting audio output device: ${error}`;
        }
        console.error(errorMessage);
        // Jump back to first output device in the list as it's the default.
        audioOutputSelect.selectedIndex = 0;
      });
  } else {
    console.warn('Browser does not support output device selection.');
  }
}

function changeAudioDestination() {
  const audioDestination = audioOutputSelect.value;
  attachSinkId(videoElement, audioDestination);
}

function gotStream(stream) {
  window.stream = stream; // make stream available to console
  videoElement.srcObject = stream;
  // Refresh button list in case labels have become available
  return navigator.mediaDevices.enumerateDevices();
}

function handleError(error) {
  console.log('navigator.getUserMedia error: ', error);
}

function start() {
  if (window.stream) {
    window.stream.getTracks().forEach(track => {
      track.stop();
    });
  }
  const audioSource = audioInputSelect.value;
  const videoSource = videoSelect.value;
  const constraints = {
    video: {
      deviceId: videoSource ? {
        exact: videoSource
      } : undefined
    }
  };
  navigator.mediaDevices.getUserMedia(constraints).then(gotStream).then(gotDevices).catch(handleError);
}

audioInputSelect.onchange = start;
audioOutputSelect.onchange = changeAudioDestination;

videoSelect.onchange = start;

start();

const snapshotButton = document.querySelector('button#snapshot');
const filterSelect = document.querySelector('select#filter');

const video = window.video = document.querySelector('video');
const canvas = window.canvas = document.querySelector('canvas');


snapshotButton.onclick = function () {
  //video.width;
  canvas.width = 600;
  canvas.height = 800;

  canvas.className = filterSelect.value;
  var context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  var imgData = context.getImageData(0, 0, canvas.width, canvas.height);
  var data = imgData.data;

  // enumerate all pixels
  // each pixel's r,g,b,a datum are stored in separate sequential array elements

  // for (var i = 0; i < data.length; i += 4) {
  //   data[i] = 0;
  //   data[i + 1] = 0;
  //   var blue = data[i + 2];
  //   var alpha = data[i + 3];
  // }

  context.putImageData(imgData, 0, 0);

  let src = cv.imread('canv');
  let dst = new cv.Mat();
  let gray = new cv.Mat();
  let opening = new cv.Mat();
  let coinsBg = new cv.Mat();
  cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY, 0);
  cv.threshold(gray, gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU);

  // get background
  let M = cv.Mat.ones(1, 1, cv.CV_8U);
  cv.erode(gray, gray, M);
  cv.dilate(gray, opening, M);
  cv.dilate(opening, coinsBg, M, new cv.Point(-1, -1), 3);

  cv.imshow('canv', coinsBg);
  src.delete();
  dst.delete();
  gray.delete();
  opening.delete();
  coinsBg.delete();
  M.delete();




  let src = cv.imread('canvasInput');
let dst = cv.Mat.zeros(src.rows, src.cols, cv.CV_8UC3);
cv.cvtColor(src, src, cv.COLOR_RGB2GRAY, 0);
cv.Canny(src, src, 50, 100, 3, false);


let contours = new cv.MatVector();
let hierarchy = new cv.Mat();
cv.findContours(src, contours, hierarchy, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE);
let cnt = contours.get(0);
// You can try more different parameters
let rect = cv.boundingRect(cnt);
let contoursColor = new cv.Scalar(255, 255, 255);
let rectangleColor = new cv.Scalar(255, 0, 0);
cv.drawContours(dst, contours, 0, contoursColor, 1, 8, hierarchy, 100);
let point1 = new cv.Point(rect.x, rect.y);
let point2 = new cv.Point(rect.x + rect.width, rect.y + rect.height);
cv.rectangle(dst, point1, point2, rectangleColor, 2, cv.LINE_AA, 0);
cv.imshow('canvasOutput', dst);
src.delete(); dst.delete(); contours.delete(); hierarchy.delete(); cnt.delete();


};

filterSelect.onchange = function () {
  video.className = filterSelect.value;
};