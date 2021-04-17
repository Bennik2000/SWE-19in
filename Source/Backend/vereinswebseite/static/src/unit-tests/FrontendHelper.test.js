const { expect } = require('@jest/globals');

/*********************************************** Testing the validateEmail function as used in the FrontendHelper ***********************************************/ 
function validateEmailTest(email) {
  var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

//-------------------- validating incorrect emails --------------------//
test('detecting an incorrect email: "jannikwell-online.de"', () => {
  expect(validateEmailTest('jannikwell-online.de')).toBe(false);
});

test('detecting an incorrect email: "jannik@well-online"', () => {
  expect(validateEmailTest('jannik@well-online')).toBe(false);
});

test('detecting an incorrect email: "jannikwell-online.de"', () => {
  expect(validateEmailTest('jannikwell-online.de')).toBe(false);
});

test('detecting an incorrect email: "jannik@well-online,de"', () => {
  expect(validateEmailTest('jannik@well-online,de')).toBe(false);
});


//-------------------- validating correct emails --------------------//
test('detecting a correct email: "jannik@well-online.de"', () => {
  expect(validateEmailTest('jannik@well-online.de')).toBe(true);
});  

test('detecting a correct email: "xyz@zxy.yxz"', () => {
  expect(validateEmailTest('xyz@zxy.yxz')).toBe(true);
});  
/****************************************************************************************************************************************************************/



//-------------------- testing the creation of a JSON-Object --------------------//

var obj = {};
obj["email"] = "jannik@well-online.de";
obj["name"] = "Jannik Well";
obj["password"] = "password123";
obj["token"] = "123";

test('correct created JSON-Object as sent to the server"', () => {
  expect(obj).toMatchObject({email: "jannik@well-online.de", name: "Jannik Well", password: "password123", token: "123"});
});



