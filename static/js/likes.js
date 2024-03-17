"use strict";

const API_URL = '/api/';
const $likeBtn = $('#likebtn');

/** API GET call, does user like stop; Return Array of [Boolean and stopId]*/

async function checkIfLiked() {
  const stopId = $likeBtn.attr('data-id');
  const params = new URLSearchParams({ 'stop_id': stopId });

  const resp = await fetch(`${API_URL}likes?${params}`);
  const json = await resp.json();

  return [json.likes, stopId];

}

function renderHTML(isLiked) {
  if (isLiked === 'true') {
    $likeBtn.html('UnLike Stop');

  } else {
    $likeBtn.html('Like Stop');
  }

}


async function userLikesStop(stopId) {
  const resp = await fetch(
    `${API_URL}like`,
    {
      method: 'POST',
      body: JSON.stringify({ 'stop_id': stopId }),
      headers: {
        'Content-Type': 'application/json'
      }
    });

  $likeBtn.html('UnLike Stop');
}


async function userUnlikesStop(stopId) {
  const resp = await fetch(
    `${API_URL}unlike`,
    {
      method: 'POST',
      body: JSON.stringify({ 'stop_id': stopId }),
      headers: {
        'Content-Type': 'application/json'
      }
    });

  $likeBtn.html('Like Stop');
}

async function handleClick() {
  const [isLiked, stopId] = await checkIfLiked();
  if (isLiked === 'true') {
    userUnlikesStop(stopId);
  } else {
    userLikesStop(stopId);
  }
}

$likeBtn.on('click', handleClick);

async function onLoad() {
  const [isLiked, stopId] = await checkIfLiked();
  const renderHTMl = renderHTML(isLiked);
}


onLoad();

