
const CryptoJS = require('crypto-js');

var nonce = 'WRmA2e/L5mm3OEFLgH75qZ2g7cKSQZ//w+m48HDMyvM=';
var saltedpwd = '59be9ef39e4bdec37d2d3682bb03d7b9abadb304c841b7a498c02bec1acad87a';
var noncedpwd = CryptoJS.SHA256(CryptoJS.enc.Hex.parse(CryptoJS.enc.Base64.parse(nonce) + saltedpwd)).toString(CryptoJS.enc.Base64);

console.log(noncedpwd);

