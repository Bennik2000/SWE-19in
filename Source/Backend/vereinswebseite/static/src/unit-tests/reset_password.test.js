const { expect } = require('@jest/globals');
const testObj = require('../create_account');


//-------------------- testing the creation of a JSON-Object --------------------//
test('correct created JSON-Object as sent to the server"', () => {
    var obj = {};
    obj["email"] = "jannik@well-online.de";
    expect(obj).toMatchObject({email: "jannik@well-online.de"});
  });