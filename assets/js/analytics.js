'use strict';

// Use the existing personal-site dashboard. Namespace pageviews so that the
// two homepages do not merge; download event names stay identical on both sites.
// This file must load before GoatCounter's count.js (both scripts use defer).
window.goatcounter = window.goatcounter || {};
window.goatcounter.path = function (path) {
  return path.charAt(0) === '/' ? '/ryba' + path : path;
};
