const { expect } = require('@jest/globals');
const testObj = require('../create_account');

//-------------------- validating incorrect emails --------------------//
test('detecting an incorrect email: "jannikwell-online.de"', () => {
  expect(testObj.validateEmail('jannikwell-online.de')).toBe(false);
});

test('detecting an incorrect email: "jannik@well-online"', () => {
  expect(testObj.validateEmail('jannik@well-online')).toBe(false);
});

test('detecting an incorrect email: "jannikwell-online.de"', () => {
  expect(testObj.validateEmail('jannikwell-online.de')).toBe(false);
});

test('detecting an incorrect email: "jannik@well-online,de"', () => {
  expect(testObj.validateEmail('jannik@well-online,de')).toBe(false);
});


//-------------------- validating correct emails --------------------//
test('detecting a correct email: "jannik@well-online.de"', () => {
  expect(testObj.validateEmail('jannik@well-online.de')).toBe(true);
});  

test('detecting a correct email: "xyz@zxy.yxz"', () => {
  expect(testObj.validateEmail('xyz@zxy.yxz')).toBe(true);
});  


//-------------------- testing the creation of a JSON-Object --------------------//
test('correct created JSON-Object as sent to the server"', () => {
  var obj = {};
  obj["email"] = "jannik@well-online.de";
  obj["name"] = "Jannik Well";
  obj["password"] = "password123";
  obj["token"] = "123";
  expect(obj).toMatchObject({email: "jannik@well-online.de", name: "Jannik Well", password: "password123", token: "123"});
});  