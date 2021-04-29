/* const {frontendHelper} = require('../FrontendHelper');
frontendHelper.isTesting = true;
const {createAccount} = require('../create_account');

/******************* create a JSON-Object with test values ************************** 
var jsonObj = {};
jsonObj["email"] = "test@test.com";
jsonObj["name"] = "Test User";
jsonObj["password"] = "password123";
jsonObj["token"] = "123";

test('correct created JSON-Object as sent to the server"', () => {
  expect(jsonObj).toMatchObject({email: "test@test.com", name: "Test User", password: "password123", token: "123"});
});
/*************************************************************************************


/*************** call the API correctly and check the response *********************** 
test('correct API call', () => {
  var requestMade = false;

  function requestCallback(request, route, json) {
      expect(request).toBe("POST");
      expect(route).toBe("/api/users");
      expect(json).toMatchObject({
          email: "test@test.com",
          name: "Test User",
          password: "password123",
          token: "123"
      });

      var responseObj = {};
      responseObj["success"] = true;

      requestMade = true;

      return responseObj;
  }

  frontendHelper.testRequestCallback = requestCallback

  function myOnloadFunction(response) {
    expect(response.success).toBe(true)
  }

  frontendHelper.makeHttpRequest("POST", "/api/users", jsonObj, myOnloadFunction);

  expect(requestMade).toBe(true)
});
/*************************************************************************************/ 