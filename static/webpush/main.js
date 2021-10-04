/*
*
*  Push Notifications codelab
*  Copyright 2015 Google Inc. All rights reserved.
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      https://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License
*
*/

/* eslint-env browser, es6 */

'use strict';

const applicationServerPublicKey = 'BDdlALZ8NCz2i918kmBPUuB868VKCwNRUizf3c5pEiqXqrmjvuiN7QccOMXzSEaSN3_gzmCXl4h7boF3D21aRgk';

const pushButton = document.querySelector('#notify');

let isSubscribed = false;
let swRegistration = null;

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}
// Checking if serviceworker and pushManager is active
if ('serviceWorker' in navigator && 'PushManager' in window) {
  console.log('Service Worker and Push are supported');

  navigator.serviceWorker.register('https://app.musixcloud.com/musixcloudpush')
  .then(function(swReg) {
    console.log('Service Worker is registered', swReg);

    swRegistration = swReg;
    initializeUI();
  })
  .catch(function(error) {
    console.error('Service Worker Error', error);
  });
} else {
  console.warn('Push messaging is not supported');
  // pushButton.textContent = 'Push Not Supported';
}

function initializeUI() {
  pushButton.addEventListener('click', function() {
    // pushButton.disabled = true;
    if (isSubscribed) {
      // TODO: Unsubscribe user
      unsubscribeUser();
    } else {
      subscribeUser();
    }
  });
  // Set the initial subscription value
  swRegistration.pushManager.getSubscription()
  .then(function(subscription) {
    isSubscribed = !(subscription === null);

    if (isSubscribed) {
      console.log('User IS subscribed.');
    } else {
      console.log('User is NOT subscribed.');
      swal({
        title: "Notification",
        text: 'Turn on post notication to enjoy update on latest songs, artist catelogue, unlimited stream and downloads',
        icon: "https://app.musixcloud.com/static/svg/icon.png",
        button: "Subscribe",
        className: "notification-bg"
      })
    .then((value) => {
     if(`${value}`=='true'){
      $("#notify").trigger("click");
     }
      });
    }

    updateBtn();
  });
}

function updateBtn() {
  if (Notification.permission === 'denied') {
    console.log('Push Messaging Blocked')
    // pushButton.textContent = 'Push Messaging Blocked';
    // pushButton.disabled = true;
    updateSubscriptionOnServer(null);
    return;
  }
  if (isSubscribed) {
    pushButton.classList.add('subcribed');
  } else {
    pushButton.classList.remove('subcribed');
  }

  // pushButton.disabled = false;
}



function subscribeUser() {
  const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
  swRegistration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: applicationServerKey
  })
  .then(function(subscription) {
    console.log('User is subscribed.');

    updateSubscriptionOnServer(subscription);

    isSubscribed = true;

    updateBtn();
  })
  .catch(function(error) {
    console.error('Failed to subscribe the user: ', error);
    updateBtn();
  });
}

function updateSubscriptionOnServer(subscription) {
  // TODO: Send subscription to application server
  
  // const subscriptionJson = document.querySelector('.js-subscription-json');
  // const subscriptionDetails =
    // document.querySelector('.js-subscription-details');

  if (subscription) {
    // subscriptionJson.textContent = JSON.stringify(subscription);
    // subscriptionDetails.classList.remove('is-invisible');

    // Send data to database
    var datastring = JSON.stringify(subscription)
    $.ajax({
      url : "/push-api", // Url of backend (can be python, php, etc..)
      type: "POST", // data type (can be get, post, put, delete)
      data : datastring, // data in json format
      contentType: 'application/json',
      async : false, // enable or disable async (optional, but suggested as false if you need to populate data afterwards)
      success: function(response, textStatus, jqXHR) {
        console.log(response);
      },
      error: function (jqXHR, textStatus, errorThrown) {
      console.log(jqXHR);
          console.log(textStatus);
          console.log(errorThrown);
      }
  });
    
  } else {
    // subscriptionDetails.classList.add('is-invisible');
  }
}

// Get user subcription
function unsubscribeUser() {
  swRegistration.pushManager.getSubscription()
  .then(function(subscription) {
    if (subscription) {
      // TODO: Tell application server to delete subscription
       // Send data to database
    var datastring = JSON.stringify(subscription)
    $.ajax({
      url : "/delete-push-api", // Url of backend (can be python, php, etc..)
      type: "POST", // data type (can be get, post, put, delete)
      data : datastring, // data in json format
      contentType: 'application/json',
      async : false, // enable or disable async (optional, but suggested as false if you need to populate data afterwards)
      success: function(response, textStatus, jqXHR) {
        console.log(response);
      },
      error: function (jqXHR, textStatus, errorThrown) {
      console.log(jqXHR);
          console.log(textStatus);
          console.log(errorThrown);
      }
  });
      return subscription.unsubscribe();
    }
  })
  .catch(function(error) {
    console.log('Error unsubscribing', error);
  })
  .then(function() {
    updateSubscriptionOnServer(null);

    console.log('User is unsubscribed.');
    isSubscribed = false;

    updateBtn();
  });
}