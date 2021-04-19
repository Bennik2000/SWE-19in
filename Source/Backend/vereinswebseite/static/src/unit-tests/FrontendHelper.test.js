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



/********************************************* Testing the makeHttpRequest function of the FrontendHelper ***********************************************/ 
//-------------------------- testing the function call of makeHttpRequest for creating an user --------------------------//
test('correct called FrontendHelper.makeHttpRequest(...) for creating a new user', () => {
  // create the JSON-Object for creating an user
  var jsonObj = {};
  jsonObj["email"] = "test@test.com";
  jsonObj["name"] = "Test User";
  jsonObj["password"] = "password123";
  jsonObj["token"] = "123";
  
  frontendHelper.testRequestCallback =  (request, route, json) => {
      expect(request).toBe("POST");
      expect(route).toBe("/users");
      expect(json).toMatchObject({email: "test@test.com", name: "Test User", password: "password123", token: "123"});

      var responseObj = {};
      responseObj["success"] = true;
      return responseObj;
  }
  function myOnloadFunction(response){
      expect(response.success).toBe(true);
  }
  frontendHelper.makeHttpRequest("POST", "/users", jsonObj, myOnloadFunction)
}); 
