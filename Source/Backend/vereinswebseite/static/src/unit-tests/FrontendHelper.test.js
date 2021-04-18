const { expect } = require('@jest/globals');
const {frontendHelper} = require('../FrontendHelper');
frontendHelper.isTesting = true;

/*********************************************** Testing the validateEmail function as used in the FrontendHelper ***********************************************/ 


//-------------------- validating incorrect emails --------------------//
test('detecting an incorrect email: "jannikwell-online.de"', () => {
  expect(frontendHelper.validateEmail('jannikwell-online.de')).toBe(false);
});

test('detecting an incorrect email: "jannik@well-online"', () => {
  expect(frontendHelper.validateEmail('jannik@well-online')).toBe(false);
});

test('detecting an incorrect email: "jannikwell-online.de"', () => {
  expect(frontendHelper.validateEmail('jannikwell-online.de')).toBe(false);
});

test('detecting an incorrect email: "jannik@well-online,de"', () => {
  expect(frontendHelper.validateEmail('jannik@well-online,de')).toBe(false);
});


//-------------------- validating correct emails --------------------//
test('detecting a correct email: "jannik@well-online.de"', () => {
  expect(frontendHelper.validateEmail('jannik@well-online.de')).toBe(true);
});  

test('detecting a correct email: "xyz@zxy.yxz"', () => {
  expect(frontendHelper.validateEmail('xyz@zxy.yxz')).toBe(true);
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



test('test', () => {
  frontendHelper.testXHRequestCallback =  (request, route, json) => {
      expect(request).toBe("POST")
      // TODO: route, json überprüfen
      var responseObj = {};
      responseObj["success"] = true;
      return responseObj;
  }
  function myOnloadFunction(response){

  }
  frontendHelper.manageXMLHttpRequest("POST", "/users", obj, myOnloadFunction)
}); 
