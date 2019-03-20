/*
 *  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree.
 */

'use strict';

const snapshotButton = document.querySelector('button#snapshot');
const filterSelect = document.querySelector('select#filter');

let stats;

// Put variables in global scope to make them available to the browser console.
const video = window.video = document.querySelector('video');
const canvas = window.canvas = document.querySelector('#canvasInput');
const canvasout = document.querySelector('#canvasOutput');
canvas.width = 600;
canvas.height = 800;

snapshotButton.onclick = function () {
  let context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  let imgData = context.getImageData(0, 0, canvas.width, canvas.height);
  context.putImageData(imgData, 0, 0);

  let src = cv.imread('canvasInput');
  let dst = new cv.Mat();
  let ksize = new cv.Size(3, 3);
  let anchor = new cv.Point(-1, -1);
  // You can try more different parameters
  cv.blur(src, dst, ksize, anchor, cv.BORDER_DEFAULT);
  // cv.boxFilter(src, dst, -1, ksize, anchor, true, cv.BORDER_DEFAULT)
  cv.imshow('canvasOutput2', dst);
  src.delete();
  dst.delete();


  let src6 = cv.imread('canvasOutput2');
  let dst6 = new cv.Mat();
  cv.cvtColor(src6, src6, cv.COLOR_RGB2GRAY, 0);
  // You can try more different parameters
  cv.Canny(src6, dst6, 50, 100, 3, false);
  cv.imshow('canvasOutput5', dst6);
  src6.delete();
  dst6.delete();

  let src4 = cv.imread('canvasOutput5');
  let dst4 = new cv.Mat();
  let gray = new cv.Mat();
  let opening = new cv.Mat();
  let coinsBg = new cv.Mat();
  let coinsFg = new cv.Mat();
  let distTrans = new cv.Mat();
  let unknown = new cv.Mat();
  let markers = new cv.Mat();
  stats = new cv.Mat();
  let centroids = new cv.Mat();
  // gray and threshold image
  cv.cvtColor(src4, gray, cv.COLOR_RGBA2GRAY, 0);
  cv.threshold(gray, gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU);
  // get background
  let M4 = cv.Mat.ones(1, 1, cv.CV_8U);
  cv.erode(gray, gray, M4);
  cv.dilate(gray, opening, M4);
  cv.dilate(opening, coinsBg, M4, new cv.Point(-1, -1), 3);
  // distance transform
  cv.distanceTransform(opening, distTrans, cv.DIST_L2, 5);
  cv.normalize(distTrans, distTrans, 1, 0, cv.NORM_INF);
  // get foreground
  cv.threshold(distTrans, coinsFg, 0.7 * 1, 255, cv.THRESH_BINARY);
  coinsFg.convertTo(coinsFg, cv.CV_8U, 1, 0);
  cv.subtract(coinsBg, coinsFg, unknown);
  // get connected components markers
  // cv.connectedComponents(coinsFg, markers);
  cv.connectedComponentsWithStats(coinsFg, markers, stats, centroids, 8, cv.CV_32S);
  for (let i = 0; i < markers.rows; i++) {
    for (let j = 0; j < markers.cols; j++) {
      //if(i == 0 && j == 0)
      //alert(markers.rows + "   " + markers.cols + "   " + cv.stats());
      markers.intPtr(i, j)[0] = markers.ucharPtr(i, j)[0] + 1;
      if (unknown.ucharPtr(i, j)[0] == 255) {
        markers.intPtr(i, j)[0] = 0;
      }
    }
  }
  cv.cvtColor(src4, src4, cv.COLOR_RGBA2RGB, 0);
  cv.watershed(src4, markers);

  let prevx = 0;
  for (let i = 0; i < markers.rows; i++) {
    for (let j = 0; j < markers.cols; j++) {
      if (markers.intPtr(i, j)[0] == -1) {
        if (i !== 0 && j !== 0 && i !== canvas.height - 1 && j !== canvas.width - 1) {
          prevx = i;
          src4.ucharPtr(i, j)[0] = 255; // R
          src4.ucharPtr(i, j)[1] = 255; // G
          src4.ucharPtr(i, j)[2] = 255; // B
        }
      } else {
        src4.ucharPtr(i, j)[0] = 0; // R
        src4.ucharPtr(i, j)[1] = 0; // G
        src4.ucharPtr(i, j)[2] = 0; // B
      }
    }
  }
  cv.imshow('canvasOutput', src4);
  src4.delete();
  dst4.delete();
  gray.delete();
  opening.delete();
  coinsBg.delete();
  coinsFg.delete();
  distTrans.delete();
  unknown.delete();
  markers.delete();
  M4.delete();


  /*
  let src7 = cv.imread('canvasOutput6');
  let dst7 = cv.Mat.zeros(src7.rows, src7.cols, cv.CV_8UC3);
  cv.cvtColor(src7, src7, cv.COLOR_RGBA2GRAY, 0);
  cv.threshold(src7, src7, 100, 200, cv.THRESH_BINARY);
  let contours = new cv.MatVector();
  let hierarchy = new cv.Mat();
  let poly = new cv.MatVector();
  cv.findContours(src7, contours, hierarchy, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE);
  // approximates each contour to polygon
  for (let i = 0; i < contours.size(); ++i) {
    let tmp = new cv.Mat();
    let cnt = contours.get(i);
    // You can try more different parameters
    cv.approxPolyDP(cnt, tmp, 3, true);
    poly.push_back(tmp);
    cnt.delete();
    tmp.delete();
  }
  // draw contours with random Scalar
  for (let i = 0; i < contours.size(); ++i) {
    let color = new cv.Scalar(Math.round(Math.random() * 255), Math.round(Math.random() * 255),
      Math.round(Math.random() * 255));
    cv.drawContours(dst7, poly, i, color, 1, 8, hierarchy, 0);
  }
  cv.imshow('canvasOutput', dst7);
  src7.delete();
  dst7.delete();
  hierarchy.delete();
  contours.delete();
  poly.delete();*/

  $.ajax({
    type: "POST",
    url: "/uploadImage",
    data: {
      imgBase64: document.querySelector('#canvasInput').toDataURL('image/png'),
      name: "in.png"
    }
  }).done(function (o) {
    alert(o);
    // If you want the file to be visible in the browser 
    // - please modify the callback in javascript. All you
    // need is to return the url to the file, you just saved 
    // and than put the image in your browser.
  });

  $.ajax({
    type: "POST",
    url: "/uploadImage",
    data: {
      imgBase64: document.querySelector('#canvasOutput').toDataURL('image/png'),
      name: "out.png"
    }
  }).done(function (o) {
    alert(o);
    // If you want the file to be visible in the browser 
    // - please modify the callback in javascript. All you
    // need is to return the url to the file, you just saved 
    // and than put the image in your browser.
  });
};

const constraints = {
  audio: false,
  video: { facingMode: { exact: "environment" } }
  //video: true
};

function handleSuccess(stream) {
  window.stream = stream; // make stream available to browser console
  video.srcObject = stream;
}

function handleError(error) {
  console.log('navigator.getUserMedia error: ', error);
}

navigator.mediaDevices.getUserMedia(constraints).then(handleSuccess).catch(handleError);
