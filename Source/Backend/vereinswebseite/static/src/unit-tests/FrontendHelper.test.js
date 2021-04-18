const { expect } = require('@jest/globals');
const {frontendHelper} = require('../FrontendHelper');
frontendHelper.isTesting = true;

/*********************************************** Testing the validateEmail function of the FrontendHelper ***********************************************/ 


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
/*************************************************************************************************************************************************************/



/********************************************* Testing the manageXMLHttpRequest function of the FrontendHelper ***********************************************/ 

//------------------------------------------ testing the creation of a JSON-Object ------------------------------------------//
// create the JSON-Object for creating an user
var jsonObj = {};
jsonObj["email"] = "jannik@well-online.de";
jsonObj["name"] = "Jannik Well";
jsonObj["password"] = "password123";
jsonObj["token"] = "123";

test('correct created JSON-Object as sent to the server"', () => {
  expect(jsonObj).toMatchObject({email: "jannik@well-online.de", name: "Jannik Well", password: "password123", token: "123"});
});


//-------------------------- testing the function call of manageXMLhttpRequest for creating an user --------------------------//
test('correct called FrontendHelper.manageXMLHttpRequest(...) for creating a new user', () => {
  frontendHelper.testXHRequestCallback =  (request, route, json) => {
      expect(request).toBe("POST");
      expect(route).toBe("/users");
      expect(json).toBe(jsonObj);

      var responseObj = {};
      responseObj["success"] = true;
      return responseObj;
  }
  function myOnloadFunction(response){
      expect(response.success).toBe(true);
  }
  frontendHelper.manageXMLHttpRequest("POST", "/users", jsonObj, myOnloadFunction)
}); 
